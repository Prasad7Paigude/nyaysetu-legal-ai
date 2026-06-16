import json
import re
import logging
from pathlib import Path
from typing import Any, Optional

import requests
from jsonschema import Draft202012Validator

from config.settings import OPENROUTER_API_KEY, DATA_DIR

logger = logging.getLogger(__name__)

# =========================
# CONFIG
# =========================

MODEL: str = "meta-llama/llama-3-8b-instruct"

HEADERS: dict[str, str] = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost",
    "Content-Type": "application/json"
}

# =========================
# LOAD INPUT + FILE PATHS
# =========================

INPUT_PATH: Path = DATA_DIR / "ipc_cleaned_v4.json"
SCHEMA_PATH: Path = DATA_DIR / "ipc_enriched_v1.schema.json"
DRAFT_PATH: Path = DATA_DIR / "ipc_enriched_v1_draft.json"
FAILED_LOG_PATH: Path = DATA_DIR / "failed_sections.log"

try:
    with INPUT_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        schema = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as exc:
    logger.error("Failed to load input files: %s", exc)
    raise

validator = Draft202012Validator(schema)
item_validator = Draft202012Validator(schema["items"])

# =========================
# EDITORIAL NOISE PATTERNS
# =========================

EDITORIAL_NOISE_PATTERNS: list[str] = [
    r"\bthe act has been amended\b",
    r"\bsubs?\.\s*by\s*act\b",
    r"\brep\.?\s*,?\s*by\s*",
    r"\bins\.?\s*by\s*act\b",
    r"\bibid\.?\b",
    r"\bomitted by act\b",
    r"\breg\.\s*\d+\s*of\b",
    r"\bfor\s+\"the states\"\b"
]

TEMPLATE_SUMMARY_PATTERNS: list[str] = [
    r"^it clarifies the legal effect of",
    r"^it defines the meaning of",
    r"^it explains how",
    r"^this provision addresses",
    r"^this section deals with the",
    r"^this provision deals with",
    r"^this law deals with",
    r"^this rule addresses"
]

FRAGMENT_KEYWORD_PATTERNS: list[str] = [
    r"^india\s+except$",
    r"^indian\s+penal$",
    r"^whole\s+india$",
    r"^person\s+said$",
    r"^word\s+\w+$",
    r"^words\s+\w+$",
    r"^sense\s+expression$",
    r"^male\s+female$",
    r"^penal\s+code$",
    r"^singular\s+plural$",
    r"^act\s+shall$",
    r"^every\s+person$",
    r"^person\s+person$",
    r"^shall\s+be$"
]

# =========================
# PROMPTS
# =========================

system_prompt: str = """You are a legal data enrichment engine for the Indian Penal Code.

Your task: given an IPC section, produce a structured JSON record with a high-quality
summary and keywords suitable for semantic search and citizen-facing legal retrieval.

SUMMARY RULES:
- Write 2 to 4 complete, fluent sentences.
- Explain what the provision actually does in plain English.
- Do NOT start with template patterns like "It clarifies the legal effect of...",
  "This provision addresses...", "It defines the meaning of...", "It explains how...".
- Start each summary differently. Vary sentence structure.
- Do NOT hallucinate legal meaning beyond what the text says.
- Do NOT mention "IPC" or "Section" by number.

KEYWORD RULES:
- Produce exactly 5 to 8 keywords.
- Each keyword must be a multi-word phrase (at least 3 words, ideally 3-5 words).
- Keywords must be lowercase.
- Keywords must be natural-language phrases a citizen might type when searching for
  legal help. Examples of GOOD keywords:
    "punishment for crimes committed in india"
    "definition of public servant under criminal law"
    "what counts as movable property in law"
    "gender neutral language in criminal code"
    "applicability of criminal code across india"
- Do NOT produce mechanical token fragments like "india except", "sense expression",
  "male female", "indian penal", "whole india".
- Do NOT produce overly generic phrases like "criminal law", "legal provision".
- Each keyword should capture a distinct aspect of the provision.

OFFENCE_TYPE must be one of:
Property Crime | Violent Crime | Fraud / Cheating | Sexual Offence |
Public Servant Offence | Abetment | General Exception | Punishment | Other

FULL_TEXT RULES:
- Include ONLY the statutory wording of the provision.
- Remove all editorial amendments, footnotes, and amendment numbering fragments
  (e.g., "The Act has been amended...", "Subs. by Act...", "Rep. by...", "ibid.").
- Preserve illustrations and explanations that are part of the statutory text.

Output ONLY valid JSON. No markdown, no explanation outside the JSON."""


