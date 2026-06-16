"""
RTI Generator Module - Production-ready RTI Application PDF generation.

Generates jurisdiction-compliant RTI Application PDFs with fee clauses,
validation, hashing, and reference numbering.
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config.settings import DATA_DIR, DRAFT_GEN_DIR

logger = logging.getLogger(__name__)


class RTIGenerator:
    """Production-ready RTI document generator with jurisdiction rules."""

    def __init__(self) -> None:
        """Initialize styles and ensure output directory exists."""
        self.styles = self._setup_styles()
        self.output_dir: str = str(DRAFT_GEN_DIR / "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    def _setup_styles(self) -> Any:
        """Set up professional PDF styles for RTI documents.

        Returns:
            ReportLab stylesheet with added DocTitle and DocBody styles.
        """
        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="DocTitle",
                parent=styles["Title"],
                fontSize=14,
                fontName="Times-Bold",
                alignment=TA_CENTER,
                spaceAfter=20,
            )
        )

        styles.add(
            ParagraphStyle(
                name="DocBody",
                parent=styles["Normal"],
                fontSize=11,
                fontName="Times-Roman",
                alignment=TA_JUSTIFY,
                spaceAfter=10,
                leading=16,
            )
        )

        return styles

    def _load_rules(self, state: str) -> Dict[str, Any]:
        """Load jurisdiction rules for a given state.

        Args:
            state: Indian state name.

        Returns:
            Dictionary of jurisdiction rules; falls back to Maharashtra defaults.
        """
        try:
            config_path = DATA_DIR / "jurisdiction_rules.json"
            with open(config_path, "r", encoding="utf-8") as f:
                rules: Dict[str, Any] = json.load(f)
            return rules.get(state, rules.get("Maharashtra", {}))
        except Exception as exc:
            logger.warning("Failed to load jurisdiction_rules.json: %s", exc)
            return {
                "fee": 10,
                "bpl_fee_waiver": True,
                "state_rti_rule": "State RTI Rules, 2005",
            }

    def _validate_request(self, info_text: str) -> Dict[str, Any]:
        """Perform basic validation of an RTI information request.

        Args:
            info_text: The body of the information request.

        Returns:
            Dictionary with keys: is_valid, issues, suggestions, complexity_score.
        """
        issues: List[str] = []
        suggestions: List[str] = []

        if len(info_text.split()) < 10:
            issues.append("Request appears brief - add specific details")
            suggestions.append("Include: dates, file numbers, or document names")

        prohibited = ["security", "intelligence", "cabinet"]
        for keyword in prohibited:
            if keyword.lower() in info_text.lower():
                issues.append(f"May contain restricted category: '{keyword}'")
                suggestions.append("Review RTI Act Section 8 exemptions")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions,
            "complexity_score": len(info_text.split()) + len(suggestions) * 5,
        }

    def _generate_hash(self, data: Dict[str, Any]) -> str:
        """Generate a SHA-256 hex digest of serialised form data.

        Args:
            data: Dictionary of form data.

        Returns:
            Hex-encoded SHA-256 hash string.
        """
        content_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()

    def _generate_fee_clause(
        self,
        user_data: Dict[str, Any],
        rules: Dict[str, Any],
    ) -> str:
        """Build the fee-payment clause for the document body.

        Args:
            user_data: Applicant form data.
            rules: Jurisdiction rules for the selected state.

        Returns:
            Formatted fee clause text.
        """
        if user_data.get("bpl") and rules.get("bpl_fee_waiver"):
            bpl_card = user_data.get("bpl_card_no", "____________")
            return (
                f"Being a Below Poverty Line (BPL) applicant (Card No: {bpl_card}), "
                "I am exempted from payment of the prescribed application fee under "
                "Section 7(5) of the RTI Act, 2005, and "
                f"{rules.get('state_rti_rule')}. BPL certificate enclosed."
            )
        fee = rules.get("fee", 10)
        payment = user_data.get("payment_method", "Demand Draft")
        return (
            f"I am enclosing herewith the prescribed application fee of Rs. {fee}/- "
            f"as per {rules.get('fee_rule_citation', 'RTI Rules')}. "
            f"Payment made via: {payment}."
        )

    def generate(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an RTI Application PDF.

        Args:
            user_data: Dictionary containing applicant details. Required keys:
                name, address, state, authority, pio_address, info.
                Optional: bpl, bpl_card_no, payment_method, place, mobile, email.

        Returns:
            Dictionary with keys: pdf_file, document_hash, reference_number, validation.
        """
        rules = self._load_rules(user_data["state"])
        validation = self._validate_request(user_data["info"])

        doc_hash = self._generate_hash(user_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ref_num = (
            f"RTI/{user_data['state'][:3].upper()}/"
            f"{datetime.now().year}/{doc_hash[:8].upper()}"
        )

        filename = (
            f"RTI_{user_data['name'].replace(' ', '_')}_{timestamp}.pdf"
        )
        file_path = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=1 * inch,
        )

        story = []

        story.append(
            Paragraph(
                "APPLICATION UNDER RIGHT TO INFORMATION ACT, 2005",
                self.styles["DocTitle"],
            )
        )
        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                f"<b>Reference No:</b> {ref_num}",
                self.styles["Normal"],
            )
        )
        story.append(Spacer(1, 20))

        address_data: List[List[str]] = [
            ["To,", ""],
            ["The Public Information Officer,", ""],
            [user_data["authority"], ""],
            [user_data["pio_address"], ""],
        ]
        address_table = Table(address_data, colWidths=[4.5 * inch, 1.5 * inch])
        address_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONT", (0, 0), (-1, -1), "Times-Roman", 11),
                ]
            )
        )
        story.append(address_table)
        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Subject:</b> Application for information under "
                "Section 6(1) of the Right to Information Act, 2005",
                self.styles["DocBody"],
            )
        )
        story.append(Spacer(1, 15))

        story.append(
            Paragraph("Respected Sir/Madam,", self.styles["DocBody"])
        )
        story.append(Spacer(1, 15))

        intro = (
            f"I, <b>{user_data['name']}</b>, residing at "
            f"<b>{user_data['address']}</b>, do hereby submit this application "
            "under the provisions of Section 6(1) of the Right to Information "
            "Act, 2005, seeking the following information from your esteemed office:"
        )
        story.append(Paragraph(intro, self.styles["DocBody"]))
        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>INFORMATION REQUESTED:</b>",
                self.styles["Heading2"],
            )
        )
        story.append(Spacer(1, 10))
        story.append(Paragraph(user_data["info"], self.styles["DocBody"]))
        story.append(Spacer(1, 15))

        fee_clause = self._generate_fee_clause(user_data, rules)
        story.append(Paragraph(fee_clause, self.styles["DocBody"]))
        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "I request that the information be provided in "
                "physical/electronic format as per my convenience.",
                self.styles["DocBody"],
            )
        )
        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "I hereby declare that the information sought does not fall "
                "within the restricted categories under Sections 8 and 9 of "
                "the RTI Act, 2005, to the best of my knowledge and belief. "
                "I undertake to pay any additional fee that may be required "
                "for providing the requested information.",
                self.styles["DocBody"],
            )
        )
        story.append(Spacer(1, 15))

        story.append(Paragraph("Thanking you,", self.styles["DocBody"]))
        story.append(Spacer(1, 10))
        story.append(
            Paragraph("Yours faithfully,", self.styles["DocBody"])
        )
        story.append(Spacer(1, 30))

        contact_data: List[List[str]] = [
            ["Full Name:", user_data["name"]],
            ["Address:", user_data["address"]],
            ["Mobile:", user_data.get("mobile", "_______________")],
            ["Email:", user_data.get("email", "_______________")],
        ]
        contact_table = Table(contact_data, colWidths=[1.5 * inch, 4 * inch])
        contact_table.setStyle(
            TableStyle(
                [
                    ("FONT", (0, 0), (0, -1), "Times-Bold", 10),
                    ("FONT", (1, 0), (-1, -1), "Times-Roman", 10),
                    ("PADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(contact_table)
        story.append(Spacer(1, 30))

        sig_data: List[List[str]] = [
            [
                "Place: " + user_data.get("place", "_______________"),
                "Signature: ___________________",
            ],
        ]
        sig_table = Table(sig_data, colWidths=[3 * inch, 3 * inch])
        sig_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (0, 0), "LEFT"),
                    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ]
            )
        )
        story.append(sig_table)
        story.append(Spacer(1, 35))

        story.append(Spacer(1, 20))

        footer_text = (
            f"<i>Document Hash: {doc_hash[:16]}... | "
            f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M')} | "
            f"Ref: {ref_num} | Applicant: {user_data['name']}</i>"
        )
        footer_style = ParagraphStyle(
            "FooterMeta",
            fontSize=7,
            fontName="Times-Roman",
            textColor=colors.grey,
            alignment=TA_CENTER,
        )
        story.append(Paragraph(footer_text, footer_style))

        doc.build(story)

        logger.info(
            "RTI PDF generated: %s | hash=%s | ref=%s",
            filename,
            doc_hash[:16],
            ref_num,
        )

        return {
            "pdf_file": file_path,
            "document_hash": doc_hash,
            "reference_number": ref_num,
            "validation": validation,
        }
