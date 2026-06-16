import logging
from typing import Any

import requests

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from ipc_prediction.llm_instruction_template import build_ipc_reasoning_prompt
from ipc_prediction.retrieve_sections import _retrieve_with_scores
from ipc_prediction.llm_validation_guard import validate_llm_response

logger = logging.getLogger(__name__)

GEMINI_MODEL_NAME: str = GEMINI_MODEL
GEMINI_API_URL: str = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"{GEMINI_MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
)

SIMILARITY_THRESHOLD: float = -0.60


def _fallback_response() -> dict[str, Any]:
    return {
        "predicted_sections": [],
        "confidence": 0.0,
        "explanation": "The described incident does not clearly fall under a specific IPC section.",
        "title": "",
    }


def run_similarity_gate(incident_text: str) -> dict[str, Any]:
    """Run the similarity-based retrieval gate on the incident text.

    Retrieves candidate IPC sections and checks if the top similarity score
    exceeds the threshold. If it does, builds the LLM reasoning prompt.

    Args:
        incident_text: Description of the incident.

    Returns:
        A dict containing either fallback response or gate results with prompt.
    """
    try:
        ranked_candidates = _retrieve_with_scores(incident_text)
        if not ranked_candidates:
            logger.info("No candidates retrieved for incident text")
            return _fallback_response()

        top_similarity = float(ranked_candidates[0][1])
        if top_similarity < SIMILARITY_THRESHOLD:
            logger.info("Top similarity %.4f below threshold %.4f", top_similarity, SIMILARITY_THRESHOLD)
            return _fallback_response()

        candidate_sections = [metadata for metadata, _ in ranked_candidates]
        allowed_section_numbers = [
            str(section.get("section_number", "")).strip() for section in candidate_sections
        ]

        prompt = build_ipc_reasoning_prompt(incident_text, candidate_sections)

        return {
            "incident_text": incident_text,
            "candidate_sections": candidate_sections,
            "allowed_section_numbers": allowed_section_numbers,
            "llm_prompt": prompt,
        }
    except Exception as exc:
        logger.error("Similarity gate failed: %s", exc)
        return _fallback_response()


def predict_ipc_section(incident_text: str) -> dict[str, Any]:
    """Predict the most applicable IPC section for a given incident description.

    Runs the similarity gate, calls the Gemini LLM if the gate passes,
    validates the LLM response, and returns structured prediction results.

    Args:
        incident_text: Description of the incident.

    Returns:
        A dict with keys 'predicted_sections', 'confidence', 'explanation', 'title'.
    """
    try:
        gate_result = run_similarity_gate(incident_text)

        if "llm_prompt" not in gate_result:
            gate_result.setdefault("title", "")
            return gate_result

        llm_prompt = gate_result["llm_prompt"]
        allowed_section_numbers = gate_result["allowed_section_numbers"]

        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "contents": [
                {
                    "parts": [{"text": llm_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.0,
            },
        }

        try:
            response = requests.post(
                GEMINI_API_URL,
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Gemini API call failed: %s", exc)
            return _fallback_response()

        body = response.json()
        try:
            raw_response = body["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as exc:
            logger.error("Unexpected Gemini response structure: %s", exc)
            return _fallback_response()

        validated = validate_llm_response(raw_response, allowed_section_numbers)

        title = ""
        if validated.get("predicted_sections"):
            predicted_section = str(validated["predicted_sections"][0]).strip()
            for candidate in gate_result.get("candidate_sections", []):
                if str(candidate.get("section_number", "")).strip() == predicted_section:
                    title = str(candidate.get("title", "")).strip()
                    break

        validated["title"] = title
        return validated
    except Exception as exc:
        logger.error("Unexpected error in predict_ipc_section: %s", exc)
        return _fallback_response()