def call_llm(section: dict[str, Any], attempt: int = 1) -> dict[str, Any]:
    """Call the OpenRouter LLM to enrich a single IPC section.

    Args:
        section: Source section data.
        attempt: Attempt number (for temperature variation on retry).

    Returns:
        The LLM API response JSON.

    Raises:
        requests.RequestException: If the API call fails.
    """
    user_prompt = f"""Transform this IPC section into structured enrichment JSON.

Input:
  law_type: IPC
  section_number: {section["section_number"]}
  section_title: {section["section_title"]}
  full_text: {section["bare_text"]}

Return JSON:
{{
  "law_type": "IPC",
  "section_number": "{section["section_number"]}",
  "section_title": "{section["section_title"]}",
  "full_text": "<statutory text only, no amendments>",
  "summary": "<2-4 fluent sentences, plain English, no template openings>",
  "keywords": ["<5-8 natural multi-word citizen-search phrases, at least 3 words each>"],
  "offence_type": "<one of the allowed categories>"
}}

CRITICAL KEYWORD GUIDANCE:
- Think about what a citizen would type into a search engine if they had a legal
  problem related to this section.
- Each keyword phrase must be at least 3 words long.
- Good: "applicability of criminal code across india"
- Bad: "india except" or "penal code" or "criminal law"

CRITICAL SUMMARY GUIDANCE:
- Even for short definitional sections, you MUST write at least 2 complete sentences.
- Explain the definition AND describe when/how it matters in practice.

Return ONLY the JSON object."""

    temp = 0.4 if attempt == 1 else 0.55

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temp,
        "top_p": 1,
        "max_tokens": 1200
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.error("LLM API call failed on attempt %d: %s", attempt, exc)
        raise


# =========================
# TEXT CLEANING UTILITIES
# =========================

def normalize_space(text: str) -> str:
    """Normalize whitespace in a string.

    Args:
        text: Input text.

    Returns:
        Text with normalized whitespace.
    """
    text = str(text)
    text = text.replace("\u200b", "").replace("\ufeff", "")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text


