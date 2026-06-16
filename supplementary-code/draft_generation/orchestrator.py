"""
NyaySetu Document Orchestrator - AI-powered analysis and document-type routing.

Uses keyword matching with programmatic expansion and optional Groq LLM fallback
to classify user requirements as RTI Application or Affidavit.
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from groq import Groq

from config.settings import GROQ_API_KEY

logger = logging.getLogger(__name__)


class DocumentOrchestrator:
    """Orchestrates multi-document generation with AI-powered requirement analysis."""

    TEMPLATES: Dict[str, Dict[str, Any]] = {
        "RTI_APPLICATION": {
            "name": "RTI Application",
            "complexity": 8,
            "base_keywords": [
                "rti",
                "right to information",
                "right to information act",
                "information act",
                "rti act 2005",
                "section 6",
                "section 7",
                "section 8",
                "section 18",
                "section 19",
                "first appeal",
                "second appeal",
                "pio",
                "cpio",
                "spio",
                "public information officer",
                "appellate authority",
                "faa",
                "sic",
                "cic",
                "information commission",
                "state information commission",
                "central information commission",
                "want to know",
                "need to know",
                "seeking information",
                "request information",
                "request details",
                "ask details",
                "obtain details",
                "obtain copy",
                "provide copy",
                "give copy",
                "furnish details",
                "supply information",
                "share information",
                "disclose information",
                "inspection of records",
                "certified copy",
                "attested copy",
                "true copy",
                "request copy",
                "need copy",
                "get copy",
                "record",
                "official record",
                "government record",
                "department record",
                "document",
                "official document",
                "file",
                "file noting",
                "file notings",
                "movement of file",
                "correspondence",
                "internal correspondence",
                "office note",
                "register",
                "ledger",
                "logbook",
                "report",
                "inspection report",
                "audit report",
                "vigilance report",
                "enquiry report",
                "committee report",
                "government file",
                "status of application",
                "status of complaint",
                "action taken",
                "action taken report",
                "atr",
                "progress report",
                "pending status",
                "delay reason",
                "timeline",
                "reason for delay",
                "why not approved",
                "why rejected",
                "grounds of rejection",
                "status update",
                "current status",
                "application status",
                "answer sheet",
                "evaluated answer sheet",
                "exam answer sheet",
                "mark sheet",
                "marksheet copy",
                "marks obtained",
                "grade sheet",
                "cutoff marks",
                "cutoff mark",
                "revaluation result",
                "moderation marks",
                "internal marks",
                "attendance record",
                "exam record",
                "admission form",
                "application form",
                "evaluation criteria",
                "exam rules",
                "university record",
                "college record",
                "academic record",
                "transcript",
                "degree certificate",
                "diploma",
                "enrollment record",
                "registration record",
                "exam paper",
                "question paper",
                "assessment record",
                "7/12 extract",
                "satbara",
                "property card",
                "mutation entry",
                "ferfar",
                "record of rights",
                "land record",
                "survey number",
                "gat number",
                "cts number",
                "measurement record",
                "demarcation record",
                "land acquisition file",
                "award copy",
                "compensation details",
                "ownership record",
                "title record",
                "property document",
                "registry copy",
                "sale deed copy",
                "fir copy",
                "complaint status",
                "police complaint",
                "diary entry",
                "nc complaint",
                "case diary",
                "chargesheet status",
                "investigation status",
                "action taken by police",
                "reason for no fir",
                "police record",
                "station diary",
                "tender document",
                "bid details",
                "contract copy",
                "work order",
                "utilization certificate",
                "fund allocation",
                "fund release",
                "scheme guidelines",
                "beneficiary list",
                "selection criteria",
                "contractor details",
                "payment details",
                "bill copy",
                "voucher copy",
                "tender notice",
                "quotation",
                "proposal",
                "service record",
                "appointment order",
                "joining report",
                "promotion details",
                "transfer order",
                "posting order",
                "salary details",
                "pay scale",
                "pay slip",
                "arrears calculation",
                "pension record",
                "gratuity details",
                "service book",
                "employment record",
                "appointment letter",
                "increment details",
                "transparency",
                "accountability",
                "public interest",
                "public money",
                "taxpayer money",
                "misuse of funds",
                "irregularities",
                "procedure followed",
                "rule followed",
                "compliance report",
                "disclosure",
                "public authority",
                "government information",
                "public sector",
                "municipality",
                "panchayat",
                "ministry",
                "department",
                "government department",
                "public office",
                "government office",
                "authority information",
                "official information",
                "copy of document",
                "information sought",
                "details requested",
            ],
            "negative_keywords": [
                "court affidavit",
                "sworn before",
                "notarize",
                "notary",
                "deponent",
                "solemnly swear",
                "penalty of perjury",
                "court case affidavit",
                "file in court",
                "submit to court",
                "legal proceedings affidavit",
                "my name is",
                "i hereby declare",
                "i solemnly",
            ],
        },
        "AFFIDAVIT": {
            "name": "Affidavit",
            "complexity": 7,
            "base_keywords": [
                "affidavit",
                "sworn affidavit",
                "self affidavit",
                "sworn statement",
                "self declaration",
                "declaration",
                "undertaking",
                "solemnly declare",
                "hereby declare",
                "affirm",
                "swear",
                "oath",
                "deponent",
                "affiant",
                "solemn affirmation",
                "sworn before",
                "sworn testimony",
                "my name is",
                "name correction",
                "name mismatch",
                "alias",
                "also known as",
                "address proof",
                "residential address",
                "current address",
                "permanent address",
                "identity proof",
                "proof of identity",
                "verify my identity",
                "confirm my name",
                "proof of residence",
                "proof of address",
                "date of birth",
                "dob correction",
                "age proof",
                "nationality declaration",
                "citizenship declaration",
                "religion declaration",
                "marital status",
                "single status",
                "unmarried",
                "married",
                "divorced",
                "widow",
                "widower",
                "birth date affidavit",
                "age declaration",
                "status declaration",
                "income affidavit",
                "income declaration",
                "annual income",
                "below poverty line",
                "bpl declaration",
                "non creamy layer",
                "dependent on parents",
                "family income",
                "unemployed",
                "not employed",
                "self employed declaration",
                "student declaration",
                "financially dependent",
                "income certificate affidavit",
                "poverty affidavit",
                "lost document",
                "lost certificate",
                "misplaced document",
                "damage of document",
                "not traceable",
                "document destroyed",
                "fir for loss",
                "loss declaration",
                "certificate lost",
                "lost my certificate",
                "document missing",
                "cannot find document",
                "destroyed document",
                "gap affidavit",
                "education gap",
                "year gap",
                "bonafide declaration",
                "character affidavit",
                "conduct affidavit",
                "anti ragging affidavit",
                "study gap",
                "break in education",
                "gap certificate affidavit",
                "character certificate affidavit",
                "legal heir affidavit",
                "surviving member",
                "family tree",
                "relationship proof",
                "father name",
                "mother name",
                "guardian declaration",
                "next of kin",
                "heir certificate",
                "succession affidavit",
                "family member affidavit",
                "parent details",
                "relationship declaration",
                "passport affidavit",
                "annexure e",
                "annexure f",
                "no objection affidavit",
                "noc affidavit",
                "address verification",
                "identity verification",
                "passport application affidavit",
                "visa affidavit",
                "immigration affidavit",
                "police verification affidavit",
                "noc for passport",
                "filed before court",
                "submitted to court",
                "court affidavit",
                "judicial proceeding",
                "legal proceeding",
                "case affidavit",
                "petition affidavit",
                "court filing",
                "legal filing",
                "affidavit for court",
                "submit affidavit",
                "file affidavit",
                "court submission",
                "legal matter affidavit",
                "case filing",
                "petition filing",
                "true and correct",
                "best of my knowledge",
                "nothing concealed",
                "no criminal record",
                "no pending case",
                "not involved in offence",
                "truthfully declare",
                "honestly state",
                "verify facts",
                "certify truth",
                "confirm authenticity",
                "guarantee accuracy",
                "testimony",
                "evidence",
                "witness",
                "statement of facts",
                "legal document",
                "notarize",
                "notary",
                "attestation",
                "certified statement",
                "name change",
                "change of name",
                "surname change",
                "income proof",
                "relationship certificate",
                "birth certificate affidavit",
                "death certificate affidavit",
                "marriage certificate affidavit",
                "criminal case",
                "civil case",
                "family court",
                "divorce",
                "custody",
                "property dispute",
                "inheritance",
                "will",
                "succession",
                "litigation",
                "lawsuit",
                "tribunal",
                "hearing",
                "judge",
                "magistrate",
                "attorney",
                "lawyer",
                "visa application",
                "immigration",
                "legal heir certificate",
                "verification affidavit",
                "self certification",
                "verify",
                "verification",
                "certified",
                "authentic",
                "genuine",
                "true statement",
                "correct statement",
                "accurate statement",
                "proof that i am",
                "certificate that i am",
                "government proof of my statement",
                "official confirmation of my claim",
                "declare officially",
                "confirm officially",
                "legally certify my statement",
                "sworn proof",
                "legal proof of my identity",
                "official proof of",
                "certify that i",
                "confirm that i",
                "declare that i",
                "state that i",
                "affirm that i",
                "testify that i",
            ],
            "negative_keywords": [
                "government record",
                "government file",
                "public authority record",
                "rti application",
                "information commission",
                "pio",
                "cpio",
                "right to information",
                "seeking information from government",
                "government information",
                "public information officer",
            ],
        },
    }

    CLARIFICATION_QUESTIONS: Dict[str, Dict[str, Any]] = {
        "rti_information_vs_declaration": {
            "category": "RTI",
            "trigger_keywords": [
                "information",
                "record",
                "document",
                "copy",
                "file",
                "data",
            ],
            "questions": [
                "Are you asking for existing records held by a government office?",
                "Do you want copies of documents already available with an authority?",
                "Are you trying to know something, not declare something?",
                "Is the information already created by a government department?",
            ],
        },
        "rti_authority": {
            "category": "RTI",
            "trigger_keywords": [
                "government",
                "office",
                "department",
                "authority",
                "ministry",
            ],
            "questions": [
                "Which government department holds this information?",
                "Is the authority a public university or government college?",
                "Is the authority a municipal corporation or panchayat?",
                "Is the information held by a police station or revenue office?",
            ],
        },
        "rti_document_type": {
            "category": "RTI",
            "trigger_keywords": ["exam", "answer", "marksheet", "land", "tender", "fir"],
            "questions": [
                "Are you asking for answer sheets or exam records?",
                "Are you requesting land records or property documents?",
                "Are you seeking service or salary records?",
                "Are you requesting tender or contract documents?",
            ],
        },
        "rti_transparency": {
            "category": "RTI",
            "trigger_keywords": ["status", "why", "reason", "action", "delay"],
            "questions": [
                "Are you asking why or how a decision was taken?",
                "Are you seeking file movement or file notings?",
                "Are you asking for status, action taken, or reasons?",
                "Is this about transparency or accountability?",
            ],
        },
        "affidavit_declaration": {
            "category": "AFFIDAVIT",
            "trigger_keywords": [
                "declare",
                "state",
                "affirm",
                "swear",
                "my",
                "i am",
            ],
            "questions": [
                "Are you trying to declare a personal fact?",
                "Are you stating something as true to your knowledge?",
                "Do you need to affirm or swear a statement?",
                "Are you declaring information about yourself?",
            ],
        },
        "affidavit_identity": {
            "category": "AFFIDAVIT",
            "trigger_keywords": [
                "name",
                "address",
                "identity",
                "proof",
                "dob",
                "birth",
            ],
            "questions": [
                "Is this about name correction or identity proof?",
                "Is this about address proof or residence verification?",
                "Is this about date of birth correction?",
                "Is this about relationship proof or legal heir status?",
            ],
        },
        "affidavit_income": {
            "category": "AFFIDAVIT",
            "trigger_keywords": [
                "income",
                "salary",
                "bpl",
                "earning",
                "financial",
                "poor",
            ],
            "questions": [
                "Are you declaring your income or financial status?",
                "Is this for scholarship or fee concession?",
                "Are you declaring unemployment or dependency?",
                "Is this related to BPL or EWS status?",
            ],
        },
        "affidavit_loss": {
            "category": "AFFIDAVIT",
            "trigger_keywords": [
                "lost",
                "damage",
                "missing",
                "destroyed",
                "misplace",
            ],
            "questions": [
                "Have you lost a document?",
                "Is the original document damaged or destroyed?",
                "Are you declaring loss for reissue or duplicate?",
                "Have you filed an FIR for the loss?",
            ],
        },
        "affidavit_court": {
            "category": "AFFIDAVIT",
            "trigger_keywords": [
                "court",
                "case",
                "judge",
                "legal",
                "petition",
            ],
            "questions": [
                "Will this document be submitted to a court?",
                "Is this part of a legal proceeding?",
                "Is this required by a judge or magistrate?",
                "Is this a court-mandated affidavit?",
            ],
        },
        "affidavit_education": {
            "category": "AFFIDAVIT",
            "trigger_keywords": [
                "gap",
                "year",
                "anti-ragging",
                "bonafide",
                "character",
            ],
            "questions": [
                "Is this about education gap or year gap?",
                "Is this for bonafide or character certificate?",
                "Is this an anti-ragging affidavit?",
                "Is this for college admission?",
            ],
        },
        "confusion_resolution": {
            "category": "BOTH",
            "trigger_keywords": [
                "proof",
                "certificate",
                "verify",
                "confirm",
            ],
            "questions": [
                "Are you trying to change a record or just get a copy?",
                "Do you want the government to accept your statement?",
                "Are you trying to prove something about yourself?",
                "Are you asking the authority to answer questions?",
            ],
        },
    }

    def __init__(self) -> None:
        """Initialize the orchestrator and expand keyword lists."""
        self.groq_client: Optional[Groq] = (
            Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        )
        if not GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set; LLM fallback will be unavailable")
        self._expand_all_keywords()

    # --- keyword expansion (runs once at init) ---------------------------------

    def _expand_all_keywords(self) -> None:
        """Programmatically expand keywords for every template."""
        for doc_type, info in self.TEMPLATES.items():
            base: List[str] = info["base_keywords"]
            info["keywords"] = self._expand_keywords(base)
            logger.debug(
                "%s: %s keywords after expansion",
                doc_type,
                len(info["keywords"]),
            )

    @staticmethod
    def _expand_keywords(base_keywords: List[str]) -> List[str]:
        """Expand keywords with singular/plural and hyphenated variants.

        Args:
            base_keywords: Original keyword list.

        Returns:
            Deduplicated expanded keyword list.
        """
        expanded: set[str] = set(base_keywords)
        for keyword in base_keywords:
            if keyword.endswith("s") and len(keyword) > 3:
                expanded.add(keyword[:-1])
            elif not keyword.endswith("s"):
                expanded.add(keyword + "s")
            if " " in keyword:
                expanded.add(keyword.replace(" ", "-"))
                expanded.add(keyword.replace(" ", ""))
        return list(expanded)

    # --- public API ------------------------------------------------------------

    def analyze_requirements(self, description: str) -> Dict[str, Any]:
        """Analyze user requirement and suggest a document type.

        Args:
            description: Free-text description of the user's legal need.

        Returns:
            Dictionary with keys: status, primary_document, document_name,
            confidence, estimated_complexity, complexity_score,
            estimated_time_minutes, potential_challenges,
            recommended_approach, score_details.
        """
        desc_lower = description.lower()

        edge_case_boost = self._compute_edge_case_boost(desc_lower)
        scores = self._compute_scores(desc_lower, edge_case_boost)

        if not any(scores.values()):
            return self._generate_clarification_response(
                base_confidence=0,
                description=description,
                scores=scores,
            )

        primary_doc, max_score, second_highest = self._rank_scores(scores)
        confidence = self._compute_confidence(max_score, second_highest)

        if confidence < 70 and self.groq_client:
            groq_result = self._try_groq_analysis(description)
            if groq_result:
                if groq_result.get("confidence", 0) >= 80:
                    primary_doc = groq_result["document_type"]
                    confidence = groq_result["confidence"]
                    scores[primary_doc] = max(scores.get(primary_doc, 0), confidence)
                elif groq_result.get("clarification_needed"):
                    return self._generate_clarification_response(
                        base_confidence=confidence,
                        suggested_doc=primary_doc,
                        description=description,
                        scores=scores,
                        llm_questions=groq_result.get("questions"),
                    )

        if confidence < 70:
            return self._generate_clarification_response(
                base_confidence=confidence,
                suggested_doc=primary_doc,
                description=description,
                scores=scores,
            )

        template_info = self.TEMPLATES[primary_doc]
        complexity_score = template_info["complexity"] * 10 + 15 + 10
        challenges: List[str] = []

        if any(w in desc_lower for w in ["urgent", "emergency", "immediate"]):
            challenges.append("Urgent request - ensure timeline compliance")
        if (
            any(w in desc_lower for w in ["court", "legal", "case"])
            and primary_doc == "RTI_APPLICATION"
        ):
            challenges.append(
                "Legal matter - verify if RTI is appropriate or if Affidavit is needed"
            )

        if primary_doc == "RTI_APPLICATION":
            approach = (
                "Submit RTI application to the Public Information Officer (PIO) "
                "of the relevant authority. Include specific details of information "
                "needed, payment proof, and contact details."
            )
        else:
            approach = (
                "Prepare sworn affidavit with clear statement of facts. "
                "Get it notarized before submitting to the concerned authority or court."
            )

        return {
            "status": "success",
            "primary_document": primary_doc,
            "document_name": template_info["name"],
            "confidence": confidence,
            "estimated_complexity": template_info["complexity"],
            "complexity_score": complexity_score,
            "estimated_time_minutes": 15,
            "potential_challenges": challenges,
            "recommended_approach": approach,
            "score_details": scores,
        }

    def calculate_complexity_score(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate a complexity breakdown for a document.

        Args:
            document_data: Dictionary containing at least a 'type' key.

        Returns:
            Dictionary with keys: total_score, breakdown (list), level.
        """
        score = 0
        factors: List[str] = []

        doc_type = document_data.get("type", "RTI_APPLICATION")
        template = self.TEMPLATES.get(doc_type, self.TEMPLATES["RTI_APPLICATION"])
        base_score = template["complexity"] * 10
        score += base_score
        factors.append(f"Template base: {base_score}")

        if document_data.get("validation_enabled", True):
            score += 15
            factors.append("AI validation: +15")
        if document_data.get("blockchain_enabled", True):
            score += 10
            factors.append("Blockchain: +10")
        if document_data.get("citations", True):
            score += 10
            factors.append("Legal citations: +10")

        level = "HIGH" if score > 70 else "MEDIUM" if score > 40 else "LOW"
        return {"total_score": score, "breakdown": factors, "level": level}

    # --- internal helpers -----------------------------------------------------

    @staticmethod
    def _compute_edge_case_boost(desc_lower: str) -> int:
        """Compute an affidavit boost based on edge-case keyword matches."""
        edge_case_keywords = [
            "proof that i am",
            "proof that i",
            "certificate that i am",
            "certificate that i",
            "declare that i",
            "state that i",
            "affirm that i",
            "certify that i",
            "confirm that i",
            "testify that i",
            "my name is",
            "i hereby",
            "i solemnly",
            "proof of my",
            "officially confirm",
            "officially declare",
        ]
        boost = 0
        for kw in edge_case_keywords:
            if kw in desc_lower:
                boost += 50
        return boost

    def _compute_scores(
        self,
        desc_lower: str,
        edge_case_boost: int,
    ) -> Dict[str, int]:
        """Compute raw keyword-match scores for each document type.

        Returns:
            Dictionary mapping document type keys to integer scores.
        """
        scores: Dict[str, int] = {}
        for doc_type, info in self.TEMPLATES.items():
            positive = sum(1 for kw in info["keywords"] if kw in desc_lower)
            negative = sum(
                1 for kw in info.get("negative_keywords", []) if kw in desc_lower
            )
            score = (positive * 10) - (negative * 20)
            if doc_type == "AFFIDAVIT":
                score += edge_case_boost
            scores[doc_type] = max(0, score)
        return scores

    @staticmethod
    def _rank_scores(
        scores: Dict[str, int],
    ) -> Tuple[str, int, int]:
        """Determine the top-ranked document type and the runner-up score.

        Returns:
            Tuple of (primary_doc, max_score, second_highest_score).
        """
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_doc = sorted_scores[0][0]
        max_score = sorted_scores[0][1]
        second_highest = sorted_scores[1][1] if len(sorted_scores) > 1 else 0
        return primary_doc, max_score, second_highest

    @staticmethod
    def _compute_confidence(max_score: int, second_highest: int) -> int:
        """Convert raw scores into a 0-100 confidence percentage."""
        gap = max_score - second_highest
        if max_score >= 50 or gap >= 30:
            return 98
        if max_score >= 30 and gap >= 15:
            return 95
        if max_score >= 20 and gap >= 10:
            return 85
        if max_score >= 15 and gap >= 5:
            return 75
        if max_score >= 10:
            return 65
        return 50

    def _try_groq_analysis(self, description: str) -> Optional[Dict[str, Any]]:
        """Attempt to classify the requirement via the Groq LLM.

        Args:
            description: The user's requirement text.

        Returns:
            Parsed JSON response from the LLM, or None on failure.
        """
        try:
            system_prompt = """You are an expert legal document router for Indian law (NyaySetu project).
Your task is to analyze user requirement and determine if they need an RTI Application or an Affidavit.

RTI APPLICATION is for:
- Requesting specific information, records, or documents from government / public authorities.
- Seeking transparency on government actions, status of complaints, or fund utilization.
- Examples: marksheets from universities, FIR copies, tender details, land records (7/12), ration card status.

AFFIDAVIT is for:
- Personal sworn declarations or statements of facts made under oath.
- Proving identity, address, income, or relationship status officially.
- Declarations for lost documents, name changes, education gaps, or court filings.
- Examples: Name correction affidavit, Income affidavit, Gap certificate affidavit, Legal heir declaration.

Response format (JSON only):
{
  "document_type": "RTI_APPLICATION" or "AFFIDAVIT",
  "confidence": 0-100,
  "reasoning": "Short explanation",
  "clarification_needed": true/false,
  "questions": ["Specific question to distinguish if unsure"]
}"""

            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User's legal need: {description}"},
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            return json.loads(response.choices[0].message.content)
        except Exception as exc:
            logger.error("Groq internal error: %s", exc)
            return None

    @staticmethod
    def _select_clarification_questions(
        description: str,
        scores: Dict[str, int],
    ) -> List[Dict[str, Any]]:
        """Select 2-4 context-aware clarification questions.

        Args:
            description: The user's requirement text.
            scores: Per-document-type confidence scores.

        Returns:
            A list of question dictionaries with 'text', 'leads_to', 'category'.
        """
        desc_lower = description.lower()

        if scores.get("RTI_APPLICATION", 0) > scores.get("AFFIDAVIT", 0):
            primary_category = "RTI"
        elif scores.get("AFFIDAVIT", 0) > scores.get("RTI_APPLICATION", 0):
            primary_category = "AFFIDAVIT"
        else:
            primary_category = "BOTH"

        relevant_cats: List[Tuple[str, Dict[str, Any]]] = []
        for cat_key, cat_data in DocumentOrchestrator.CLARIFICATION_QUESTIONS.items():
            if any(kw in desc_lower for kw in cat_data["trigger_keywords"]):
                pair = (cat_key, cat_data)
                if cat_data["category"] in (primary_category, "BOTH"):
                    relevant_cats.insert(0, pair)
                else:
                    relevant_cats.append(pair)

        if not relevant_cats:
            relevant_cats = [
                (
                    "confusion_resolution",
                    DocumentOrchestrator.CLARIFICATION_QUESTIONS[
                        "confusion_resolution"
                    ],
                )
            ]

        selected_cats = relevant_cats[: min(2, len(relevant_cats))]
        final_questions: List[Dict[str, Any]] = []
        for cat_key, cat_data in selected_cats:
            for q in cat_data["questions"][:2]:
                final_questions.append(
                    {
                        "text": q,
                        "leads_to": (
                            "RTI_APPLICATION"
                            if cat_data["category"] == "RTI"
                            else (
                                "AFFIDAVIT"
                                if cat_data["category"] == "AFFIDAVIT"
                                else primary_category
                            )
                        ),
                        "category": cat_data["category"],
                    }
                )
        return final_questions[:4]

    def _generate_clarification_response(
        self,
        base_confidence: int,
        suggested_doc: Optional[str] = None,
        description: str = "",
        scores: Optional[Dict[str, int]] = None,
        llm_questions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Build a 'needs_clarification' response with context-aware questions.

        Args:
            base_confidence: Current confidence score.
            suggested_doc: Best-guess document type.
            description: Original user input.
            scores: Per-document scores.
            llm_questions: Optional questions from the LLM fallback.

        Returns:
            Response dictionary with status, questions, and metadata.
        """
        if scores is None:
            scores = {}
        formatted_questions: List[Dict[str, Any]] = []

        if llm_questions:
            for q_text in llm_questions:
                formatted_questions.append(
                    {
                        "question": q_text,
                        "options": [
                            {
                                "text": "Yes",
                                "leads_to": suggested_doc or "RTI_APPLICATION",
                            },
                            {
                                "text": "No",
                                "leads_to": (
                                    "AFFIDAVIT"
                                    if suggested_doc == "RTI_APPLICATION"
                                    else "RTI_APPLICATION"
                                ),
                            },
                        ],
                    }
                )

        if not formatted_questions:
            selected = self._select_clarification_questions(
                description,
                scores,
            )
            opposite = (
                "AFFIDAVIT"
                if suggested_doc == "RTI_APPLICATION"
                else "RTI_APPLICATION"
            )
            for q in selected:
                formatted_questions.append(
                    {
                        "question": q["text"],
                        "options": [
                            {
                                "text": "Yes",
                                "leads_to": (
                                    q["leads_to"]
                                    if q["category"] != "BOTH"
                                    else suggested_doc or "RTI_APPLICATION"
                                ),
                            },
                            {"text": "No", "leads_to": opposite},
                        ],
                    }
                )

        return {
            "status": "needs_clarification",
            "confidence": max(base_confidence, 55),
            "suggested_document": suggested_doc,
            "questions": formatted_questions,
            "message": "I need a bit more information to suggest the right document for you.",
        }
