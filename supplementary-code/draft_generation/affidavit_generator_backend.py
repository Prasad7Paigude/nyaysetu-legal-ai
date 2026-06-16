"""
Affidavit Generator Module - Production-ready Affidavit PDF generation.

Generates formatted affidavits with court headers, deponent information,
numbered statements, verification clauses, and document metadata.
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config.settings import DRAFT_GEN_DIR

logger = logging.getLogger(__name__)


class AffidavitGenerator:
    """Production-ready affidavit document generator."""

    def __init__(self) -> None:
        """Initialise styles and ensure the output directory exists."""
        self.styles = self._setup_styles()
        self.output_dir: str = str(DRAFT_GEN_DIR / "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    def _setup_styles(self) -> Any:
        """Set up professional PDF styles for affidavits.

        Returns:
            ReportLab stylesheet with added affidavit-specific styles.
        """
        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="AffTitle",
                parent=styles["Title"],
                fontSize=14,
                fontName="Times-Bold",
                alignment=TA_CENTER,
                spaceAfter=20,
                spaceBefore=10,
            )
        )

        styles.add(
            ParagraphStyle(
                name="SectionHead",
                fontSize=12,
                fontName="Times-Bold",
                alignment=TA_CENTER,
                spaceAfter=15,
                spaceBefore=20,
            )
        )

        styles.add(
            ParagraphStyle(
                name="AffBody",
                parent=styles["Normal"],
                fontSize=11,
                fontName="Times-Roman",
                alignment=TA_JUSTIFY,
                spaceAfter=10,
                leading=16,
                firstLineIndent=20,
            )
        )

        styles.add(
            ParagraphStyle(
                name="Statement",
                fontSize=11,
                fontName="Times-Roman",
                alignment=TA_JUSTIFY,
                spaceAfter=12,
                leading=16,
                leftIndent=30,
                firstLineIndent=-15,
            )
        )

        styles.add(
            ParagraphStyle(
                name="Footer",
                fontSize=8,
                fontName="Times-Roman",
                textColor=colors.grey,
                alignment=TA_CENTER,
            )
        )

        return styles

    def _generate_hash(self, data: Dict[str, Any]) -> str:
        """Generate a SHA-256 hex digest of serialised form data.

        Args:
            data: Dictionary of form data.

        Returns:
            Hex-encoded SHA-256 hash string.
        """
        content_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()

    def generate(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate an Affidavit PDF.

        Args:
            user_data: Dictionary containing deponent details. Required keys:
                deponent_name, address, statements.
                Optional: court_name, case_number, gender, father_name, age,
                place, mobile, email.

        Returns:
            Dictionary with keys: pdf_file, document_hash.
        """
        doc_hash = self._generate_hash(user_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = (
            f"Affidavit_{user_data['deponent_name'].replace(' ', '_')}_"
            f"{timestamp}.pdf"
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

        story: List[Any] = []

        if user_data.get("court_name"):
            story.append(Spacer(1, 15))
            story.append(
                Paragraph(
                    f"IN THE {user_data['court_name'].upper()}",
                    self.styles["AffTitle"],
                )
            )
            story.append(Spacer(1, 12))

            if user_data.get("case_number"):
                case_style = ParagraphStyle(
                    "CaseNum",
                    fontSize=10,
                    fontName="Times-Roman",
                    alignment=TA_CENTER,
                    spaceAfter=8,
                )
                story.append(
                    Paragraph(
                        f"<b>Case No:</b> {user_data['case_number']}",
                        case_style,
                    )
                )
                story.append(Spacer(1, 20))

        story.append(Spacer(1, 10))
        title_style = ParagraphStyle(
            "MainTitle",
            fontSize=14,
            fontName="Times-Bold",
            alignment=TA_CENTER,
            spaceAfter=25,
            underline=True,
        )
        story.append(Paragraph("AFFIDAVIT", title_style))
        story.append(Spacer(1, 15))

        gender = user_data.get("gender", "male").lower()
        relation = "son" if gender == "male" else "daughter"

        opening_text = (
            f"{relation} of <b>{user_data.get('father_name', '_____________')}</b>, "
            f"aged about <b>{user_data.get('age', '_____')}</b> years, "
            f"residing at <b>{user_data['address']}</b>, "
            "do hereby solemnly affirm and state as under:"
        )

        deponent_style = ParagraphStyle(
            "DeponentInfo",
            fontSize=11,
            fontName="Times-Roman",
            alignment=TA_JUSTIFY,
            spaceAfter=18,
            leading=16,
            leftIndent=40,
            rightIndent=40,
        )

        story.append(
            Paragraph(
                f"I, <b>{user_data['deponent_name']}</b>, {opening_text}",
                deponent_style,
            )
        )
        story.append(Spacer(1, 20))

        statements: List[str] = user_data.get("statements", [])

        statement_style = ParagraphStyle(
            "StatementText",
            fontSize=11,
            fontName="Times-Roman",
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=16,
            leftIndent=20,
        )

        for i, statement in enumerate(statements, 1):
            stmt_text = f"<b>{i}.</b>&nbsp;&nbsp;{statement}"
            story.append(Paragraph(stmt_text, statement_style))

        story.append(Spacer(1, 30))

        story.append(Spacer(1, 25))
        story.append(Paragraph("DEPONENT", self.styles["SectionHead"]))
        story.append(Spacer(1, 35))

        sig_style = ParagraphStyle(
            "Signature",
            fontSize=10,
            fontName="Times-Roman",
            alignment=TA_CENTER,
        )

        story.append(Paragraph("____________________________", sig_style))
        story.append(
            Paragraph(
                f"<b>({user_data['deponent_name']})</b>", sig_style
            )
        )
        story.append(Spacer(1, 35))

        story.append(Spacer(1, 25))

        verif_title_style = ParagraphStyle(
            "VerifTitle",
            fontSize=12,
            fontName="Times-Bold",
            alignment=TA_CENTER,
            spaceAfter=18,
            underline=True,
        )
        story.append(Paragraph("VERIFICATION", verif_title_style))
        story.append(Spacer(1, 15))

        verification_text = (
            f"I, <b>{user_data['deponent_name']}</b>, the deponent above named, "
            "do hereby verify that the contents of the above affidavit are "
            "true and correct to the best of my knowledge and belief and "
            "nothing material has been concealed therefrom."
        )

        verif_style = ParagraphStyle(
            "VerifText",
            fontSize=11,
            fontName="Times-Roman",
            alignment=TA_JUSTIFY,
            spaceAfter=15,
            leading=16,
            leftIndent=40,
            rightIndent=40,
        )

        story.append(Paragraph(verification_text, verif_style))
        story.append(Spacer(1, 15))

        place_date_style = ParagraphStyle(
            "PlaceDate",
            fontSize=11,
            fontName="Times-Roman",
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leftIndent=40,
        )

        story.append(
            Paragraph(
                f"Verified at <b>{user_data.get('place', '_______________')}</b> "
                f"on this <b>{datetime.now().strftime('%d day of %B, %Y')}</b>.",
                place_date_style,
            )
        )
        story.append(Spacer(1, 35))

        story.append(Paragraph("DEPONENT", self.styles["SectionHead"]))
        story.append(Spacer(1, 35))

        final_sig_style = ParagraphStyle(
            "FinalSignature",
            fontSize=10,
            fontName="Times-Roman",
            alignment=TA_CENTER,
        )

        story.append(
            Paragraph("____________________________", final_sig_style)
        )
        story.append(
            Paragraph(
                f"<b>({user_data['deponent_name']})</b>", final_sig_style
            )
        )

        story.append(Spacer(1, 30))

        footer_text = (
            f"<i>Document Hash: {doc_hash[:16]}... | "
            f"Generated: {datetime.now().strftime('%d-%b-%Y %H:%M')} | "
            f"Deponent: {user_data['deponent_name']}</i>"
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
            "Affidavit PDF generated: %s | hash=%s",
            filename,
            doc_hash[:16],
        )

        return {"pdf_file": file_path, "document_hash": doc_hash}
