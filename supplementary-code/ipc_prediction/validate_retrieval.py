"""
DAY 2 – STEP 6: Deterministic Retrieval Validation Suite

Validates retrieve_sections() with 20 deterministic test cases.
All expected section_numbers are verified to exist in ipc_enriched_v1.json.
"""

import logging
from typing import Any

from ipc_prediction.retrieve_sections import retrieve_sections

logger = logging.getLogger(__name__)

TEST_CASES: list[dict[str, str]] = [
    {"description": "The accused threatened to kill the victim if they did not withdraw their complaint against him.", "expected_section": "503"},
    {"description": "A man punched another person in the face during an argument, causing injuries.", "expected_section": "351"},
    {"description": "The accused deceived the victim into transferring money by falsely promising employment.", "expected_section": "420"},
    {"description": "An employee misappropriated company funds entrusted to him for business purposes.", "expected_section": "405"},
    {"description": "The accused entered the victim's house without permission with intent to commit an offence.", "expected_section": "452"},
    {"description": "The accused made threatening gestures and attempted to strike the victim with a stick.", "expected_section": "351"},
    {"description": "A person instigated and helped another to commit a crime by providing weapons.", "expected_section": "109"},
    {"description": "The accused created a fake signature on a property document to claim ownership.", "expected_section": "463"},
    {"description": "The accused threatened to release private photos unless the victim paid money.", "expected_section": "383"},
    {"description": "The accused intentionally damaged the victim's car by scratching it with a key.", "expected_section": "425"},
    {"description": "The accused blocked the victim's path and prevented them from leaving the room.", "expected_section": "339"},
    {"description": "The accused published false and defamatory statements about the victim in a newspaper harming their reputation.", "expected_section": "501"},
    {"description": "Two or more persons agreed to do an illegal act constituting criminal conspiracy under law.", "expected_section": "120B"},
    {"description": "A person performed obscene gestures in a public place causing annoyance to others.", "expected_section": "294"},
    {"description": "A government officer knowingly disobeyed a lawful order from a superior authority.", "expected_section": "166"},
    {"description": "The attacker struck the victim with an iron rod causing permanent disability.", "expected_section": "324"},
    {"description": "The accused stabbed the victim multiple times intending to kill, but the victim survived.", "expected_section": "307"},
    {"description": "A servant stole valuable items from his employer's house while employed there.", "expected_section": "381"},
    {"description": "The accused knowingly used a forged certificate to obtain a job.", "expected_section": "471"},
    {"description": "The accused sent threatening messages to the victim saying he would harm their family.", "expected_section": "503"},
]

EDGE_CASES: list[str] = [
    "",
    "   ",
    (
        "The accused repeatedly issued threats over several months, forced entry into a property, "
        "caused physical injury during confrontation, and removed financial documents and valuables "
        "without consent, while witnesses observed intimidation, damage to property, and attempted "
        "destruction of records before law enforcement intervention. The victim suffered both physical "
        "and psychological trauma requiring medical treatment and counseling. Multiple witnesses have "
        "provided statements corroborating the sequence of events and identifying the accused."
    ),
    "1234567890 987654321",
]


def run_test_cases() -> tuple[int, int]:
    """Run all deterministic test cases.

    Returns:
        Tuple of (passed_count, failed_count).
    """
    passed = 0
    failed = 0

    for i, test in enumerate(TEST_CASES, start=1):
        description = test["description"]
        expected = test["expected_section"]

        results = retrieve_sections(description)
        returned_sections = [r["section_number"] for r in results]

        if expected in returned_sections:
            logger.info("[PASS] Test %02d: Section %s found in Top-5", i, expected)
            passed += 1
        else:
            logger.info("[FAIL] Test %02d: Section %s NOT found (got: %s)", i, expected, returned_sections)
            failed += 1

    return passed, failed


def run_edge_case_tests() -> tuple[int, int]:
    """Run edge case tests for the retrieval system.

    Returns:
        Tuple of (passed_count, failed_count).
    """
    passed = 0
    failed = 0

    for i, case in enumerate(EDGE_CASES, start=1):
        try:
            results = retrieve_sections(case)
            if len(results) == 7:
                logger.info("[PASS] Edge case %d: Returned 7 results, no crash", i)
                passed += 1
            else:
                logger.info("[FAIL] Edge case %d: Expected 5 results, got %d", i, len(results))
                failed += 1
        except Exception as e:
            logger.info("[FAIL] Edge case %d: Crashed with %s: %s", i, type(e).__name__, e)
            failed += 1

    return passed, failed


def main() -> None:
    """Run the deterministic retrieval validation suite."""
    logger.info("=" * 60)
    logger.info("DETERMINISTIC RETRIEVAL VALIDATION SUITE")
    logger.info("=" * 60)

    logger.info("-" * 60)
    logger.info("RUNNING 20 TEST CASES")
    logger.info("-" * 60)
    test_passed, test_failed = run_test_cases()

    logger.info("-" * 60)
    logger.info("RUNNING EDGE CASE TESTS")
    logger.info("-" * 60)
    edge_passed, edge_failed = run_edge_case_tests()

    logger.info("=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    total_tests = len(TEST_CASES)
    total_edge = len(EDGE_CASES)
    logger.info("Total tests passed: %d / %d", test_passed, total_tests)
    logger.info("Edge cases passed: %d / %d", edge_passed, total_edge)

    if test_failed > 0 or edge_failed > 0:
        raise AssertionError(
            f"Validation failed: {test_failed} test case(s) and {edge_failed} edge case(s) failed."
        )

    logger.info("All validations passed successfully.")


if __name__ == "__main__":
    main()
