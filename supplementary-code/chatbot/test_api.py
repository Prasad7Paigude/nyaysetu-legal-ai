import logging
from pathlib import Path
from typing import Optional

from utils.logging_setup import setup_logging

logger: logging.Logger = setup_logging(__name__)

_SCRIPTS_DIR: Path = Path(__file__).resolve().parent / "scripts"


def test_rag_pipeline_import() -> None:
    logger.info("Testing imports...")
    try:
        from chatbot.scripts.rag_pipeline import answer_query
        logger.info("rag_pipeline imported successfully")
    except Exception as e:
        logger.error("Failed to import rag_pipeline: %s", e)
        raise


def test_chatbot_response() -> None:
    logger.info("Testing chatbot...")
    try:
        from chatbot.scripts.rag_pipeline import answer_query
        response = answer_query("What is IPC Section 420?")
        logger.info("Chatbot responded successfully")
        logger.info("Response preview: %s...", response[:200])
    except Exception as e:
        logger.error("Chatbot failed: %s", e)
        raise


def main() -> None:
    test_rag_pipeline_import()
    test_chatbot_response()

    print("\n" + "=" * 80)
    print("All integration tests passed!")
    print("=" * 80)
    print("\nYou can now run the API with:")
    print("  uvicorn main:app --reload")
    print("\nOr:")
    print("  python main.py")


if __name__ == "__main__":
    main()
