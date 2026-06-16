"""
NyaySetu - Advanced Legal Document Generation Engine.

Features:
- Jurisdiction-aware document variants
- Smart legal validation
- Document lifecycle tracking
- Explainable clause generation
- Auto-appeal generation for RTI
"""

import hashlib
import json
import logging
import os
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config.settings import DATA_DIR, DRAFT_GEN_DIR

from draft_generation.database import NyaySetuDB

logger = logging.getLogger(__name__)


class JurisdictionManager:
    """Manages jurisdiction-specific legal requirements, profiles, and RTI categories."""

    def __init__(self) -> None:
        """Load jurisdiction profiles and RTI category data from disk."""
        self.profiles: Dict[str, Any] = {}
        self.category_data: Dict[str, Any] = {}
        self.load_profiles()
        self.load_categories()

    def load_profiles(self) -> None:
        """Load jurisdiction profiles from the shared data directory."""
        try:
            profiles_path = DATA_DIR / "jurisdiction_profiles.json"
            with open(profiles_path, "r", encoding="utf-8") as f:
                self.profiles = json.load(f)
            logger.debug("Loaded %s jurisdiction profiles", len(self.profiles))
        except Exception as exc:
            logger.error("Failed to load jurisdiction profiles: %s", exc)
            self.profiles = {"Maharashtra": self._default_profile()}

    @staticmethod
    def _default_profile() -> Dict[str, Any]:
        """Return a sensible default jurisdiction profile when loading fails."""
        return {
            "rti_rules": {
                "fee": 10,
                "payment_modes": ["Cash", "DD", "IPO"],
                "bpl_exemption": True,
                "pio_designation": "Public Information Officer",
                "appellate_designation": "First Appellate Authority",
            },
            "affidavit_rules": {
                "stamp_paper_value": 100,
                "stamp_mandatory": True,
                "notary_required": True,
                "guardian_age_limit": 18,
                "court_designation": "Civil Judge (Junior Division)",
                "verification_format": "notary_format",
                "witness_required": False,
            },
        }

    def load_categories(self) -> None:
        """Load RTI categories and compliance rules from the shared data directory."""
        try:
            categories_path = DATA_DIR / "rti_categories.json"
            with open(categories_path, "r", encoding="utf-8") as f:
                self.category_data = json.load(f)
            logger.debug("Loaded RTI categories from %s", categories_path)
        except Exception as exc:
            logger.error("Failed to load RTI categories: %s", exc)
            self.category_data = {"auto_detect_keywords": {}, "categories": {}, "additional_clauses_library": {}}

    def get_jurisdiction(self, state: str) -> Dict[str, Any]:
        """Return the jurisdiction profile for a given state.

        Args:
            state: Indian state name.

        Returns:
            Jurisdiction profile dictionary. Falls back to Maharashtra.
        """
        return self.profiles.get(state, self.profiles.get("Maharashtra", self._default_profile()))

    def detect_rti_category(self, info_text: str) -> List[str]:
        """Detect RTI information categories from the request text.

        Args:
            info_text: The body of the information request.

        Returns:
            List of unique category keys that matched keywords.
        """
        info_lower = info_text.lower()
        detected: List[str] = []
        categories = self.category_data.get("auto_detect_keywords", {})
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in info_lower:
                    detected.append(category)
                    break
        return list(set(detected))

    def get_category_info(self, category_key: str) -> Dict[str, Any]:
        """Get full information about a specific RTI category.

        Args:
            category_key: The category identifier.

        Returns:
            Category information dictionary, or empty dict.
        """
        return self.category_data.get("categories", {}).get(category_key, {})

    def get_additional_clause(self, clause_key: str) -> Dict[str, Any]:
        """Get an additional clause text by its library key.

        Args:
            clause_key: The clause identifier.

        Returns:
            Clause data dictionary, or empty dict.
        """
        return self.category_data.get("additional_clauses_library", {}).get(clause_key, {})


