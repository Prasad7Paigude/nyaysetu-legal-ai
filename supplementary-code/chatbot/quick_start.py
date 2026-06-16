import logging
import sys
from pathlib import Path
from typing import List

from config.settings import CHATBOT_VECTOR_DB_PATH
from utils.logging_setup import setup_logging

logger: logging.Logger = setup_logging(__name__)


def check_python_version() -> bool:
    version = sys.version_info
    logger.info("Python version: %s.%s.%s", version.major, version.minor, version.micro)

    if version.major < 3 or (version.major == 3 and version.minor < 11):
        logger.error("Python 3.11+ required")
        return False

    logger.info("Python version OK")
    return True


def check_virtual_env() -> bool:
    venv_path = Path("legal_chatbot")

    if venv_path.exists():
        logger.info("Virtual environment found")
        return True
    else:
        logger.warning("Virtual environment not found. Run: python -m venv legal_chatbot")
        return False


def check_dependencies() -> bool:
    required: List[str] = ["fastapi", "uvicorn", "langchain", "chromadb", "openai"]
    missing: List[str] = []

    for package in required:
        try:
            __import__(package)
            logger.info("%s installed", package)
        except ImportError:
            logger.error("%s not installed", package)
            missing.append(package)

    if missing:
        logger.warning("Missing dependencies detected. Run: pip install -r requirements.txt")
        return False

    return True


def check_env_file() -> bool:
    env_path = Path(".env")

    if env_path.exists():
        logger.info(".env file found")

        try:
            content = env_path.read_text(encoding="utf-8")
            if "OPENAI_API_KEY" in content:
                logger.info("OPENAI_API_KEY configured")
            else:
                logger.warning("OPENAI_API_KEY not found in .env")
        except OSError:
            logger.error("Could not read .env file")

        return True
    else:
        logger.error(".env file not found. Create .env with OPENAI_API_KEY=your_key")
        return False


def check_vector_db() -> bool:
    db_path = Path(CHATBOT_VECTOR_DB_PATH)

    if db_path.exists():
        logger.info("Vector database found at %s", db_path)
        return True
    else:
        logger.error("Vector database not found at %s", db_path)
        return False


def print_next_steps(all_ok: bool) -> None:
    print("\n" + "=" * 60)

    if all_ok:
        print("ALL CHECKS PASSED - Ready to run!")
        print("=" * 60)
        print("\nStart the API server:")
        print("\n  Option 1 (Development):")
        print("    uvicorn main:app --reload --port 8000")
        print("\n  Option 2 (Production):")
        print("    python main.py")
        print("\nThen visit:")
        print("  - API Docs: http://localhost:8000/docs")
        print("  - Health Check: http://localhost:8000/health")

    else:
        print("SETUP INCOMPLETE")
        print("=" * 60)
        print("\nComplete these steps:")
        print("\n1. Create virtual environment:")
        print("   python -m venv legal_chatbot")
        print("\n2. Activate virtual environment:")
        print("   legal_chatbot\\Scripts\\activate  # Windows")
        print("   source legal_chatbot/bin/activate  # macOS/Linux")
        print("\n3. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n4. Create .env file with your API key")
        print("\n5. Run this script again: python quick_start.py")


def main() -> int:
    print("=" * 60)
    print("Legal Chatbot API - Quick Start Check")
    print("=" * 60)
    print()

    checks: List[bool] = [
        check_python_version(),
        check_virtual_env(),
        check_env_file(),
        check_vector_db(),
        check_dependencies(),
    ]

    all_ok: bool = all(checks)
    print_next_steps(all_ok)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
