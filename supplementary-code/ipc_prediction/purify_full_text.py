from __future__ import annotations

import json
import re
import logging
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

from jsonschema import Draft202012Validator

from config.settings import DATA_DIR

logger = logging.getLogger(__name__)

DRAFT_PATH: Path = DATA_DIR / "ipc_enriched_v1_draft.json"
OUTPUT_PATH: Path = DATA_DIR / "ipc_enriched_v1.json"
SCHEMA_PATH: Path = DATA_DIR / "ipc_enriched_v1.schema.json"

NUMBERED_ARTIFACT_PATTERNS: list[re.Pattern] = [
    re.compile(r"\s*\d+\.,\s*for\s+\"[^\"]*\"\.?$", re.IGNORECASE),
    re.compile(r"\s*\d+\.\s*[IVXLC\d]+,\s*for[\s\S]*$", re.IGNORECASE),
    re.compile(
        r"\s*\d+\.\s*(?:cl\.|cls\.|the words|the word|the letters?|the figures?|ins\.?|inserted|substituted|omitted|rep\.?|repealed|para\.?|paragraph|proviso|sch\.|schedule)[\s\S]*$",
        re.IGNORECASE,
    ),
    re.compile(r"\s*for\s+the\s+original[\s\S]*$", re.IGNORECASE),
]

KEYWORD_TRAIL_PATTERNS: list[re.Pattern] = [
    re.compile(r"\s*(?:ins|inserted|substituted|omitted|rep\.?|repealed)\s+by[\s\S]*$", re.IGNORECASE),
    re.compile(r"\s*explanation\s+renumbered[\s\S]*$", re.IGNORECASE),
    re.compile(r"\s*the\s+(?:words|word|letters?|figures?)\s+[^.]*?(?:omitted|inserted|substituted|ins\.?)[^.]*\.?$", re.IGNORECASE),
    re.compile(r"\s*and\s+sch[^.]*$", re.IGNORECASE),
    re.compile(r"\s*and\s+schedule[^.]*$", re.IGNORECASE),
]

MIDSTREAM_ARTIFACT_PATTERNS: list[re.Pattern] = [
    re.compile(r"\s*\d+\.,\s*for\s+\"[^\"]*\"\.?(?=\s|$)", re.IGNORECASE),
    re.compile(r"\s*\d+\.\s*[IVXLC\d]+,\s*for[^.]*\.\s*", re.IGNORECASE),
    re.compile(
        r"\s*\d+\.\s*(?:cl\.|cls\.|the words|the word|the letters?|the figures?|ins\.?|inserted|substituted|omitted|rep\.?|repealed|para\.?|paragraph|proviso|sch\.|schedule)[^.]*\.\s*",
        re.IGNORECASE,
    ),
    re.compile(r"\s*the\s+(?:words|word|letters?|figures?)\s+[^.]*?(?:omitted|inserted|substituted|ins\.?)\s*[^.]*\.\s*", re.IGNORECASE),
    re.compile(r"\s*and\s+sch\s*,?\s*for[^.]*\.\s*", re.IGNORECASE),
    re.compile(r"\s*and\s+schedule\s*,?\s*for[^.]*\.\s*", re.IGNORECASE),
]

STANDALONE_NUMBER_PATTERN: re.Pattern = re.compile(r"\s*\d+\.\s*$")
DOUBLE_NUMBER_PATTERN: re.Pattern = re.compile(r"\s*\d+\.\s*\d+\.\s*")
WHITESPACE_GAP_PATTERN: re.Pattern = re.compile(r"\s{2,}")

RESIDUAL_CHECKS: list[re.Pattern] = [
    re.compile(r"Ins\.?\s+by", re.IGNORECASE),
    re.compile(r"Inserted\s+by", re.IGNORECASE),
    re.compile(r"Substituted\s+by", re.IGNORECASE),
    re.compile(r"Omitted\s+by", re.IGNORECASE),
    re.compile(r"Rep\.?\s+by", re.IGNORECASE),
    re.compile(r"Repealed\s+by", re.IGNORECASE),
    re.compile(r"Explanation\s+renumbered", re.IGNORECASE),
    re.compile(r"for\s+the\s+original", re.IGNORECASE),
    re.compile(r"\d+\.,\s*for\s+\"", re.IGNORECASE),
    re.compile(r"\d+\.\s*[IVXLC\d]+,\s*for", re.IGNORECASE),
    re.compile(r"The\s+(?:words|word|letters?|figures?)\s+[^.]{0,80}(?:omitted|inserted|substituted|ins\.?)", re.IGNORECASE),
    re.compile(r"and\s+sch", re.IGNORECASE),
]


