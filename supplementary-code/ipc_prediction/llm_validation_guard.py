import json
import math
import re
import logging
from typing import Any

logger = logging.getLogger(__name__)

MIN_CONFIDENCE: float = 0.30

_REQUIRED_KEYS: set[str] = {"predicted_sections", "confidence", "explanation"}


def _fallback_response() -> dict[str, Any]:
    return {
        "predicted_sections": [],
        "confidence": 0.0,
        "explanation": "The described incident does not clearly fall under a specific IPC section.",
    }


def _normalize_allowed_sections(allowed_section_numbers: list[str]) -> set[str]:
    normalized: set[str] = set()
    for value in allowed_section_numbers:
        text = str(value).strip()
        if text:
            normalized.add(text)
    return normalized


def _strip_markdown_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ```) that LLMs often wrap around JSON.

    Args:
        text: Raw LLM response text.

    Returns:
        Cleaned text with markdown fences removed, or the original text if no fences found.
    """
    stripped = text.strip()
    pattern = re.compile(r"^```(?:json)?\s*\n?(.*?)\n?\s*```$", re.DOTALL)
    match = pattern.match(stripped)
    if match:
        return match.group(1).strip()
    return stripped


def validate_llm_response(raw_response: str, allowed_section_numbers: list[str]) -> dict[str, Any]:
    """Validate and sanitize an LLM response against allowed IPC sections.

    Parses the raw response as JSON, verifies structure, checks section numbers
    against the allowed list, and clamps confidence values.

    Args:
        raw_response: Raw string response from the LLM.
        allowed_section_numbers: List of section numbers the LLM is allowed to predict.

    Returns:
        A validated dict with keys 'predicted_sections', 'confidence', and 'explanation',
        or a fallback response if validation fails.
    """
    try:
        cleaned = _strip_markdown_fences(raw_response)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("LLM response is not valid JSON")
            return _fallback_response()

        if not isinstance(parsed, dict):
            logger.warning("LLM response is not a dict")
            return _fallback_response()

        if not _REQUIRED_KEYS.issubset(set(parsed.keys())):
            logger.warning("LLM response missing required keys")
            return _fallback_response()

        predicted_sections = parsed.get("predicted_sections")
        confidence = parsed.get("confidence")
        explanation = parsed.get("explanation")

        if not isinstance(predicted_sections, list):
            return _fallback_response()

        if len(predicted_sections) != 1:
            return _fallback_response()

        section_value = predicted_sections[0]
        if not isinstance(section_value, str):
            return _fallback_response()

        sanitized_section = section_value.strip()
        if not sanitized_section:
            return _fallback_response()

        allowed_set = _normalize_allowed_sections(allowed_section_numbers)
        if sanitized_section not in allowed_set:
            logger.warning("Section %s not in allowed list", sanitized_section)
            return _fallback_response()

        if isinstance(confidence, str):
            return _fallback_response()

        if not isinstance(confidence, (int, float)):
            return _fallback_response()

        confidence_value = float(confidence)
        if not math.isfinite(confidence_value):
            return _fallback_response()

        clamped_confidence = max(0.0, min(1.0, confidence_value))
        if clamped_confidence < MIN_CONFIDENCE:
            return _fallback_response()

        if not isinstance(explanation, str):
            return _fallback_response()

        sanitized_explanation = explanation.strip()
        if not sanitized_explanation:
            return _fallback_response()

        return {
            "predicted_sections": [sanitized_section],
            "confidence": clamped_confidence,
            "explanation": sanitized_explanation,
        }
    except Exception as exc:
        logger.error("Unexpected error in validate_llm_response: %s", exc)
        return _fallback_response()
