"""
Phase 4 – Stability & Stress Testing
Covers all 8 test categories for the RAG-based IPC prediction system.
"""

import json
import time
import logging
from typing import Any

from ipc_prediction.ipc_reasoning_engine import predict_ipc_section, _fallback_response, SIMILARITY_THRESHOLD
from ipc_prediction.llm_validation_guard import validate_llm_response, MIN_CONFIDENCE
from ipc_prediction.retrieve_sections import _retrieve_with_scores

logger = logging.getLogger(__name__)

PASS: str = "PASS"
FAIL: str = "FAIL"
FALLBACK_EXPLANATION: str = "The described incident does not clearly fall under a specific IPC section."

results: list[tuple[str, str, str]] = []


def record(category: str, name: str, passed: bool, detail: str = "") -> None:
    """Record a test result and log it.

    Args:
        category: Test category identifier.
        name: Test name.
        passed: Whether the test passed.
        detail: Optional failure detail.
    """
    status = PASS if passed else FAIL
    results.append((category, name, status))
    mark = "+" if passed else "X"
    msg = f"  [{mark}] {name}"
    if detail and not passed:
        msg += f"  -- {detail}"
    logger.info(msg)


def test_category_1() -> dict[str, Any]:
    """Test CAT1: Strong IPC case."""
    logger.info("\n=== CATEGORY 1: Strong IPC Case ===")
    text = "He cheated me by taking money and not delivering the goods."
    out = predict_ipc_section(text)

    record("CAT1", "Returns dict", isinstance(out, dict))
    record("CAT1", "predicted_sections present", "predicted_sections" in out)
    record("CAT1", "confidence present", "confidence" in out)
    record("CAT1", "explanation present", "explanation" in out)
    record("CAT1", "title present", "title" in out)

    sections = out.get("predicted_sections", [])
    conf = out.get("confidence", -1)
    expl = out.get("explanation", "")
    title = out.get("title", "")

    has_section = isinstance(sections, list) and len(sections) == 1
    record("CAT1", "Exactly one section", has_section)

    if has_section:
        record("CAT1", "Section is string", isinstance(sections[0], str) and len(sections[0]) > 0)
    else:
        record("CAT1", "Section is string", False, f"sections={sections}")

    record("CAT1", "Confidence is float", isinstance(conf, (int, float)))
    record("CAT1", "Confidence 0.3-1.0", 0.3 <= conf <= 1.0, f"conf={conf}")
    record("CAT1", "Explanation non-empty", isinstance(expl, str) and len(expl.strip()) > 0)
    record("CAT1", "Title non-empty", isinstance(title, str) and len(title.strip()) > 0, f"title={repr(title)}")
    record("CAT1", "No extra keys", set(out.keys()) == {"predicted_sections", "confidence", "explanation", "title"}, f"keys={set(out.keys())}")

    logger.info("  >> Section: %s, Confidence: %s", sections, conf)
    logger.info("  >> Title: %s", title)
    logger.info("  >> Explanation: %s...", expl[:120] if expl else "")
    return out


def test_category_2() -> None:
    """Test CAT2: Low similarity case."""
    logger.info("\n=== CATEGORY 2: Low Similarity Case ===")
    text = "The weather is nice today."
    out = predict_ipc_section(text)

    sections = out.get("predicted_sections", ["NOT_EMPTY"])
    conf = out.get("confidence", -1)
    expl = out.get("explanation", "")

    record("CAT2", "Returns dict", isinstance(out, dict))
    record("CAT2", "Empty sections", sections == [])
    record("CAT2", "Confidence is 0.0", conf == 0.0, f"conf={conf}")
    record("CAT2", "Fallback explanation", expl == FALLBACK_EXPLANATION, f"expl={expl[:80]}")
    record("CAT2", "Title empty", out.get("title", None) == "", f"title={repr(out.get('title'))}")

    ranked = _retrieve_with_scores(text)
    top_sim = float(ranked[0][1]) if ranked else 0.0
    record("CAT2", "Top sim < threshold", top_sim < SIMILARITY_THRESHOLD, f"top_sim={top_sim:.4f}")
    logger.info("  >> Top similarity: %.4f (threshold: %s)", top_sim, SIMILARITY_THRESHOLD)