class DocumentLifecycle:
    """Tracks document lifecycle states and manages deadlines via MongoDB."""

    STATES: Dict[str, str] = {
        "DRAFTED": "Document has been generated",
        "SUBMITTED": "Document submitted to authority",
        "ACKNOWLEDGED": "Receipt acknowledged by authority",
        "REPLY_RECEIVED": "Response received from authority",
        "APPEAL_FILED": "First appeal filed",
        "CLOSED": "Matter resolved/closed",
    }

    def __init__(self) -> None:
        """Initialise lifecycle manager and attempt to load existing records."""
        self.db: NyaySetuDB = NyaySetuDB()
        self.lifecycles: Dict[str, Any] = (
            self.db.get_lifecycles() if self.db.client is not None else {}
        )

    def create_lifecycle(
        self,
        doc_hash: str,
        doc_type: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create a new document lifecycle with calculated deadlines.

        Args:
            doc_hash: Unique document hash.
            doc_type: Document type identifier.
            metadata: Arbitrary metadata attached to the document.

        Returns:
            Dictionary of computed deadlines.
        """
        deadlines = self._calculate_deadlines(doc_type, metadata)

        if self.db.client is not None:
            try:
                self.db.save_lifecycle(doc_hash, doc_type, metadata, deadlines)
                self.lifecycles = self.db.get_lifecycles()
            except Exception as exc:
                logger.error("Failed to persist lifecycle: %s", exc)
                self._fallback_store(doc_hash, doc_type, metadata, deadlines)
        else:
            self._fallback_store(doc_hash, doc_type, metadata, deadlines)

        return deadlines

    def _fallback_store(
        self,
        doc_hash: str,
        doc_type: str,
        metadata: Dict[str, Any],
        deadlines: Dict[str, Any],
    ) -> None:
        """Store lifecycle in local dictionary when DB is unavailable."""
        self.lifecycles[doc_hash] = {
            "document_type": doc_type,
            "created_date": datetime.now().isoformat(),
            "current_state": "DRAFTED",
            "state_history": [
                {
                    "state": "DRAFTED",
                    "timestamp": datetime.now().isoformat(),
                    "notes": "Document generated",
                }
            ],
            "metadata": metadata,
            "deadlines": deadlines,
        }

    def _calculate_deadlines(
        self,
        doc_type: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compute statutory deadlines based on document type.

        Args:
            doc_type: Document type identifier.
            metadata: Document metadata (may include notice_period_days).

        Returns:
            Deadline dictionary with ISO-format dates.
        """
        now = datetime.now()

        if doc_type == "RTI_Application":
            reply_deadline = now + timedelta(days=30)
            appeal_deadline = now + timedelta(days=60)
            return {
                "reply_deadline": reply_deadline.isoformat(),
                "reply_deadline_days": 30,
                "first_appeal_deadline": appeal_deadline.isoformat(),
                "first_appeal_days": 30,
                "description": "RTI Act 2005 mandates response within 30 days of receipt",
            }

        if doc_type == "Legal_Notice":
            notice_period = metadata.get("notice_period_days", 15)
            notice_deadline = now + timedelta(days=notice_period)
            return {
                "response_deadline": notice_deadline.isoformat(),
                "response_deadline_days": notice_period,
                "description": f"Recipient must respond within {notice_period} days",
            }

        return {}

    def update_state(
        self,
        doc_hash: str,
        new_state: str,
        notes: str = "",
    ) -> bool:
        """Update the lifecycle state for a document.

        Args:
            doc_hash: Unique document hash.
            new_state: The new state string.
            notes: Optional human-readable note.

        Returns:
            True if the update succeeded.
        """
        if doc_hash not in self.lifecycles:
            logger.warning("Lifecycle not found for hash %s", doc_hash[:16])
            return False

        lifecycle = self.lifecycles[doc_hash]
        lifecycle["current_state"] = new_state
        lifecycle["state_history"].append(
            {
                "state": new_state,
                "timestamp": datetime.now().isoformat(),
                "notes": notes,
            }
        )
        return True

    def get_pending_deadlines(self) -> List[Dict[str, Any]]:
        """Return all pending deadlines sorted by urgency.

        Returns:
            List of deadline dictionaries with keys: doc_hash, doc_type,
            deadline_type, deadline_date, days_remaining, is_urgent.
        """
        pending: List[Dict[str, Any]] = []
        now = datetime.now()

        for doc_hash, lifecycle in self.lifecycles.items():
            if lifecycle["current_state"] in ("DRAFTED", "SUBMITTED", "ACKNOWLEDGED"):
                deadlines = lifecycle["deadlines"]
                for key, value in deadlines.items():
                    if key.endswith("_deadline") and isinstance(value, str):
                        try:
                            deadline_date = datetime.fromisoformat(value)
                            days_remaining = (deadline_date - now).days
                            if days_remaining >= 0:
                                pending.append(
                                    {
                                        "doc_hash": doc_hash,
                                        "doc_type": lifecycle["document_type"],
                                        "deadline_type": key,
                                        "deadline_date": value,
                                        "days_remaining": days_remaining,
                                        "is_urgent": days_remaining <= 7,
                                    }
                                )
                        except (ValueError, TypeError):
                            continue

        return sorted(pending, key=lambda x: x["days_remaining"])


class AdvancedDocumentEngine:
    """Base class for jurisdiction-aware document generation with lifecycle tracking."""

    def __init__(self) -> None:
        """Initialise styles, jurisdiction manager, lifecycle tracker, and explanation log."""
        self.styles: Any = self._setup_styles()
        self.jurisdiction_mgr: JurisdictionManager = JurisdictionManager()
        self.lifecycle_mgr: DocumentLifecycle = DocumentLifecycle()
        self.document_hash: Optional[str] = None
        self.explanation_log: List[Dict[str, Any]] = []

    def _setup_styles(self) -> Any:
        """Create a rich set of ParagraphStyles for legal document production.

        Returns:
            ReportLab stylesheet with added DocTitle, Subject, BodyJustify,
            and RightAlign styles.
        """
        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="DocTitle",
                parent=styles["Heading1"],
                fontSize=13,
                textColor=colors.black,
                spaceAfter=24,
                spaceBefore=12,
                alignment=TA_CENTER,
                fontName="Times-Bold",
                leading=16,
            )
        )

        styles.add(
            ParagraphStyle(
                name="Subject",
                parent=styles["Normal"],
                fontSize=11,
                textColor=colors.black,
                spaceAfter=14,
                spaceBefore=10,
                alignment=TA_LEFT,
                fontName="Times-Bold",
                leading=14,
            )
        )

        styles.add(
            ParagraphStyle(
                name="BodyJustify",
                parent=styles["Normal"],
                fontSize=11,
                textColor=colors.black,
                alignment=TA_JUSTIFY,
                fontName="Times-Roman",
                leading=15,
                spaceBefore=6,
                spaceAfter=6,
                firstLineIndent=0,
            )
        )

        styles.add(
            ParagraphStyle(
                name="RightAlign",
                parent=styles["Normal"],
                fontSize=11,
                alignment=TA_RIGHT,
                fontName="Times-Roman",
                leading=14,
            )
        )

        return styles

    def log_clause_explanation(
        self,
        clause_type: str,
        reason: str,
        legal_ref: str = "",
    ) -> None:
        """Record why a particular clause was added to the document.

        Args:
            clause_type: Short identifier for the clause.
            reason: Human-readable justification.
            legal_ref: Optional statutory reference.
        """
        self.explanation_log.append(
            {
                "clause_type": clause_type,
                "reason": reason,
                "legal_reference": legal_ref,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def generate_explanation_report(self) -> str:
        """Build a human-readable report of all clause decisions.

        Returns:
            Multi-line explanation string.
        """
        if not self.explanation_log:
            return "Standard document generated without additional clauses."

        lines: List[str] = ["Document Generation Explanation:", "=" * 50]
        for i, entry in enumerate(self.explanation_log, 1):
            lines.append(f"\n{i}. {entry['clause_type']}")
            lines.append(f"   Reason: {entry['reason']}")
            if entry["legal_reference"]:
                lines.append(f"   Legal Basis: {entry['legal_reference']}")
        return "\n".join(lines)


class RTIApplicationGenerator(AdvancedDocumentEngine):
    """Advanced RTI Application Generator with jurisdiction awareness and clause logging."""

    def generate(
        self,
        user_data: Dict[str, Any],
        output_path: str,
    ) -> Tuple[str, Dict[str, Any]]:
        """Generate a jurisdiction-specific RTI Application PDF.

        Args:
            user_data: Dictionary containing applicant details. Required keys:
                name, address, state, authority, pio_address, info, etc.
            output_path: Filesystem path for the generated PDF.

        Returns:
            Tuple of (document_hash, deadlines_dict).
        """
        state = user_data["state"]
        jurisdiction = self.jurisdiction_mgr.get_jurisdiction(state)
        rti_rules = jurisdiction["rti_rules"]

        detected_categories = self.jurisdiction_mgr.detect_rti_category(
            user_data["info"]
        )

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=2.5 * cm,
            bottomMargin=2.5 * cm,
            title=f"RTI Application - {user_data['name']}",
        )

        story: List[Any] = []

        story.append(
            Paragraph(
                "APPLICATION UNDER THE RIGHT TO INFORMATION ACT, 2005",
                self.styles["DocTitle"],
            )
        )
        story.append(Spacer(1, 0.4 * inch))

        pio_designation = rti_rules["pio_designation"]
        to_address = (
            "<b>To,</b><br/>"
            f"The {pio_designation},<br/>"
            f"{user_data['authority']},<br/>"
            f"{user_data['pio_address']}"
        )
        story.append(Paragraph(to_address, self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.3 * inch))

        if user_data.get("reference_number"):
            story.append(
                Paragraph(
                    f"<b>Ref No.:</b> {user_data['reference_number']}",
                    self.styles["BodyJustify"],
                )
            )
            story.append(Spacer(1, 0.15 * inch))

        subject_text = self._generate_specific_subject(user_data["info"])
        story.append(
            Paragraph(
                f"<b>Subject:</b> {subject_text}",
                self.styles["Subject"],
            )
        )
        story.append(Spacer(1, 0.25 * inch))

        story.append(
            Paragraph("Respected Sir/Madam,", self.styles["BodyJustify"])
        )
        story.append(Spacer(1, 0.2 * inch))

        intro_text = self._generate_contextual_intro(user_data, jurisdiction)
        story.append(Paragraph(intro_text, self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.2 * inch))

        story.append(
            Paragraph(
                "<b>INFORMATION SOUGHT:</b>",
                self.styles["Subject"],
            )
        )
        story.append(Spacer(1, 0.1 * inch))

        info_paragraphs = self._format_information_requests(user_data["info"])
        for para in info_paragraphs:
            story.append(Paragraph(para, self.styles["BodyJustify"]))
            story.append(Spacer(1, 0.1 * inch))

        story.append(Spacer(1, 0.15 * inch))

        if detected_categories:
            self._add_category_clauses(detected_categories, story)

        fee_text = self._generate_fee_clause(user_data, rti_rules)
        story.append(Paragraph(fee_text, self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.15 * inch))

        self.log_clause_explanation(
            "Fee Clause",
            f"State-specific fee rules applied for {state}",
            f"{state} RTI Rules",
        )

        format_pref = user_data.get("format_preference", "electronic/physical")
        story.append(
            Paragraph(
                f"I request that the information be provided in "
                f"<b>{format_pref}</b> format as per my convenience.",
                self.styles["BodyJustify"],
            )
        )
        story.append(Spacer(1, 0.15 * inch))

        story.append(
            Paragraph(
                "If any portion of the requested information is exempt from "
                "disclosure, I request that the remaining non-exempt portions "
                "be provided separately as per Section 10 of the RTI Act, 2005.",
                self.styles["BodyJustify"],
            )
        )
        story.append(Spacer(1, 0.15 * inch))

        self.log_clause_explanation(
            "Severability Clause",
            "Added to ensure partial information is disclosed even if some parts are exempt",
            "Section 10, RTI Act 2005",
        )

        story.append(
            Paragraph(
                "I hereby declare that the information sought does not fall "
                "within the restricted categories under Sections 8 and 9 of "
                "the RTI Act, 2005, to the best of my knowledge and belief.",
                self.styles["BodyJustify"],
            )
        )
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Thanking you,", self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.1 * inch))
        story.append(
            Paragraph("Yours faithfully,", self.styles["BodyJustify"])
        )
        story.append(Spacer(1, 0.6 * inch))

        sig_date = datetime.now().strftime("%d/%m/%Y")
        signature_data: List[List[str]] = [
            ["Place: _____________________", ""],
            [f"Date: {sig_date}", ""],
            ["", ""],
            ["", "(Signature of Applicant)"],
            ["", ""],
            [f"<b>Name:</b> {user_data['name']}", ""],
            [f"<b>Address:</b> {user_data['address']}", ""],
        ]

        if user_data.get("contact"):
            signature_data.append(
                [f"<b>Contact:</b> {user_data['contact']}", ""]
            )
        if user_data.get("email"):
            signature_data.append(
                [f"<b>Email:</b> {user_data['email']}", ""]
            )

        sig_table = Table(
            signature_data, colWidths=[3.2 * inch, 2.8 * inch]
        )
        sig_table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), "Times-Roman", 11),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (1, 3), (1, 3), "CENTER"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        story.append(sig_table)

        doc.build(story)

        with open(output_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        metadata: Dict[str, Any] = {
            "applicant_name": user_data["name"],
            "authority": user_data["authority"],
            "state": state,
            "detected_categories": detected_categories,
            "jurisdiction": state,
        }
        deadlines = self.lifecycle_mgr.create_lifecycle(
            file_hash, "RTI_Application", metadata
        )

        logger.info(
            "RTI Application generated: %s | hash=%s",
            output_path,
            file_hash[:16],
        )
        return file_hash, deadlines

    def _generate_specific_subject(self, info_text: str) -> str:
        """Derive a specific subject line from the information request.

        Args:
            info_text: The body of the information request.

        Returns:
            A context-appropriate subject line.
        """
        preview = info_text[:100].strip().lower()
        if "copy" in preview:
            return "Request for certified copies under RTI Act, 2005"
        if "details" in preview or "information" in preview:
            return "Application seeking information under Section 6(1) of RTI Act, 2005"
        if "list" in preview:
            return "Request for list/details under Right to Information Act, 2005"
        return "Application for information under Section 6(1) of RTI Act, 2005"

    def _generate_contextual_intro(
        self,
        user_data: Dict[str, Any],
        jurisdiction: Dict[str, Any],
    ) -> str:
        """Generate a context-appropriate introductory paragraph.

        Args:
            user_data: Applicant details.
            jurisdiction: State jurisdiction profile.

        Returns:
            A formatted introductory paragraph.
        """
        variants = [
            f"I, <b>{user_data['name']}</b>, a citizen of India residing at "
            f"<b>{user_data['address']}</b>, hereby submit this application "
            "under Section 6(1) of the Right to Information Act, 2005, "
            "seeking information from your esteemed office as detailed below:",
            f"Respectfully, I, <b>{user_data['name']}</b>, permanent resident "
            f"of <b>{user_data['address']}</b>, do hereby make this application "
            "under the provisions of the Right to Information Act, 2005, "
            "requesting the following information which is under the control "
            "of your office:",
            f"I, <b>{user_data['name']}</b>, residing at "
            f"<b>{user_data['address']}</b>, submit this application in "
            "exercise of my right under Section 6 of the Right to Information "
            "Act, 2005, requesting disclosure of the following information:",
        ]
        variant_index = hash(user_data["name"]) % len(variants)
        return variants[variant_index]

    def _format_information_requests(self, info_text: str) -> List[str]:
        """Format raw information request text into numbered paragraphs.

        Args:
            info_text: Unstructured information request text.

        Returns:
            List of formatted request strings.
        """
        raw_requests = [
            s.strip()
            for s in info_text.replace("\n", ". ").split(".")
            if s.strip()
        ]
        formatted: List[str] = []
        for i, request in enumerate(raw_requests, 1):
            request = request.strip()
            if not request:
                continue
            if request[0].isupper() and i > 1:
                request = request[0].lower() + request[1:]
            formatted.append(f"{i}. {request.capitalize() if i == 1 else request};")
        if formatted:
            formatted[-1] = formatted[-1].rstrip(";") + "."
        return formatted

    def _add_category_clauses(
        self,
        categories: List[str],
        story: List[Any],
    ) -> None:
        """Add category-specific warnings and additional clauses to the document.

        Args:
            categories: List of detected RTI category keys.
            story: The reportlab story list to append to.
        """
        for category in categories:
            cat_info = self.jurisdiction_mgr.get_category_info(category)
            if not cat_info:
                continue

            if cat_info.get("warnings"):
                story.append(Spacer(1, 0.15 * inch))
                warning_text = "<b>Note:</b> " + cat_info["warnings"][0]
                story.append(
                    Paragraph(warning_text, self.styles["BodyJustify"])
                )
                self.log_clause_explanation(
                    f'{cat_info["name"]} Warning',
                    f"Auto-detected category: {category}",
                    cat_info.get("exemption_reference", ""),
                )

            if cat_info.get("additional_clauses"):
                for clause_key in cat_info["additional_clauses"]:
                    clause_data = self.jurisdiction_mgr.get_additional_clause(
                        clause_key
                    )
                    if clause_data:
                        story.append(Spacer(1, 0.15 * inch))
                        story.append(
                            Paragraph(
                                clause_data["text"],
                                self.styles["BodyJustify"],
                            )
                        )
                        self.log_clause_explanation(
                            clause_key,
                            f'Required for {cat_info["name"]} requests',
                            clause_data.get("legal_reference", ""),
                        )

    def _generate_fee_clause(
        self,
        user_data: Dict[str, Any],
        rti_rules: Dict[str, Any],
    ) -> str:
        """Build the fee-payment clause based on jurisdiction and BPL status.

        Args:
            user_data: Applicant form data.
            rti_rules: State-specific RTI fee rules.

        Returns:
            HTML-formatted fee clause string.
        """
        if user_data.get("bpl") and rti_rules.get("bpl_exemption"):
            bpl_card = user_data.get("bpl_card_number", "[To be provided]")
            return (
                f"Being a holder of Below Poverty Line (BPL) card, I am "
                f"exempted from payment of the application fee as per the "
                f"provisions of the RTI Act, 2005. My BPL Card Number is "
                f"<b>{bpl_card}</b>."
            )
        fee = rti_rules["fee"]
        payment_modes = " / ".join(rti_rules["payment_modes"])
        return (
            f"I am submitting the prescribed application fee of "
            f"<b>Rs. {fee}/-</b> (Rupees {self._amount_in_words(fee)} only) "
            f"through {payment_modes} as per the RTI Rules applicable in "
            f"{user_data['state']}."
        )

    @staticmethod
    def _amount_in_words(amount: int) -> str:
        """Convert common fee amounts to words.

        Args:
            amount: Numeric fee value.

        Returns:
            Amount in words, or the raw string for uncommon values.
        """
        words: Dict[int, str] = {
            10: "Ten",
            20: "Twenty",
            30: "Thirty",
            50: "Fifty",
            100: "One Hundred",
            200: "Two Hundred",
            500: "Five Hundred",
        }
        return words.get(amount, str(amount))

    def generate_first_appeal(
        self,
        original_rti_data: Dict[str, Any],
        appeal_reason: str,
        output_path: str,
    ) -> str:
        """Auto-generate a First Appeal PDF from the original RTI data.

        Args:
            original_rti_data: The data dictionary from the original RTI application.
            appeal_reason: Text describing why the appeal is being filed.
            output_path: Filesystem path for the generated PDF.

        Returns:
            SHA-256 document hash.
        """
        state = original_rti_data["state"]
        jurisdiction = self.jurisdiction_mgr.get_jurisdiction(state)
        rti_rules = jurisdiction["rti_rules"]

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=2.5 * cm,
            bottomMargin=2.5 * cm,
            title=f"RTI First Appeal - {original_rti_data['name']}",
        )

        story: List[Any] = []

        story.append(
            Paragraph(
                "FIRST APPEAL UNDER SECTION 19(1) OF THE RIGHT TO INFORMATION ACT, 2005",
                self.styles["DocTitle"],
            )
        )
        story.append(Spacer(1, 0.4 * inch))

        appellate_designation = rti_rules["appellate_designation"]
        to_address = (
            "<b>To,</b><br/>"
            f"The {appellate_designation},<br/>"
            f"{original_rti_data['authority']},<br/>"
            f"{original_rti_data['pio_address']}"
        )
        story.append(Paragraph(to_address, self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.3 * inch))

        story.append(
            Paragraph(
                "<b>Subject:</b> First Appeal under Section 19(1) of the "
                "RTI Act, 2005 against the decision/non-decision of the "
                "Public Information Officer",
                self.styles["Subject"],
            )
        )
        story.append(Spacer(1, 0.25 * inch))

        story.append(
            Paragraph("Respected Sir/Madam,", self.styles["BodyJustify"])
        )
        story.append(Spacer(1, 0.2 * inch))

        appeal_intro = (
            f"I, <b>{original_rti_data['name']}</b>, had filed an RTI "
            f"application dated <b>{original_rti_data.get('application_date', '____')}</b> "
            f"with the Public Information Officer of your office. The "
            f"application sought specific information as detailed below. "
            f"However, {appeal_reason}. Therefore, I am filing this First "
            "Appeal under Section 19(1) of the RTI Act, 2005."
        )
        story.append(Paragraph(appeal_intro, self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.2 * inch))

        story.append(
            Paragraph(
                "<b>ORIGINAL INFORMATION REQUESTED:</b>",
                self.styles["Subject"],
            )
        )
        story.append(Spacer(1, 0.1 * inch))

        info_paragraphs = self._format_information_requests(
            original_rti_data["info"]
        )
        for para in info_paragraphs:
            story.append(Paragraph(para, self.styles["BodyJustify"]))

        story.append(Spacer(1, 0.2 * inch))

        story.append(
            Paragraph(
                "<b>GROUNDS OF APPEAL:</b>",
                self.styles["Subject"],
            )
        )
        story.append(Spacer(1, 0.1 * inch))

        grounds: List[str] = [
            "The Public Information Officer has failed to provide information "
            "within the stipulated period of 30 days as mandated under "
            "Section 7(1) of the RTI Act, 2005.",
            "The information requested is not exempt under any provisions "
            "of Section 8 or Section 9 of the Act.",
            "The delay/refusal has caused undue hardship and is contrary to "
            "the spirit of transparency enshrined in the RTI Act, 2005.",
        ]
        for i, ground in enumerate(grounds, 1):
            story.append(
                Paragraph(f"{i}. {ground}", self.styles["BodyJustify"])
            )
            story.append(Spacer(1, 0.08 * inch))

        story.append(Spacer(1, 0.2 * inch))

        story.append(
            Paragraph("<b>PRAYER:</b>", self.styles["Subject"])
        )
        story.append(Spacer(1, 0.1 * inch))

        prayer = (
            "In light of the above, I humbly pray that this Hon'ble "
            "Appellate Authority may be pleased to direct the Public "
            "Information Officer to provide the requested information at "
            "the earliest and impose appropriate penalties for the delay "
            "as per Section 20 of the RTI Act, 2005."
        )
        story.append(Paragraph(prayer, self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.3 * inch))

        story.append(Paragraph("Thanking you,", self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.1 * inch))
        story.append(
            Paragraph("Yours faithfully,", self.styles["BodyJustify"])
        )
        story.append(Spacer(1, 0.6 * inch))

        sig_date = datetime.now().strftime("%d/%m/%Y")
        signature_data: List[List[str]] = [
            ["Place: _____________________", ""],
            [f"Date: {sig_date}", ""],
            ["", ""],
            ["", "(Signature of Appellant)"],
            ["", ""],
            [f"<b>Name:</b> {original_rti_data['name']}", ""],
            [f"<b>Address:</b> {original_rti_data['address']}", ""],
        ]
        if original_rti_data.get("contact"):
            signature_data.append(
                [f"<b>Contact:</b> {original_rti_data['contact']}", ""]
            )

        sig_table = Table(
            signature_data, colWidths=[3.2 * inch, 2.8 * inch]
        )
        sig_table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), "Times-Roman", 11),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (1, 3), (1, 3), "CENTER"),
                ]
            )
        )
        story.append(sig_table)

        doc.build(story)

        with open(output_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        logger.info(
            "First Appeal generated: %s | hash=%s",
            output_path,
            file_hash[:16],
        )
        return file_hash


class AffidavitGenerator(AdvancedDocumentEngine):
    """Generate jurisdiction-specific affidavits with stamp paper, guardian, and notary logic."""

    def generate(
        self,
        user_data: Dict[str, Any],
        output_path: str,
    ) -> str:
        """Generate a jurisdiction-specific Affidavit PDF.

        Args:
            user_data: Dictionary containing deponent details. Required keys:
                deponent_name, age, address, statements. Optional: state, gender,
                father_name, guardian_name, guardian_age, guardian_father_name.
            output_path: Filesystem path for the generated PDF.

        Returns:
            SHA-256 document hash.
        """
        state = user_data.get("state", "Maharashtra")
        jurisdiction = self.jurisdiction_mgr.get_jurisdiction(state)
        affidavit_rules = jurisdiction["affidavit_rules"]

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=3 * cm,
            bottomMargin=2.5 * cm,
            title=f"Affidavit - {user_data['deponent_name']}",
        )

        story: List[Any] = []

        if affidavit_rules["stamp_mandatory"]:
            stamp_note = (
                f"<font size=9><i>To be executed on Non-Judicial Stamp Paper "
                f"of Rs. {affidavit_rules['stamp_paper_value']}/- as per "
                f"{state} Stamp Act</i></font>"
            )
            story.append(Paragraph(stamp_note, self.styles["BodyJustify"]))
            story.append(Spacer(1, 0.3 * inch))

            self.log_clause_explanation(
                "Stamp Paper Requirement",
                f"{state} requires stamp paper of "
                f"Rs. {affidavit_rules['stamp_paper_value']}",
                f"{state} Stamp Act",
            )

        story.append(Paragraph("AFFIDAVIT", self.styles["DocTitle"]))
        story.append(Spacer(1, 0.3 * inch))

        age = int(user_data["age"])
        guardian_required = age < affidavit_rules["guardian_age_limit"]

        if guardian_required:
            deponent_intro = (
                f"I, <b>{user_data['guardian_name']}</b>, aged "
                f"<b>{user_data['guardian_age']} years</b>, "
                f"son/daughter/wife of <b>{user_data['guardian_father_name']}</b>, "
                f"resident of <b>{user_data['address']}</b>, being the lawful "
                f"guardian of <b>{user_data['deponent_name']}</b>, a minor aged "
                f"<b>{age} years</b>, do hereby solemnly affirm and state on "
                "oath as under:"
            )
            self.log_clause_explanation(
                "Guardian Declaration",
                f"Deponent is minor (age {age}), guardian declaration "
                f"added as per {state} law",
                f"{state} Majority Act / Indian Contract Act",
            )
        else:
            relation = self._determine_relation(
                user_data.get("gender", "male")
            )
            deponent_intro = (
                f"I, <b>{user_data['deponent_name']}</b>, aged "
                f"<b>{age} years</b>, {relation} "
                f"<b>{user_data['father_name']}</b>, resident of "
                f"<b>{user_data['address']}</b>, do hereby solemnly affirm "
                "and state on oath as under:"
            )

        story.append(
            Paragraph(deponent_intro, self.styles["BodyJustify"])
        )
        story.append(Spacer(1, 0.25 * inch))

        statements = user_data["statements"]
        for i, statement in enumerate(statements, 1):
            if not statement.lower().strip().startswith("that"):
                statement = f"that {statement}"
            story.append(
                Paragraph(
                    f"<b>{i}.</b> {statement.capitalize()};",
                    self.styles["BodyJustify"],
                )
            )
            story.append(Spacer(1, 0.12 * inch))

        story.append(Spacer(1, 0.2 * inch))

        verification_format = affidavit_rules["verification_format"]
        if verification_format == "magistrate_court":
            verification = (
                f"I, the above-named deponent, do hereby verify and state on "
                f"solemn affirmation that the contents of paragraphs 1 to "
                f"{len(statements)} stated hereinabove are true and correct "
                "to the best of my knowledge and belief, and nothing material "
                "has been concealed therefrom. I further state that no part "
                "of this affidavit is false and nothing has been concealed herein."
            )
        else:
            verification = (
                f"Verified at _____________ on this _____ day of "
                f"_____________ {datetime.now().year}. I, the deponent "
                "above-named, do hereby verify that the contents of this "
                "affidavit are true to the best of my knowledge and belief."
            )

        story.append(Paragraph(verification, self.styles["BodyJustify"]))
        story.append(Spacer(1, 0.4 * inch))

        story.append(Paragraph("DEPONENT", self.styles["RightAlign"]))
        story.append(Spacer(1, 1 * inch))

        court_designation = affidavit_rules["court_designation"]

        story.append(
            Paragraph(
                f"<b>VERIFICATION BY {court_designation.upper()}/"
                "NOTARY PUBLIC/OATH COMMISSIONER</b>",
                self.styles["Subject"],
            )
        )
        story.append(Spacer(1, 0.2 * inch))

        if affidavit_rules.get("witness_required"):
            witness_text = (
                "Identified by me / Identified by _________________________ "
                "(Witness Name & Address)"
            )
            self.log_clause_explanation(
                "Witness Requirement",
                f"{state} requires witness identification for affidavits",
                f"{state} Court Rules",
            )
        else:
            witness_text = "Identified by me"

        notary_block = (
            f"{witness_text}<br/>"
            "<br/>"
            "<b>Signature:</b> _____________________<br/>"
            "<b>Name:</b> _________________________<br/>"
            f"<b>Designation:</b> {court_designation}/"
            "Notary Public/Oath Commissioner<br/>"
            "<b>Registration No.:</b> ______________<br/>"
            "<b>Seal:</b><br/>"
            "<br/>"
            "<br/>"
        )
        story.append(Paragraph(notary_block, self.styles["BodyJustify"]))

        doc.build(story)

        with open(output_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        metadata: Dict[str, Any] = {
            "deponent_name": user_data["deponent_name"],
            "state": state,
            "stamp_value": affidavit_rules["stamp_paper_value"],
            "guardian_required": guardian_required,
        }
        self.lifecycle_mgr.create_lifecycle(file_hash, "Affidavit", metadata)

        logger.info(
            "Affidavit generated: %s | hash=%s",
            output_path,
            file_hash[:16],
        )
        return file_hash

    @staticmethod
    def _determine_relation(gender: str) -> str:
        """Return the correct relation descriptor based on gender.

        Args:
            gender: 'male', 'female', or other.

        Returns:
            'son of' or 'daughter/wife of'.
        """
        return "daughter/wife of" if gender.lower() == "female" else "son of"