def clean_full_text_statutory(text: str) -> str:
    """Strip editorial amendment tails and noise from statutory text.

    Args:
        text: Raw statutory text.

    Returns:
        Cleaned statutory text.
    """
    cleaned = normalize_space(text)

    tail_markers = [
        r"\bThe\s+Act\s+has\s+been\s+amended\b",
        r"\bRep\.?\s*,?\s*by\b",
        r"\bSubs?\.?\s*by\s*Act\b",
        r"\bIns\.?\s*by\s*Act\b",
        r"\bibid\.?\b",
        r"\bomitted\s+by\s+Act\b"
    ]
    for marker in tail_markers:
        m = re.search(marker, cleaned, flags=re.IGNORECASE)
        if m:
            cleaned = cleaned[:m.start()].rstrip(" ,;:-")
            break

    cleaned = re.sub(r"\b\d+\.?\s*(for|ins\.?|rep\.?|subs\.?|ibid\.?)[^.;:]*[.;:]?", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\*\s*\*\s*\*\s*\*+", " ", cleaned)
    cleaned = normalize_space(cleaned)

    return cleaned if len(cleaned) >= 10 else normalize_space(text)


def sentence_count(text: str) -> int:
    parts = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    return len(parts)


# =========================
# QUALITY CHECKS (REJECTION-BASED)
# =========================

def is_fragment_keyword(kw: str) -> bool:
    """Return True if the keyword looks like a mechanical fragment.

    Args:
        kw: Keyword string to check.

    Returns:
        True if the keyword is a fragment pattern.
    """
    kw = kw.strip().lower()
    words = kw.split()
    if len(words) < 2:
        return True

    for pattern in FRAGMENT_KEYWORD_PATTERNS:
        if re.match(pattern, kw):
            return True

    if len(words) == 2 and all(len(w) <= 4 for w in words):
        return True

    return False


def is_generic_keyword(kw: str) -> bool:
    """Return True if the keyword is too generic to be useful for retrieval.

    Args:
        kw: Keyword string to check.

    Returns:
        True if the keyword is generic.
    """
    kw = kw.strip().lower()
    generic_phrases = {
        "criminal law", "indian law", "legal provision", "penal code",
        "law and order", "legal system", "criminal justice",
        "legal framework", "rule of law", "criminal code",
        "law enforcement", "legal rights"
    }
    return kw in generic_phrases


def is_template_summary(summary: str) -> bool:
    """Return True if the summary follows a template pattern.

    Args:
        summary: Summary string to check.

    Returns:
        True if the summary starts with a template pattern.
    """
    summary_lower = summary.strip().lower()
    for pattern in TEMPLATE_SUMMARY_PATTERNS:
        if re.match(pattern, summary_lower):
            return True
    return False


def keywords_quality_ok(keywords: list[str]) -> tuple[bool, str]:
    """Check that all keywords meet quality standards.

    Args:
        keywords: List of keyword strings.

    Returns:
        Tuple of (ok, reason).
    """
    if not isinstance(keywords, list):
        return False, "keywords is not a list"
    if len(keywords) < 5 or len(keywords) > 8:
        return False, f"keyword count {len(keywords)} outside 5-8 range"
    if len(set(keywords)) != len(keywords):
        return False, "duplicate keywords"

    for kw in keywords:
        if not isinstance(kw, str) or kw.strip() == "":
            return False, "empty or non-string keyword"
        if len(kw.split()) < 2:
            return False, f"single-word keyword: '{kw}'"
        if len(kw) < 3:
            return False, f"keyword too short: '{kw}'"
        if is_fragment_keyword(kw):
            return False, f"fragment keyword: '{kw}'"
        if is_generic_keyword(kw):
            return False, f"generic keyword: '{kw}'"

    return True, "OK"


def summary_quality_ok(summary: str) -> tuple[bool, str]:
    """Check that the summary meets quality standards.

    Args:
        summary: Summary string to check.

    Returns:
        Tuple of (ok, reason).
    """
    if not isinstance(summary, str) or len(summary) < 50:
        return False, "summary too short"
    sc = sentence_count(summary)
    if sc < 2:
        return False, "summary has fewer than 2 sentences"
    if sc > 4:
        return False, "summary has more than 4 sentences"
    if is_template_summary(summary):
        return False, "summary uses template opening pattern"
    return True, "OK"


# =========================
# NORMALIZATION LAYER (MINIMAL)
# =========================

def normalize_record(record: dict[str, Any], source_section: dict[str, Any]) -> dict[str, Any]:
    """Minimal normalization of an enriched record.

    Does NOT generate or repair keywords/summaries. Only cleans formatting
    and enforces source-of-truth fields.

    Args:
        record: The LLM-generated record.
        source_section: The original source section data.

    Returns:
        Normalized record.
    """
    normalized = record.copy()

    normalized["law_type"] = "IPC"
    normalized["section_number"] = str(source_section.get("section_number", "")).strip()
    normalized["section_title"] = str(source_section.get("section_title", "")).strip()
    normalized["full_text"] = clean_full_text_statutory(source_section.get("bare_text", ""))

    raw_keywords = normalized.get("keywords", [])
    cleaned = []
    seen = set()
    for kw in raw_keywords:
        if not isinstance(kw, str):
            continue
        kw = normalize_space(kw).lower().strip()
        kw = re.sub(r"[^a-z0-9\s\-]", " ", kw)
        kw = normalize_space(kw)
        if kw and kw not in seen:
            seen.add(kw)
            cleaned.append(kw)

    normalized["keywords"] = cleaned[:8]
    normalized["summary"] = normalize_space(normalized.get("summary", ""))

    allowed_offence_types = {
        "Property Crime", "Violent Crime", "Fraud / Cheating",
        "Sexual Offence", "Public Servant Offence", "Abetment",
        "General Exception", "Punishment", "Other"
    }
    offence_raw = str(normalized.get("offence_type", "")).strip()
    matched = None
    for option in allowed_offence_types:
        if offence_raw.lower() == option.lower():
            matched = option
            break
    normalized["offence_type"] = matched if matched else "Other"

    return normalized


# =========================
# VALIDATION
# =========================

def has_no_empty_fields(record: dict[str, Any]) -> bool:
    for value in record.values():
        if value is None:
            return False
        if isinstance(value, str) and value.strip() == "":
            return False
    return True


def validate_enriched(record: dict[str, Any], source_section: dict[str, Any]) -> tuple[bool, str]:
    """Full validation: schema + quality checks.

    Args:
        record: The enriched record to validate.
        source_section: The original source section.

    Returns:
        Tuple of (ok, reason).
    """
    errors = sorted(item_validator.iter_errors(record), key=lambda e: e.path)
    if errors:
        return False, f"schema: {errors[0].message}"

    if not has_no_empty_fields(record):
        return False, "record contains empty fields"

    if any(re.search(p, record.get("full_text", ""), flags=re.IGNORECASE)
           for p in EDITORIAL_NOISE_PATTERNS):
        return False, "full_text contains editorial amendment noise"

    kw_ok, kw_reason = keywords_quality_ok(record.get("keywords", []))
    if not kw_ok:
        return False, f"keyword quality: {kw_reason}"

    sum_ok, sum_reason = summary_quality_ok(record.get("summary", ""))
    if not sum_ok:
        return False, f"summary quality: {sum_reason}"

    return True, "OK"


# =========================
# PARSE HELPERS
# =========================

def repair_json_string(text: str) -> str:
    """Attempt to fix common LLM JSON issues: unescaped quotes inside string values.

    Args:
        text: Potentially malformed JSON string.

    Returns:
        Repaired JSON string.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return text
    candidate = text[start:end + 1]

    candidate = candidate.replace("\u201c", '"').replace("\u201d", '"')
    candidate = candidate.replace("\u2018", "'").replace("\u2019", "'")

    lines = candidate.split("\n")
    fixed_lines = []
    for line in lines:
        m = re.match(r'^(\s*"[^"]+"\s*:\s*")(.*)(",?\s*)$', line)
        if m:
            prefix, value, suffix = m.group(1), m.group(2), m.group(3)
            value = value.replace('\\"', '\x00')
            value = value.replace('"', '\\"')
            value = value.replace('\x00', '\\"')
            fixed_lines.append(prefix + value + suffix)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def extract_json_object(text: str) -> Any:
    """Extract and parse a JSON object from text that may contain surrounding content.

    Args:
        text: Text that may contain a JSON object.

    Returns:
        Parsed JSON object.

    Raises:
        json.JSONDecodeError: If no valid JSON object is found.
    """
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    repaired = repair_json_string(text)
    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        pass

    raise json.JSONDecodeError("No JSON object found", text, 0)


# =========================
# BATCH PIPELINE
# =========================

START_SECTION: int = 1
END_SECTION: int = 100

if FAILED_LOG_PATH.exists():
    FAILED_LOG_PATH.unlink()

draft_records: list[dict[str, Any]] = []

source_sections = [
    row for row in data
    if START_SECTION <= int(re.match(r"\d+", str(row.get("section_number", "0"))).group(0)) <= END_SECTION
]

processed = 0
added = 0

for section in source_sections:
    processed += 1
    section_number = str(section.get("section_number", "")).strip()

    success = False
    last_error = "unknown error"

    for attempt in range(1, 4):
        try:
            result = call_llm(section, attempt=attempt)
            if "choices" not in result or not result["choices"]:
                raise ValueError(f"LLM response missing choices: {result}")

            raw_output = result["choices"][0]["message"]["content"]
            parsed = extract_json_object(raw_output)
            normalized = normalize_record(parsed, section)

            is_valid, reason = validate_enriched(normalized, section)
            if not is_valid:
                last_error = reason
                logger.info("[%d/%d] %s: attempt %d rejected (%s)", processed, len(source_sections), section_number, attempt, reason)
                continue

            draft_records.append(normalized)
            with DRAFT_PATH.open("w", encoding="utf-8") as f:
                json.dump(draft_records, f, ensure_ascii=False, indent=2)

            added += 1
            success = True
            logger.info("[%d/%d] %s: accepted (total=%d)", processed, len(source_sections), section_number, added)
            break

        except Exception as exc:
            last_error = str(exc)
            logger.error("[%d/%d] %s: attempt %d error (%s)", processed, len(source_sections), section_number, attempt, exc)

    if not success:
        with FAILED_LOG_PATH.open("a", encoding="utf-8") as logf:
            logf.write(f"{section_number} | {last_error}\n")
        logger.warning("[%d/%d] %s: FAILED after retry -> logged", processed, len(source_sections), section_number)

logger.info("\n" + "=" * 60)
logger.info("BATCH COMPLETE")
logger.info("Sections processed: %d", processed)
logger.info("Records accepted: %d", added)
logger.info("Records rejected: %d", processed - added)
logger.info("Draft: %s", DRAFT_PATH)
logger.info("=" * 60)

# =========================
# POST-RUN VERIFICATION
# =========================

logger.info("\n--- POST-RUN VERIFICATION ---\n")

schema_valid = True
try:
    validator.validate(draft_records)
except Exception:
    schema_valid = False

no_fragmented_keywords = all(
    not any(is_fragment_keyword(kw) for kw in r.get("keywords", []))
    for r in draft_records
)

keywords_semantically_natural = all(
    keywords_quality_ok(r.get("keywords", []))[0]
    for r in draft_records
)

summaries_non_template_style = all(
    not is_template_summary(r.get("summary", ""))
    for r in draft_records
)
summary_texts = [r.get("summary", "") for r in draft_records]
if len(summary_texts) > 1 and len(set(summary_texts)) < len(summary_texts) * 0.8:
    summaries_non_template_style = False

no_editorial_noise_in_full_text = all(
    not any(re.search(p, r.get("full_text", ""), flags=re.IGNORECASE)
            for p in EDITORIAL_NOISE_PATTERNS)
    for r in draft_records
)

logger.info("schema_valid=%s", schema_valid)
logger.info("no_fragmented_keywords=%s", no_fragmented_keywords)
logger.info("keywords_semantically_natural=%s", keywords_semantically_natural)
logger.info("summaries_non_template_style=%s", summaries_non_template_style)
logger.info("no_editorial_noise_in_full_text=%s", no_editorial_noise_in_full_text)

if draft_records:
    logger.info("\n--- SAMPLE RECORD (first accepted) ---")
    logger.info(json.dumps(draft_records[0], indent=2, ensure_ascii=False))