def test_category_3() -> None:
    """Test CAT3: Ambiguous case."""
    logger.info("\n=== CATEGORY 3: Ambiguous Case ===")
    text = "They argued loudly in public."
    out = predict_ipc_section(text)

    sections = out.get("predicted_sections", [])
    conf = out.get("confidence", -1)
    expl = out.get("explanation", "")
    title = out.get("title", "")

    record("CAT3", "Returns dict", isinstance(out, dict))
    record("CAT3", "Sections list", isinstance(sections, list))
    record("CAT3", "Sections len 0 or 1", len(sections) <= 1)

    if sections:
        record("CAT3", "Confidence >= 0.3", conf >= 0.3, f"conf={conf}")
        record("CAT3", "Explanation non-empty", len(expl.strip()) > 0)
        record("CAT3", "No hallucinated section", isinstance(sections[0], str) and sections[0].strip() != "")
        logger.info("  >> Predicted: %s, Confidence: %s, Title: %s", sections[0], conf, title)
    else:
        record("CAT3", "Fallback confidence", conf == 0.0, f"conf={conf}")
        record("CAT3", "Fallback explanation", expl == FALLBACK_EXPLANATION)
        logger.info("  >> Fallback triggered")


def test_category_4() -> None:
    """Test CAT4: Repeatability test (10 runs)."""
    logger.info("\n=== CATEGORY 4: Repeatability Test (10 runs) ===")
    text = "He cheated me by taking money and not delivering the goods."
    outputs = []
    for i in range(10):
        out = predict_ipc_section(text)
        outputs.append(out)
        logger.info("  Run %d/10 --> Section: %s, Conf: %s", i + 1, out.get('predicted_sections'), out.get('confidence'))

    first = outputs[0]
    all_same_section = all(o.get("predicted_sections") == first.get("predicted_sections") for o in outputs)
    all_same_conf = all(o.get("confidence") == first.get("confidence") for o in outputs)
    all_same_title = all(o.get("title") == first.get("title") for o in outputs)
    all_same_expl = all(o.get("explanation") == first.get("explanation") for o in outputs)

    record("CAT4", "Section identical x10", all_same_section)
    record("CAT4", "Confidence identical x10", all_same_conf)
    record("CAT4", "Title identical x10", all_same_title)
    record("CAT4", "Explanation identical x10", all_same_expl)


def test_category_5() -> None:
    """Test CAT5: Invalid LLM JSON simulation."""
    logger.info("\n=== CATEGORY 5: Invalid LLM JSON Simulation ===")
    allowed = ["378", "420", "452"]
    fb_guard = {"predicted_sections": [], "confidence": 0.0, "explanation": FALLBACK_EXPLANATION}

    r = validate_llm_response("This is not JSON", allowed)
    record("CAT5", "Non-JSON to fallback", r == fb_guard)

    r = validate_llm_response("[1, 2, 3]", allowed)
    record("CAT5", "Array JSON to fallback", r == fb_guard)

    r = validate_llm_response('{"predicted_sections": ["378"]}', allowed)
    record("CAT5", "Missing keys to fallback", r == fb_guard)

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": 0.8, "explanation": "theft", "extra": true}', allowed)
    expected_extra = {"predicted_sections": ["378"], "confidence": 0.8, "explanation": "theft"}
    record("CAT5", "Extra keys to passes", r == expected_extra, f"got={r}")

    r = validate_llm_response('{"predicted_sections": ["378", "420"], "confidence": 0.8, "explanation": "theft"}', allowed)
    record("CAT5", "Multi-section to fallback", r == fb_guard)

    r = validate_llm_response('{"predicted_sections": ["999"], "confidence": 0.8, "explanation": "theft"}', allowed)
    record("CAT5", "Section not allowed to fallback", r == fb_guard)

    r = validate_llm_response('{"predicted_sections": [" 378 "], "confidence": 0.8, "explanation": "theft"}', allowed)
    expected_ws = {"predicted_sections": ["378"], "confidence": 0.8, "explanation": "theft"}
    record("CAT5", "Whitespace section to passes", r == expected_ws, f"got={r}")

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": "0.8", "explanation": "theft"}', allowed)
    record("CAT5", "String confidence to fallback", r == fb_guard)

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": 0.8, "explanation": ""}', allowed)
    record("CAT5", "Empty explanation to fallback", r == fb_guard)

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": 0.8, "explanation": "This involves theft."}', allowed)
    expected_valid = {"predicted_sections": ["378"], "confidence": 0.8, "explanation": "This involves theft."}
    record("CAT5", "Valid JSON to passes", r == expected_valid, f"got={r}")

    r = validate_llm_response('```json\n{"predicted_sections": ["378"], "confidence": 0.8, "explanation": "theft"}\n```', allowed)
    expected_md = {"predicted_sections": ["378"], "confidence": 0.8, "explanation": "theft"}
    record("CAT5", "Markdown-wrapped to passes", r == expected_md, f"got={r}")

    r = validate_llm_response("", allowed)
    record("CAT5", "Empty string to fallback", r == fb_guard)


