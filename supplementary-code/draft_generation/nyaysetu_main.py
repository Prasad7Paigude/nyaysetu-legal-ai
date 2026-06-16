#!/usr/bin/env python3
"""
NyaySetu - Advanced Legal Document Generation System (CLI Edition).

Features:
- Jurisdiction-aware document generation
- Smart legal validation prevents invalid documents
- Document lifecycle tracking with automatic deadlines
- RTI auto-appeal generation
- Explainable AI - shows why clauses were added
- Category-based compliance checking
"""

import glob
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from config.settings import DRAFT_GEN_DIR
from utils.logging_setup import setup_logging

from draft_generation.document_engine import (
    AffidavitGenerator,
    DocumentLifecycle,
    JurisdictionManager,
    RTIApplicationGenerator,
)
from draft_generation.validation import SmartLegalValidator

logger = setup_logging(__name__)


class NyaySetuAdvanced:
    """Advanced NyaySetu CLI application for interactive document generation."""

    def __init__(self) -> None:
        """Initialise validators, managers, and output directory."""
        self.validator: SmartLegalValidator = SmartLegalValidator()
        self.jurisdiction_mgr: JurisdictionManager = JurisdictionManager()
        self.lifecycle_mgr: DocumentLifecycle = DocumentLifecycle()
        self.output_dir: str = str(DRAFT_GEN_DIR / "generated_documents")
        os.makedirs(self.output_dir, exist_ok=True)
        self.user_id: Optional[str] = None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen (platform-aware)."""
        os.system("clear" if os.name != "nt" else "cls")

    def print_header(self) -> None:
        """Log the application header banner."""
        logger.info("=" * 75)
        logger.info("%sNYAYSETU%s", " " * 22, " " * 22)
        logger.info("%sAdvanced Legal Document Generation System", " " * 12)
        logger.info("%sNational Hackathon Edition", " " * 18)
        logger.info("=" * 75)
        logger.info("")

    def print_menu(self) -> None:
        """Log the main menu options."""
        logger.info("")
        logger.info("MAIN MENU")
        logger.info("=" * 75)
        logger.info("DOCUMENT GENERATION:")
        logger.info("  1. Generate RTI Application (Jurisdiction-Aware)")
        logger.info("  2. Generate Affidavit (State-Specific Format)")
        logger.info("")
        logger.info("RTI LIFECYCLE MANAGEMENT:")
        logger.info("  3. Generate First Appeal (Auto from Original RTI)")
        logger.info("  4. View Document Lifecycle & Deadlines")
        logger.info("  5. Update Document Status")
        logger.info("")
        logger.info("DOCUMENT INTELLIGENCE:")
        logger.info("  6. View Document Generation Explanation")
        logger.info("  7. Check Legal Compliance (Before Filing)")
        logger.info("")
        logger.info("  8. Exit")
        logger.info("=" * 75)

    def get_user_session(self) -> None:
        """Prompt for or create a user session."""
        if self.user_id:
            return
        logger.info("")
        logger.info("User Authentication")
        logger.info("-" * 75)
        user_id = input("Enter your User ID (or press Enter for new): ").strip()
        if not user_id:
            user_id = f"USER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            logger.info("Created User ID: %s", user_id)
        self.user_id = user_id
        logger.info("Session: %s", self.user_id)
        logger.info("")

    # ------------------------------------------------------------------
    # Document Generation
    # ------------------------------------------------------------------

    def generate_rti(self) -> None:
        """Interactive RTI application generation with validation and compliance check."""
        self.clear_screen()
        self.print_header()
        logger.info("ADVANCED RTI APPLICATION GENERATOR")
        logger.info("=" * 75)
        logger.info("This system:")
        logger.info("  - Validates legal compliance BEFORE generation")
        logger.info("  - Auto-detects Section 8 exemptions")
        logger.info("  - Applies state-specific legal rules")
        logger.info("  - Tracks deadlines automatically")
        logger.info("  - Explains why each clause was added")
        logger.info("=" * 75)
        logger.info("")

        user_data: Dict[str, Any] = {}

        logger.info("STEP 1: APPLICANT DETAILS")
        logger.info("-" * 75)
        user_data["name"] = input("Full Name (as per ID proof): ").strip()
        user_data["address"] = input(
            "Complete Address (House, Street, City, PIN): "
        ).strip()

        logger.info("")
        logger.info("Select State/UT:")
        states = list(self.jurisdiction_mgr.profiles.keys())
        for i, state in enumerate(states, 1):
            logger.info("  %s. %s", i, state)

        state_input = input("\nEnter number or state name: ").strip()
        if state_input.isdigit() and 1 <= int(state_input) <= len(states):
            user_data["state"] = states[int(state_input) - 1]
        else:
            user_data["state"] = state_input

        if user_data["state"] in self.jurisdiction_mgr.profiles:
            jurisdiction = self.jurisdiction_mgr.profiles[user_data["state"]]
            rti_rules = jurisdiction["rti_rules"]
            logger.info(
                "Loaded jurisdiction rules for %s:", user_data["state"]
            )
            logger.info(
                "   - Application Fee: Rs. %s/-", rti_rules["fee"]
            )
            logger.info(
                "   - Payment Modes: %s",
                ", ".join(rti_rules["payment_modes"]),
            )
            logger.info(
                "   - BPL Exemption: %s",
                "Yes" if rti_rules["bpl_exemption"] else "No",
            )

        user_data["contact"] = input("\nMobile Number or Email: ").strip()
        user_data["email"] = input("Email (optional): ").strip()

        logger.info("")
        logger.info("STEP 2: PUBLIC AUTHORITY DETAILS")
        logger.info("-" * 75)
        user_data["authority"] = input(
            "Public Authority/Department Full Name: "
        ).strip()
        user_data["pio_address"] = input(
            "Complete Address of PIO Office: "
        ).strip()
        user_data["reference_number"] = input(
            "Reference Number (if any, optional): "
        ).strip()

        logger.info("")
        logger.info("STEP 3: INFORMATION REQUESTED")
        logger.info("-" * 75)
        logger.info("TIP: Be specific! Include:")
        logger.info("   - Exact document names or file numbers")
        logger.info("   - Time period (from X date to Y date)")
        logger.info("   - Department/section if known")
        logger.info("")
        logger.info("Enter your information request (Press Enter twice when done):")
        logger.info("")

        info_lines: List[str] = []
        empty_count = 0
        while True:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                info_lines.append(line)
        user_data["info"] = "\n".join(info_lines)

        logger.info("")
        logger.info("STEP 4: FEE PAYMENT")
        logger.info("-" * 75)
        bpl_input = input(
            "Do you have a BPL card? (yes/no): "
        ).strip().lower()
        user_data["bpl"] = bpl_input in ("yes", "y")
        if user_data["bpl"]:
            user_data["bpl_card_number"] = input(
                "BPL Card Number: "
            ).strip()

        logger.info("")
        logger.info("Preferred information format:")
        logger.info("  1. Electronic (PDF/Digital)")
        logger.info("  2. Physical (Printed copies)")
        logger.info("  3. Both")

        format_choice = input("Select (1-3): ").strip()
        format_map: Dict[str, str] = {
            "1": "electronic",
            "2": "physical",
            "3": "electronic and physical",
        }
        user_data["format_preference"] = format_map.get(
            format_choice, "electronic/physical"
        )

        logger.info("")
        logger.info("=" * 75)
        logger.info("PHASE 1: SMART LEGAL VALIDATION")
        logger.info("=" * 75)

        if not self.validator.validate_rti_application(user_data):
            logger.info("\n%s", self.validator.get_validation_report())

            if self.validator.has_blocking_issues():
                logger.info(
                    "GENERATION BLOCKED: Critical issues must be resolved first."
                )
                retry = input(
                    "\nFix issues and retry? (yes/no): "
                ).strip().lower()
                if retry in ("yes", "y"):
                    return self.generate_rti()
                input("\nPress Enter to return to menu...")
                return
            proceed = input(
                "\nWarnings found. Proceed anyway? (yes/no): "
            ).strip().lower()
            if proceed not in ("yes", "y"):
                return
        else:
            logger.info("Validation passed!")

        if self.validator.warnings or self.validator.suggestions:
            logger.info("\n%s", self.validator.get_validation_report())
            input("\nPress Enter to continue...")

        logger.info("")
        logger.info("=" * 75)
        logger.info("PHASE 2: SECTION 8 COMPLIANCE CHECK")
        logger.info("=" * 75)

        detected_categories = self.jurisdiction_mgr.detect_rti_category(
            user_data["info"]
        )

        if detected_categories:
            logger.info(
                "Detected %s information category/categories:",
                len(detected_categories),
            )
            for cat in detected_categories:
                cat_info = self.jurisdiction_mgr.get_category_info(cat)
                logger.info("  - %s", cat_info.get("name", cat))
                if cat_info.get("section_8_exempt"):
                    logger.info(
                        "    Exemption: %s",
                        cat_info.get("exemption_reference"),
                    )
                    logger.info(
                        "    Info: %s",
                        cat_info.get(
                            "processing_notes",
                            "May be partially exempt",
                        ),
                    )
                else:
                    logger.info("    Generally not exempt")

            logger.info(
                "These categories will trigger appropriate legal clauses "
                "in your application"
            )

            modify = input(
                "\nDo you want to modify your request? (yes/no): "
            ).strip().lower()
            if modify in ("yes", "y"):
                logger.info(
                    "\nEnter modified information request "
                    "(Press Enter twice when done):"
                )
                info_lines = []
                empty_count = 0
                while True:
                    line = input()
                    if line.strip() == "":
                        empty_count += 1
                        if empty_count >= 2:
                            break
                    else:
                        empty_count = 0
                        info_lines.append(line)
                user_data["info"] = "\n".join(info_lines)
        else:
            logger.info(
                "No Section 8 exemptions detected. Request appears compliant."
            )

        logger.info("")
        logger.info("=" * 75)
        logger.info("PHASE 3: DOCUMENT GENERATION")
        logger.info("=" * 75)

        generator = RTIApplicationGenerator()
        filename = (
            f"RTI_Application_"
            f"{user_data['name'].replace(' ', '_')}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        output_path = os.path.join(self.output_dir, filename)

        try:
            logger.info("Generating jurisdiction-specific RTI application...")
            user_data["application_date"] = datetime.now().strftime(
                "%Y-%m-%d"
            )

            doc_hash, deadlines = generator.generate(user_data, output_path)

            logger.info("DOCUMENT GENERATED SUCCESSFULLY!")
            logger.info("=" * 75)
            logger.info("Filename: %s", filename)
            logger.info("Location: %s", output_path)
            logger.info("Size: %s bytes", os.path.getsize(output_path))
            logger.info("Document Hash: %s", doc_hash)

            logger.info("")
            logger.info("=" * 75)
            logger.info("DOCUMENT GENERATION EXPLANATION")
            logger.info("=" * 75)
            logger.info(generator.generate_explanation_report())

            if deadlines:
                logger.info("")
                logger.info("=" * 75)
                logger.info("AUTOMATIC DEADLINE TRACKING")
                logger.info("=" * 75)
                logger.info(
                    "Reply Deadline: %s",
                    deadlines.get("reply_deadline", "N/A")[:10],
                )
                logger.info(
                    "  (%s days from submission)",
                    deadlines.get("reply_deadline_days", 0),
                )
                logger.info(
                    "Appeal Deadline: %s",
                    deadlines.get("first_appeal_deadline", "N/A")[:10],
                )
                logger.info(
                    "  (%s days from reply)",
                    deadlines.get("first_appeal_days", 0),
                )
                logger.info(
                    "Info: %s", deadlines.get("description", "")
                )

            rti_data_file = output_path.replace(".pdf", "_data.json")
            with open(rti_data_file, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=2)

            logger.info("")
            logger.info("=" * 75)
            logger.info("NEXT STEPS")
            logger.info("=" * 75)
            logger.info("1. Print the generated PDF")
            logger.info("2. Sign at the designated place")
            logger.info(
                "3. Attach fee of Rs. %s/-",
                self.jurisdiction_mgr.get_jurisdiction(
                    user_data["state"]
                )["rti_rules"]["fee"],
            )
            logger.info("   (unless BPL exemption applies)")
            logger.info("4. Submit to the Public Information Officer")
            logger.info("5. Keep a copy for your records")
            logger.info("")
            logger.info(
                "Track your deadlines using option 4 in main menu"
            )
            logger.info(
                "If no reply in 30 days, generate First Appeal using option 3"
            )

        except Exception as exc:
            logger.error("Error: %s", exc)
            import traceback

            traceback.print_exc()

        input("\n\nPress Enter to return to main menu...")

    def generate_affidavit(self) -> None:
        """Interactive affidavit generation with jurisdiction-specific rules."""
        self.clear_screen()
        self.print_header()
        logger.info("ADVANCED AFFIDAVIT GENERATOR")
        logger.info("=" * 75)
        logger.info("This system:")
        logger.info("  - Checks age for guardian requirement")
        logger.info("  - Applies state-specific stamp rules")
        logger.info("  - Uses correct court designations")
        logger.info("  - Validates statement quality")
        logger.info("=" * 75)
        logger.info("")

        user_data: Dict[str, Any] = {}

        logger.info("STEP 1: DEPONENT DETAILS")
        logger.info("-" * 75)
        user_data["deponent_name"] = input(
            "Full Name of Deponent: "
        ).strip()
        user_data["age"] = input("Age: ").strip()

        try:
            age_int = int(user_data["age"])
            if age_int < 18:
                logger.info(
                    "Deponent is minor (age %s). Guardian details required!",
                    age_int,
                )
                logger.info("-" * 75)
                user_data["guardian_name"] = input(
                    "Guardian's Full Name: "
                ).strip()
                user_data["guardian_age"] = input(
                    "Guardian's Age: "
                ).strip()
                user_data["guardian_father_name"] = input(
                    "Guardian's Father's Name: "
                ).strip()
        except (ValueError, TypeError):
            pass

        user_data["father_name"] = input(
            "Father's/Husband's Name (of Deponent): "
        ).strip()
        user_data["gender"] = input("Gender (male/female): ").strip()
        user_data["address"] = input("Complete Address: ").strip()

        logger.info("")
        logger.info("Select State (for stamp paper rules):")
        states = list(self.jurisdiction_mgr.profiles.keys())
        for i, state in enumerate(states, 1):
            logger.info("  %s. %s", i, state)

        state_input = input("\nEnter number or state name: ").strip()
        if state_input.isdigit() and 1 <= int(state_input) <= len(states):
            user_data["state"] = states[int(state_input) - 1]
        else:
            user_data["state"] = state_input

        if user_data["state"] in self.jurisdiction_mgr.profiles:
            jurisdiction = self.jurisdiction_mgr.profiles[user_data["state"]]
            affidavit_rules = jurisdiction["affidavit_rules"]
            logger.info(
                "%s Affidavit Rules:", user_data["state"]
            )
            logger.info(
                "   - Stamp Paper Value: Rs. %s/-",
                affidavit_rules["stamp_paper_value"],
            )
            logger.info(
                "   - Notary Required: %s",
                "Yes" if affidavit_rules["notary_required"] else "No",
            )
            logger.info(
                "   - Court Designation: %s",
                affidavit_rules["court_designation"],
            )

        logger.info("")
        logger.info("STEP 2: AFFIDAVIT STATEMENTS")
        logger.info("-" * 75)
        logger.info("TIP: Each statement should:")
        logger.info("   - State facts, not opinions")
        logger.info("   - Be based on direct knowledge")
        logger.info("   - Start with 'that' (auto-added if missing)")
        logger.info("")
        logger.info("Enter each statement (type 'DONE' when finished):")
        logger.info("")

        statements: List[str] = []
        i = 1
        while True:
            statement = input(f"Statement {i}: ").strip()
            if statement.upper() == "DONE":
                break
            if statement:
                statements.append(statement)
                i += 1
        user_data["statements"] = statements

        logger.info("")
        logger.info("=" * 75)
        logger.info("SMART LEGAL VALIDATION")
        logger.info("=" * 75)

        if not self.validator.validate_affidavit(user_data):
            logger.info("\n%s", self.validator.get_validation_report())

            if self.validator.has_blocking_issues():
                logger.info(
                    "GENERATION BLOCKED: Must fix critical issues."
                )
                retry = input(
                    "\nRetry? (yes/no): "
                ).strip().lower()
                if retry in ("yes", "y"):
                    return self.generate_affidavit()
                input("\nPress Enter to return...")
                return
            proceed = input(
                "\nProceed with warnings? (yes/no): "
            ).strip().lower()
            if proceed not in ("yes", "y"):
                return
        else:
            logger.info("Validation passed!")

        if self.validator.suggestions:
            logger.info("\n%s", self.validator.get_validation_report())
            input("\nPress Enter to continue...")

        logger.info("")
        logger.info("=" * 75)
        logger.info("DOCUMENT GENERATION")
        logger.info("=" * 75)

        generator = AffidavitGenerator()
        filename = (
            f"Affidavit_"
            f"{user_data['deponent_name'].replace(' ', '_')}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        output_path = os.path.join(self.output_dir, filename)

        try:
            logger.info("Generating state-specific affidavit...")

            doc_hash = generator.generate(user_data, output_path)

            logger.info("AFFIDAVIT GENERATED SUCCESSFULLY!")
            logger.info("=" * 75)
            logger.info("Filename: %s", filename)
            logger.info("Location: %s", output_path)
            logger.info("Document Hash: %s", doc_hash)

            logger.info("")
            logger.info("=" * 75)
            logger.info("DOCUMENT GENERATION EXPLANATION")
            logger.info("=" * 75)
            logger.info(generator.generate_explanation_report())

            logger.info("")
            logger.info("=" * 75)
            logger.info("NEXT STEPS")
            logger.info("=" * 75)
            if user_data["state"] in self.jurisdiction_mgr.profiles:
                stamp_value = self.jurisdiction_mgr.profiles[
                    user_data["state"]
                ]["affidavit_rules"]["stamp_paper_value"]
                logger.info(
                    "1. Get Non-Judicial Stamp Paper of Rs. %s/- "
                    "from authorized vendor",
                    stamp_value,
                )
            logger.info("2. Print the affidavit on the stamp paper")
            logger.info("3. Sign in front of Notary Public/Oath Commissioner")
            logger.info("4. Get it notarized with seal")
            logger.info("5. Submit as required")

        except Exception as exc:
            logger.error("Error: %s", exc)
            import traceback

            traceback.print_exc()

        input("\n\nPress Enter to return to main menu...")

    def generate_first_appeal(self) -> None:
        """Auto-generate a First Appeal from a previously generated RTI application."""
        self.clear_screen()
        self.print_header()
        logger.info("AUTOMATIC FIRST APPEAL GENERATOR")
        logger.info("=" * 75)
        logger.info("Generate First Appeal under Section 19(1) of RTI Act")
        logger.info("Uses data from your original RTI application")
        logger.info("=" * 75)
        logger.info("")

        rti_data_files = glob.glob(
            os.path.join(self.output_dir, "RTI_Application_*_data.json")
        )

        if not rti_data_files:
            logger.info(
                "No RTI applications found. Generate an RTI first (Option 1)"
            )
            input("\nPress Enter to continue...")
            return

        logger.info("Found %s RTI application(s):", len(rti_data_files))
        logger.info("")

        for i, file in enumerate(rti_data_files, 1):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(
                "%s. %s - %s", i, data["name"], data["authority"]
            )
            logger.info(
                "   Date: %s", data.get("application_date", "N/A")
            )

        selection = input("\nSelect RTI number for appeal: ").strip()

        try:
            idx = int(selection) - 1
            with open(rti_data_files[idx], "r", encoding="utf-8") as f:
                original_rti = json.load(f)
        except (ValueError, IndexError):
            logger.info("Invalid selection")
            input("Press Enter...")
            return

        logger.info("")
        logger.info("Select reason for appeal:")
        logger.info("1. No reply received within 30 days")
        logger.info("2. Incomplete information provided")
        logger.info("3. Information denied wrongly")
        logger.info("4. Excessive fee demanded")
        logger.info("5. Other (custom reason)")

        reason_choice = input("\nSelect (1-5): ").strip()
        reason_map: Dict[str, str] = {
            "1": "I have not received any response within the statutory period of 30 days",
            "2": "the information provided is incomplete and does not address my specific queries",
            "3": "the information has been wrongly denied citing exemptions that do not apply",
            "4": "excessive fee has been demanded without proper justification",
            "5": "",
        }
        appeal_reason = reason_map.get(reason_choice, reason_map["1"])
        if reason_choice == "5":
            appeal_reason = input("\nEnter custom reason: ").strip()

        logger.info("")
        logger.info("=" * 75)
        logger.info("GENERATING FIRST APPEAL")
        logger.info("=" * 75)

        generator = RTIApplicationGenerator()
        filename = (
            f"RTI_First_Appeal_"
            f"{original_rti['name'].replace(' ', '_')}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        output_path = os.path.join(self.output_dir, filename)

        try:
            logger.info(
                "Auto-generating First Appeal from original RTI data..."
            )

            doc_hash = generator.generate_first_appeal(
                original_rti, appeal_reason, output_path
            )

            logger.info("FIRST APPEAL GENERATED!")
            logger.info("=" * 75)
            logger.info("Filename: %s", filename)
            logger.info("Location: %s", output_path)
            logger.info("Hash: %s", doc_hash)

            logger.info("")
            logger.info("=" * 75)
            logger.info("NEXT STEPS")
            logger.info("=" * 75)
            logger.info("1. Print the generated First Appeal")
            logger.info("2. Sign at designated place")
            logger.info("3. Attach appeal fee (Rs. 50/- typically)")
            logger.info("4. Submit to First Appellate Authority")
            logger.info("5. Keep acknowledgment")
            logger.info("")
            logger.info("Appeal should be decided within 30 days")

        except Exception as exc:
            logger.error("Error: %s", exc)
            import traceback

            traceback.print_exc()

        input("\n\nPress Enter to return...")

    def view_lifecycles(self) -> None:
        """Display pending document deadlines."""
        self.clear_screen()
        self.print_header()
        logger.info("DOCUMENT LIFECYCLE & DEADLINE TRACKER")
        logger.info("=" * 75)

        pending_deadlines = self.lifecycle_mgr.get_pending_deadlines()

        if not pending_deadlines:
            logger.info("No pending deadlines")
        else:
            logger.info(
                "You have %s pending deadline(s):", len(pending_deadlines)
            )
            logger.info("")
            for deadline in pending_deadlines:
                urgency = "URGENT" if deadline["is_urgent"] else ""
                logger.info(
                    "%s %s", urgency, deadline["doc_type"]
                )
                logger.info(
                    "   Hash: %s...", deadline["doc_hash"][:32]
                )
                logger.info(
                    "   Deadline: %s", deadline["deadline_date"][:10]
                )
                logger.info(
                    "   Days Remaining: %s", deadline["days_remaining"]
                )
                logger.info("")

        input("\nPress Enter to return...")

    def update_document_status(self) -> None:
        """Interactively update a document's lifecycle state."""
        self.clear_screen()
        self.print_header()
        logger.info("UPDATE DOCUMENT STATUS")
        logger.info("=" * 75)

        if not self.lifecycle_mgr.lifecycles:
            logger.info("No documents in lifecycle tracker")
            input("Press Enter...")
            return

        logger.info("Active Documents:")
        docs = list(self.lifecycle_mgr.lifecycles.items())

        for i, (doc_hash, lifecycle) in enumerate(docs, 1):
            logger.info("")
            logger.info("%s. %s", i, lifecycle["document_type"])
            logger.info("   Hash: %s...", doc_hash[:32])
            logger.info("   Status: %s", lifecycle["current_state"])
            logger.info(
                "   Created: %s", lifecycle["created_date"][:10]
            )

        selection = input("\nSelect document number: ").strip()

        try:
            idx = int(selection) - 1
            doc_hash, lifecycle = docs[idx]
        except (ValueError, IndexError):
            logger.info("Invalid selection")
            input("Press Enter...")
            return

        logger.info("")
        logger.info("Available States:")
        states = list(DocumentLifecycle.STATES.keys())
        for i, state in enumerate(states, 1):
            logger.info(
                "%s. %s - %s", i, state, DocumentLifecycle.STATES[state]
            )

        state_sel = input("\nSelect new state: ").strip()

        try:
            new_state = states[int(state_sel) - 1]
            notes = input("Notes (optional): ").strip()
            self.lifecycle_mgr.update_state(doc_hash, new_state, notes)
            logger.info("Status updated to: %s", new_state)
        except (ValueError, IndexError):
            logger.info("Invalid selection")

        input("\nPress Enter...")

    def view_explanation(self) -> None:
        """Display information about the explanation feature."""
        self.clear_screen()
        self.print_header()
        logger.info("DOCUMENT GENERATION EXPLANATION")
        logger.info("=" * 75)
        logger.info(
            "This feature shows WHY each clause was added to your document."
        )
        logger.info(
            "It demonstrates the 'Explainable AI' aspect of NyaySetu."
        )
        logger.info("")
        logger.info(
            "(Generate a document first to see explanations)"
        )

        input("\n\nPress Enter...")

    def check_compliance(self) -> None:
        """Pre-filing compliance check for Section 8 exemptions."""
        self.clear_screen()
        self.print_header()
        logger.info("LEGAL COMPLIANCE CHECKER")
        logger.info("=" * 75)
        logger.info(
            "Check RTI application for Section 8 exemptions BEFORE filing"
        )
        logger.info("")

        info = input("Paste your information request:\n\n")

        if not info.strip():
            logger.info("No text entered")
            input("Press Enter...")
            return

        detected = self.jurisdiction_mgr.detect_rti_category(info)

        if not detected:
            logger.info(
                "No obvious Section 8 exemptions detected"
            )
            logger.info("Your request appears compliant!")
        else:
            logger.info(
                "Detected %s potential issue(s):", len(detected)
            )
            logger.info("")
            for cat in detected:
                cat_info = self.jurisdiction_mgr.get_category_info(cat)
                logger.info("  - %s", cat_info.get("name", cat))
                if cat_info.get("section_8_exempt"):
                    logger.info(
                        "    Exemption: %s",
                        cat_info.get("exemption_reference"),
                    )
                    logger.info(
                        "    Note: %s",
                        cat_info.get("processing_notes", ""),
                    )
                logger.info("")

        input("\nPress Enter...")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Run the main CLI application loop."""
        self.clear_screen()
        self.print_header()
        self.get_user_session()

        while True:
            self.print_menu()

            choice = input("\nEnter choice (1-8): ").strip()

            if choice == "1":
                self.generate_rti()
            elif choice == "2":
                self.generate_affidavit()
            elif choice == "3":
                self.generate_first_appeal()
            elif choice == "4":
                self.view_lifecycles()
            elif choice == "5":
                self.update_document_status()
            elif choice == "6":
                self.view_explanation()
            elif choice == "7":
                self.check_compliance()
            elif choice == "8":
                logger.info("Thank you for using NyaySetu!")
                logger.info("=" * 75)
                break
            else:
                logger.info("Invalid choice")
                input("Press Enter...")


if __name__ == "__main__":
    try:
        app = NyaySetuAdvanced()
        app.run()
    except KeyboardInterrupt:
        logger.info("Terminated")
        sys.exit(0)
    except Exception as exc:
        logger.error("Error: %s", exc)
        import traceback

        traceback.print_exc()
        sys.exit(1)
