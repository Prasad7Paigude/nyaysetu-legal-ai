"""
NyaySetu - Smart Legal Validation System.

Provides pre-generation validation for RTI applications and affidavits,
including jurisdiction checks, Section 8 compliance, date consistency,
and statement-quality analysis.
"""

import json
import logging
import os
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from config.settings import DATA_DIR

logger = logging.getLogger(__name__)


class SmartLegalValidator:
    """Advanced legal validation with jurisdiction-aware rules and compliance checks."""

    INDIAN_STATES: List[str] = [
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chhattisgarh",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",
        "Delhi",
        "Jammu and Kashmir",
        "Ladakh",
    ]

    def __init__(self) -> None:
        """Initialise validator with empty result buffers and load reference data."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.blocking_issues: List[str] = []
        self.suggestions: List[str] = []
        self.jurisdictions: Dict[str, Any] = {}
        self.rti_categories: Dict[str, Any] = {}
        self.load_jurisdiction_profiles()
        self.load_rti_categories()

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_jurisdiction_profiles(self) -> None:
        """Load jurisdiction profiles from the shared data directory."""
        try:
            profiles_path = DATA_DIR / "jurisdiction_profiles.json"
            with open(profiles_path, "r", encoding="utf-8") as f:
                self.jurisdictions = json.load(f)
            logger.debug("Loaded %s jurisdiction profiles", len(self.jurisdictions))
        except Exception as exc:
            logger.warning("Failed to load jurisdiction_profiles.json: %s", exc)
            self.jurisdictions = {}

    def load_rti_categories(self) -> None:
        """Load RTI category data from the shared data directory."""
        try:
            cat_path = DATA_DIR / "rti_categories.json"
            with open(cat_path, "r", encoding="utf-8") as f:
                self.rti_categories = json.load(f)
            logger.debug("Loaded RTI categories from %s", cat_path)
        except Exception as exc:
            logger.warning("Failed to load rti_categories.json: %s", exc)
            self.rti_categories = {}

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear all accumulated validation results."""
        self.errors.clear()
        self.warnings.clear()
        self.blocking_issues.clear()
        self.suggestions.clear()

    # ------------------------------------------------------------------
    # RTI validation
    # ------------------------------------------------------------------

    def validate_rti_application(self, user_data: Dict[str, Any]) -> bool:
        """Run smart validation on an RTI application.

        Args:
            user_data: Dictionary of applicant-provided data.

        Returns:
            True when no blocking issues or errors are found.
        """
        self.reset()
        required_fields = [
            "name",
            "address",
            "state",
            "authority",
            "pio_address",
            "info",
        ]
        for field in required_fields:
            if not user_data.get(field) or not str(user_data[field]).strip():
                self.errors.append(f"Missing required field: {field}")

        if self.errors:
            return False

        self._validate_name(user_data["name"], "Applicant Name")
        self._validate_address(user_data["address"])
        self._validate_state_jurisdiction(user_data["state"])
        self._validate_authority_name(user_data["authority"])
        self._validate_information_request(
            user_data["info"], user_data.get("state")
        )

        if user_data.get("contact"):
            self._validate_contact(user_data["contact"])
        if user_data.get("bpl"):
            self._validate_bpl_details(user_data, user_data.get("state"))

        self._check_section_8_compliance(user_data["info"])

        if user_data.get("application_date"):
            self._validate_date_consistency(user_data["application_date"])

        return len(self.blocking_issues) == 0 and len(self.errors) == 0

    # ------------------------------------------------------------------
    # Affidavit validation
    # ------------------------------------------------------------------

    def validate_affidavit(self, user_data: Dict[str, Any]) -> bool:
        """Run smart validation on an affidavit.

        Args:
            user_data: Dictionary of deponent-provided data.

        Returns:
            True when no blocking issues or errors are found.
        """
        self.reset()
        required_fields = [
            "deponent_name",
            "age",
            "father_name",
            "address",
            "statements",
        ]
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                self.errors.append(f"Missing required field: {field}")

        if self.errors:
            return False

        age_valid, guardian_needed = self._validate_age_for_affidavit(
            user_data["age"],
            user_data.get("state", "Maharashtra"),
        )
        if not age_valid:
            return False

        if guardian_needed:
            if not user_data.get("guardian_name"):
                self.blocking_issues.append(
                    "Deponent is minor (under 18). "
                    "Guardian details are MANDATORY."
                )
                self.errors.append("Guardian name is required for minor deponents")
            if not user_data.get("guardian_age"):
                self.errors.append("Guardian age is required")
            if not user_data.get("guardian_father_name"):
                self.errors.append("Guardian's father's name is required")
            if user_data.get("guardian_age"):
                try:
                    g_age = int(user_data["guardian_age"])
                    if g_age < 18:
                        self.blocking_issues.append(
                            "Guardian must be at least 18 years old"
                        )
                except ValueError:
                    self.errors.append("Guardian age must be a valid number")

        self._validate_name(user_data["deponent_name"], "Deponent Name")
        self._validate_name(
            user_data["father_name"], "Father's/Husband's Name"
        )
        if guardian_needed and user_data.get("guardian_name"):
            self._validate_name(user_data["guardian_name"], "Guardian Name")

        self._validate_address(user_data["address"])
        self._validate_affidavit_statements(user_data["statements"])

        if user_data.get("state"):
            self._validate_state_jurisdiction(user_data["state"])
            self._check_stamp_requirements(user_data["state"])

        return len(self.blocking_issues) == 0 and len(self.errors) == 0

    # ------------------------------------------------------------------
    # Individual validators
    # ------------------------------------------------------------------

    def _validate_name(self, name: str, field_name: str) -> None:
        """Validate that a name field is well-formed.

        Args:
            name: The name value to check.
            field_name: Human-readable label for error messages.
        """
        if len(name) < 3:
            self.errors.append(f"{field_name} must be at least 3 characters")
        if not re.match(r"^[A-Za-z\s\.]+$", name):
            self.warnings.append(
                f"{field_name} contains special characters. "
                "Legal documents typically use only letters"
            )
        if name.isupper() or name.islower():
            self.suggestions.append(
                f"Use proper capitalization for {field_name} "
                "(e.g., 'Rajesh Kumar')"
            )

    def _validate_address(self, address: str) -> None:
        """Validate that an address is complete and contains a PIN code.

        Args:
            address: The address string to check.
        """
        if len(address) < 15:
            self.warnings.append(
                "Address seems very short. Provide complete address "
                "including house/flat number, street, city, and PIN code"
            )
        if not re.search(r"\b\d{6}\b", address):
            self.warnings.append(
                "Address should include 6-digit PIN code"
            )
        if len(address) < 30:
            self.suggestions.append(
                "Recommended address format: "
                "'House No., Street/Area, City, State - PIN'"
            )

    def _validate_state_jurisdiction(self, state: str) -> bool:
        """Check that the state is recognised and that jurisdiction data exists.

        Args:
            state: Indian state or UT name.

        Returns:
            True if the state is valid.
        """
        if state not in self.INDIAN_STATES:
            self.errors.append(
                f"'{state}' is not a valid Indian state/UT"
            )
            self.suggestions.append(
                "Did you mean one of: Maharashtra, Karnataka, "
                "Delhi, Gujarat, Tamil Nadu?"
            )
            return False
        if state not in self.jurisdictions:
            self.warnings.append(
                f"Limited jurisdiction data for {state}. Using default rules"
            )
            self.suggestions.append(
                "For best results, use: Maharashtra, Karnataka, Delhi, "
                "Gujarat, Tamil Nadu, UP, West Bengal, or Rajasthan"
            )
        return True

    def _validate_authority_name(self, authority: str) -> None:
        """Ensure the authority name is sufficiently detailed.

        Args:
            authority: Public authority / department name.
        """
        if len(authority) < 5:
            self.errors.append("Authority/Department name is too short")
        if any(abbr in authority for abbr in ["Corp", "Dept", "Off"]):
            self.suggestions.append(
                "Use full authority name (e.g., 'Municipal Corporation' "
                "not 'Muncipal Corp')"
            )

    def _validate_information_request(
        self,
        info_text: str,
        state: Optional[str] = None,
    ) -> None:
        """Check the quality and specificity of an RTI information request.

        Args:
            info_text: The body of the information request.
            state: Optional state name for context-specific checks.
        """
        info_length = len(info_text.strip())
        if info_length < 30:
            self.warnings.append(
                "Information request is very brief. "
                "Be more specific for better results"
            )
            self.suggestions.append(
                "Include: specific documents, time periods, "
                "file numbers, departments"
            )
        if info_length > 3000:
            self.warnings.append(
                "Request is very long. "
                "Consider breaking into multiple applications"
            )

        specificity_markers = [
            "copy of",
            "details of",
            "list of",
            "information regarding",
        ]
        if not any(marker in info_text.lower() for marker in specificity_markers):
            self.suggestions.append(
                "Start with specific phrases: "
                "'Copy of...', 'Details of...', 'List of...'"
            )

        has_time_period = any(
            kw in info_text.lower()
            for kw in [
                "year",
                "month",
                "period",
                "from",
                "to",
                "during",
                "2020",
                "2021",
                "2022",
                "2023",
                "2024",
                "2025",
            ]
        )
        if not has_time_period:
            self.warnings.append(
                "No time period specified. "
                "Specify date range for better clarity"
            )
            self.suggestions.append(
                "Example: 'from January 2023 to December 2023' "
                "or 'for financial year 2023-24'"
            )

        question_marks = info_text.count("?")
        if question_marks > 2:
            self.warnings.append(
                "RTI is for information/documents, "
                "not for answering questions"
            )
            self.suggestions.append(
                "Instead of 'Why was X done?', request "
                "'Copy of file noting explaining decision on X'"
            )

    def _validate_contact(self, contact: str) -> None:
        """Validate a contact string as either mobile or email.

        Args:
            contact: The contact value to check.
        """
        contact = contact.strip()
        mobile_pattern = r"^[6-9]\d{9}$"
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        is_mobile = re.match(mobile_pattern, contact)
        is_email = re.match(email_pattern, contact)

        if not (is_mobile or is_email):
            self.warnings.append(
                "Contact should be valid 10-digit mobile "
                "(starting with 6-9) or email"
            )

    def _validate_bpl_details(
        self,
        user_data: Dict[str, Any],
        state: Optional[str],
    ) -> None:
        """Validate BPL card details and state exemption.

        Args:
            user_data: Full applicant data dictionary.
            state: The selected state name.
        """
        if not user_data.get("bpl_card_number"):
            self.warnings.append(
                "BPL applicants should provide BPL card number for verification"
            )
            self.suggestions.append(
                "Add BPL card number to avoid fee payment issues"
            )
        if state and state in self.jurisdictions:
            rti_rules = self.jurisdictions[state]["rti_rules"]
            if not rti_rules.get("bpl_exemption"):
                self.warnings.append(
                    f"{state} may not offer BPL fee exemption. "
                    "Verify with local rules"
                )

    def _check_section_8_compliance(self, info_text: str) -> None:
        """Scan the request text for potentially exempt information categories.

        Args:
            info_text: The body of the information request.
        """
        if not self.rti_categories:
            return

        info_lower = info_text.lower()
        detected_issues: List[Dict[str, str]] = []
        auto_detect = self.rti_categories.get("auto_detect_keywords", {})

        for category, keywords in auto_detect.items():
            for keyword in keywords:
                if keyword.lower() in info_lower:
                    cat_info = self.rti_categories["categories"].get(category, {})
                    if cat_info.get("section_8_exempt"):
                        detected_issues.append(
                            {
                                "category": cat_info.get("name", category),
                                "exemption": cat_info.get(
                                    "exemption_reference", "Section 8"
                                ),
                                "keyword": keyword,
                            }
                        )
                        if cat_info.get("block_generation"):
                            self.blocking_issues.append(
                                f"Request likely to be REJECTED: "
                                f"{cat_info.get('block_message', 'Highly exempt category')}"
                            )
                    break

        if detected_issues:
            self.warnings.append(
                f"Detected {len(detected_issues)} potential exemption(s) "
                "under RTI Act:"
            )
            for issue in detected_issues:
                self.warnings.append(
                    f"  - {issue['category']} ({issue['exemption']}) -- "
                    f"keyword: '{issue['keyword']}'"
                )
            self.suggestions.append(
                "Review Section 8 & 9 of RTI Act. "
                "Consider narrowing request to non-exempt aspects"
            )

    def _validate_date_consistency(self, application_date: str) -> None:
        """Ensure an application date is not in the future and is recent.

        Args:
            application_date: Date string in YYYY-MM-DD format.
        """
        try:
            app_date = datetime.strptime(application_date, "%Y-%m-%d")
            today = datetime.now()
            if app_date > today:
                self.errors.append("Application date cannot be in the future")
            days_old = (today - app_date).days
            if days_old > 90:
                self.warnings.append(
                    f"Application date is {days_old} days old. "
                    "RTI must be filed within reasonable time"
                )
        except ValueError:
            self.errors.append("Invalid date format. Use YYYY-MM-DD")

    def _validate_age_for_affidavit(
        self,
        age: str,
        state: str,
    ) -> Tuple[bool, bool]:
        """Parse age and determine whether a guardian is required.

        Args:
            age: Age as a string.
            state: State name for jurisdiction-specific age limit.

        Returns:
            Tuple of (is_valid, guardian_needed).
        """
        try:
            age_int = int(age)
        except ValueError:
            self.errors.append("Age must be a valid number")
            return False, False

        if age_int < 1 or age_int > 120:
            self.errors.append("Age must be between 1 and 120")
            return False, False

        guardian_age_limit = 18
        if state in self.jurisdictions:
            guardian_age_limit = self.jurisdictions[state][
                "affidavit_rules"
            ].get("guardian_age_limit", 18)

        guardian_needed = age_int < guardian_age_limit
        if guardian_needed:
            self.warnings.append(
                f"Deponent is minor (age {age_int}). "
                "Guardian details are REQUIRED"
            )
            self.suggestions.append(
                "Provide guardian's name, age, and father's name"
            )
        return True, guardian_needed

    def _validate_affidavit_statements(self, statements: List[str]) -> None:
        """Check affidavit statements for quality, hearsay, and formatting.

        Args:
            statements: List of statement strings.
        """
        if not statements:
            self.errors.append("Affidavit must contain at least one statement")
            return

        if len(statements) > 30:
            self.warnings.append(
                "Affidavit has many statements. "
                "Consider creating multiple affidavits if unrelated"
            )

        for i, statement in enumerate(statements, 1):
            if not statement.strip():
                self.errors.append(f"Statement {i} is empty")
                continue
            if len(statement) < 10:
                self.warnings.append(
                    f"Statement {i} is very brief. Be more specific"
                )

            opinion_words = [
                "think",
                "believe",
                "feel",
                "probably",
                "maybe",
                "might",
                "could be",
            ]
            if any(word in statement.lower() for word in opinion_words):
                self.warnings.append(
                    f"Statement {i} contains opinion words. "
                    "Affidavits should state facts only"
                )
                self.suggestions.append(
                    f"Statement {i}: Replace opinions with factual statements"
                )

            hearsay_indicators = [
                "i heard",
                "someone told",
                "it is said",
                "people say",
                "rumor",
            ]
            if any(phrase in statement.lower() for phrase in hearsay_indicators):
                self.warnings.append(
                    f"Statement {i} may be based on hearsay. "
                    "Use direct knowledge only"
                )

            if not statement.lower().strip().startswith("that"):
                self.suggestions.append(
                    f"Statement {i}: Should start with 'that' "
                    "as per legal format"
                )

    def _check_stamp_requirements(self, state: str) -> None:
        """Add a suggestion if the state mandates stamp paper for affidavits.

        Args:
            state: State name to look up.
        """
        if state in self.jurisdictions:
            affidavit_rules = self.jurisdictions[state]["affidavit_rules"]
            if affidavit_rules.get("stamp_mandatory"):
                stamp_value = affidavit_rules.get("stamp_paper_value", 0)
                self.suggestions.append(
                    f"{state} requires affidavit on stamp paper of "
                    f"Rs. {stamp_value}/-. "
                    "This will be noted in the generated document"
                )

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def get_validation_report(self) -> str:
        """Build a human-readable validation report string.

        Returns:
            Multi-line report summarising all issues, warnings, and suggestions.
        """
        lines: List[str] = []

        if self.blocking_issues:
            lines.append("BLOCKING ISSUES (CANNOT PROCEED):")
            lines.append("=" * 60)
            for issue in self.blocking_issues:
                lines.append(f"  {issue}")
            lines.append("")
        if self.errors:
            lines.append("ERRORS (Must Fix):")
            lines.append("=" * 60)
            for error in self.errors:
                lines.append(f"  {error}")
            lines.append("")
        if self.warnings:
            lines.append("WARNINGS (Strongly Recommended):")
            lines.append("=" * 60)
            for warning in self.warnings:
                lines.append(f"  {warning}")
            lines.append("")
        if self.suggestions:
            lines.append("SUGGESTIONS (For Better Results):")
            lines.append("=" * 60)
            for suggestion in self.suggestions:
                lines.append(f"  {suggestion}")
            lines.append("")
        if not self.errors and not self.blocking_issues and not self.warnings:
            lines.append("All validations passed! Document is ready for generation.")
            lines.append("=" * 60)

        return "\n".join(lines) if lines else "Validation complete."

    def has_blocking_issues(self) -> bool:
        """Check whether there are issues that prevent document generation.

        Returns:
            True if blocking issues or errors exist.
        """
        return bool(self.blocking_issues) or bool(self.errors)

    def get_complexity_score(
        self,
        user_data: Dict[str, Any],
        doc_type: str,
    ) -> Tuple[Dict[str, int], int]:
        """Calculate a complexity score breakdown for demonstration.

        Args:
            user_data: Applicant data dictionary.
            doc_type: Either 'RTI' or another type.

        Returns:
            Tuple of (score_dict, total_score).
        """
        score: Dict[str, int] = {
            "validation_checks": 0,
            "jurisdiction_rules": 0,
            "legal_compliance": 0,
            "smart_features": 0,
        }

        score["validation_checks"] = (
            len(self.errors) + len(self.warnings) + len(self.suggestions)
        )
        if user_data.get("state") in self.jurisdictions:
            score["jurisdiction_rules"] = 5
        if doc_type == "RTI":
            detected = self._detect_categories_internal(
                user_data.get("info", "")
            )
            score["legal_compliance"] = len(detected) * 3
        score["smart_features"] = 8

        return score, sum(score.values())

    def _detect_categories_internal(self, info_text: str) -> List[str]:
        """Internal category detection used for scoring.

        Args:
            info_text: The text of the information request.

        Returns:
            List of matched category keys.
        """
        if not self.rti_categories:
            return []
        info_lower = info_text.lower()
        detected: List[str] = []
        auto_detect = self.rti_categories.get("auto_detect_keywords", {})
        for category, keywords in auto_detect.items():
            if any(kw.lower() in info_lower for kw in keywords):
                detected.append(category)
        return detected