def normalize_brackets(value: str) -> str:
    """Clean obvious bracket residue without touching statutory insertions.

    Args:
        value: Input string with potential bracket artifacts.

    Returns:
        Cleaned string with normalized brackets.
    """
    text = value
    text = re.sub(r"\[\s+\[", "[[", text)
    text = re.sub(r"\]\s+\]", "]]", text)
    text = re.sub(r"\[\s+\]", " ", text)
    text = re.sub(r"(?<=\s)\[(?=\s)", " ", text)
    text = re.sub(r"(?<=\s)\](?=\s)", " ", text)
    return text


def remove_midstream_artifacts(value: str) -> str:
    """Remove editorial amendment artifacts that appear mid-stream in the text.

    Args:
        value: Input string with potential midstream artifacts.

    Returns:
        Cleaned string with midstream artifacts removed.
    """
    text = value
    changed = True
    while changed:
        changed = False
        for pattern in MIDSTREAM_ARTIFACT_PATTERNS:
            updated = pattern.sub(" ", text)
            if updated != text:
                text = updated.strip()
                changed = True
        updated = DOUBLE_NUMBER_PATTERN.sub(" ", text)
        if updated != text:
            text = updated.strip()
            changed = True
    return text


def strip_trailing_artifacts(value: str) -> str:
    """Remove editorial amendment artifacts that trail at the end of the text.

    Args:
        value: Input string with potential trailing artifacts.

    Returns:
        Cleaned string with trailing artifacts removed.
    """
    text = value
    changed = True
    while changed:
        changed = False
        for pattern in NUMBERED_ARTIFACT_PATTERNS + KEYWORD_TRAIL_PATTERNS:
            updated = pattern.sub("", text)
            if updated != text:
                text = updated.strip()
                changed = True
                break
    text = STANDALONE_NUMBER_PATTERN.sub("", text).strip()
    return text


def clean_full_text(value: str) -> str:
    """Clean the full_text field of an IPC section by removing editorial artifacts.

    Args:
        value: Raw full_text string.

    Returns:
        Cleaned full_text string.
    """
    stripped = value.strip()
    if stripped.upper() == "REPEALED":
        return "REPEALED"
    stripped = normalize_brackets(stripped)
    stripped = remove_midstream_artifacts(stripped)
    stripped = strip_trailing_artifacts(stripped)
    stripped = normalize_brackets(stripped)
    stripped = WHITESPACE_GAP_PATTERN.sub(" ", stripped)
    return stripped.strip() or value.strip()


def fields_except_full_text(record: Dict[str, Any]) -> Dict[str, Any]:
    clone = dict(record)
    clone.pop("full_text", None)
    return clone


def main() -> None:
    if not DRAFT_PATH.exists():
        raise FileNotFoundError(f"Missing draft dataset at {DRAFT_PATH}")

    try:
        original_data: List[Dict[str, Any]] = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse draft dataset: %s", exc)
        raise

    cleaned_data: List[Dict[str, Any]] = []
    modifications = 0

    for entry in original_data:
        new_entry = deepcopy(entry)
        cleaned_text = clean_full_text(entry["full_text"])
        if cleaned_text != entry["full_text"]:
            modifications += 1
        new_entry["full_text"] = cleaned_text
        cleaned_data.append(new_entry)

    try:
        OUTPUT_PATH.write_text(json.dumps(cleaned_data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        logger.info("Cleaned data written to %s", OUTPUT_PATH)
    except IOError as exc:
        logger.error("Failed to write cleaned data: %s", exc)
        raise

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        schema_valid = True
        schema_error = ""
        try:
            validator.validate(cleaned_data)
        except Exception as exc:
            schema_valid = False
            schema_error = str(exc)
    except Exception as exc:
        logger.error("Schema validation setup failed: %s", exc)
        schema_valid = False
        schema_error = str(exc)

    section_numbers = [item["section_number"] for item in original_data]
    ordering_preserved = section_numbers == [item["section_number"] for item in cleaned_data]
    unique_sections = len(section_numbers) == len(set(section_numbers))
    no_other_fields_modified = all(
        fields_except_full_text(orig) == fields_except_full_text(new)
        for orig, new in zip(original_data, cleaned_data)
    )
    non_empty_full_text = all(
        isinstance(item["full_text"], str) and bool(item["full_text"].strip())
        for item in cleaned_data
    )

    residual_hits = []
    for entry in cleaned_data:
        text = entry["full_text"]
        if text == "REPEALED":
            continue
        for pattern in RESIDUAL_CHECKS:
            if pattern.search(text):
                residual_hits.append(entry["section_number"])
                break

    report = {
        "total_records": len(cleaned_data),
        "modified_full_text_entries": modifications,
        "schema_valid": schema_valid,
        "ordering_preserved": ordering_preserved,
        "unique_section_numbers": unique_sections,
        "no_empty_full_text": non_empty_full_text,
        "no_other_fields_modified": no_other_fields_modified,
        "editorial_artifacts_removed": not residual_hits,
    }
    if not schema_valid:
        report["schema_error"] = schema_error
    if residual_hits:
        report["residual_artifact_sections"] = residual_hits[:10]

    logger.info(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