def test_category_6() -> None:
    """Test CAT6: API failure simulation."""
    logger.info("\n=== CATEGORY 6: API Failure Simulation ===")

    from ipc_prediction import ipc_reasoning_engine as eng

    original_url = eng.GEMINI_API_URL

    eng.GEMINI_API_URL = "https://localhost:1/nonexistent"
    r = eng.predict_ipc_section("Someone stole my wallet from my bag while I was on the bus.")
    record("CAT6", "Bad URL to fallback", r.get("predicted_sections") == [] and r.get("confidence") == 0.0)

    eng.GEMINI_API_URL = "not-a-url"
    r = eng.predict_ipc_section("Someone stole my wallet from my bag while I was on the bus.")
    record("CAT6", "Invalid URL to fallback", r.get("predicted_sections") == [] and r.get("confidence") == 0.0)

    eng.GEMINI_API_URL = original_url
    record("CAT6", "URL restored", eng.GEMINI_API_URL == original_url)


def test_category_7() -> None:
    """Test CAT7: Empty / short input."""
    logger.info("\n=== CATEGORY 7: Empty / Short Input ===")

    for label, text in [("Empty string", ""), ("Whitespace only", "   "), ("Very short", "Hi"), ("Under 10 chars", "Help me")]:
        out = predict_ipc_section(text)
        is_fallback = out.get("predicted_sections") == [] and out.get("confidence") == 0.0
        record("CAT7", f"{label} to fallback", is_fallback, f"out={out}")


def test_category_8() -> None:
    """Test CAT8: Confidence boundary test."""
    logger.info("\n=== CATEGORY 8: Confidence Boundary Test ===")
    allowed = ["378", "420"]
    fb = _fallback_response()
    fb_guard = {k: v for k, v in fb.items() if k != "title"}

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": 0.29, "explanation": "theft"}', allowed)
    record("CAT8", "conf=0.29 to fallback", r == fb_guard, f"r={r}")

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": 0.30, "explanation": "theft"}', allowed)
    record("CAT8", "conf=0.30 to passes", r.get("predicted_sections") == ["378"] and r.get("confidence") == 0.3, f"r={r}")

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": 1.2, "explanation": "theft"}', allowed)
    record("CAT8", "conf=1.2 to clamped 1.0", r.get("confidence") == 1.0 and r.get("predicted_sections") == ["378"], f"r={r}")

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": -0.5, "explanation": "theft"}', allowed)
    record("CAT8", "conf=-0.5 to fallback", r == fb_guard, f"r={r}")

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": 0.0, "explanation": "theft"}', allowed)
    record("CAT8", "conf=0.0 to fallback", r == fb_guard, f"r={r}")

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": NaN, "explanation": "theft"}', allowed)
    record("CAT8", "conf=NaN to fallback", r == fb_guard, f"r={r}")

    r = validate_llm_response('{"predicted_sections": ["378"], "confidence": Infinity, "explanation": "theft"}', allowed)
    record("CAT8", "conf=Infinity to fallback", r == fb_guard, f"r={r}")


def main() -> int:
    logger.info("=" * 60)
    logger.info("PHASE 4 -- STABILITY & STRESS TESTING")
    logger.info("=" * 60)

    test_category_5()
    test_category_7()
    test_category_8()
    test_category_6()
    cat1_out = test_category_1()
    test_category_2()
    test_category_3()
    test_category_4()

    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    total = len(results)
    passed = sum(1 for _, _, s in results if s == PASS)
    failed = sum(1 for _, _, s in results if s == FAIL)
    logger.info("Total: %d  |  Passed: %d  |  Failed: %d", total, passed, failed)

    if failed > 0:
        logger.info("\nFAILED TESTS:")
        for cat, name, status in results:
            if status == FAIL:
                logger.info("  [%s] %s", cat, name)

    logger.info("\n%s", "ALL TESTS PASSED -- SYSTEM DEMO SAFE" if failed == 0 else "SOME TESTS FAILED -- REVIEW REQUIRED")
    logger.info("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
