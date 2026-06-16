"""Centralised configuration for NyaySetu.

All API keys, model names, directory paths, and runtime settings are defined
here and loaded from the environment via python-dotenv.
"""

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent
DATA_DIR: Final[Path] = ROOT_DIR / "data"
MODELS_DIR: Final[Path] = ROOT_DIR / "models"
UTILS_DIR: Final[Path] = ROOT_DIR / "utils"
CONFIG_DIR: Final[Path] = ROOT_DIR / "config"
SUPPLEMENTARY_DIR: Final[Path] = ROOT_DIR / "supplementary-code"
CHATBOT_DIR: Final[Path] = SUPPLEMENTARY_DIR / "chatbot"
BLOCKCHAIN_DIR: Final[Path] = SUPPLEMENTARY_DIR / "blockchain"
DRAFT_GEN_DIR: Final[Path] = SUPPLEMENTARY_DIR / "draft_generation"
IPC_PREDICTION_DIR: Final[Path] = SUPPLEMENTARY_DIR / "ipc_prediction"

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/file_storage")
BLOCKCHAIN_SERVICE_URL: str = os.getenv("BLOCKCHAIN_SERVICE_URL", "")
BLOCKCHAIN_NODE_ADDR: str = os.getenv("BLOCKCHAIN_NODE_ADDR", "http://127.0.0.1:8800")
ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
PORT: int = int(os.getenv("PORT", "10000"))

CHATBOT_VECTOR_DB_PATH: str = os.getenv(
    "CHATBOT_VECTOR_DB_PATH",
    str(SUPPLEMENTARY_DIR / "chatbot" / "scripts" / "chroma_day1")
)
IPC_VECTOR_DB_PATH: str = os.getenv(
    "IPC_VECTOR_DB_PATH",
    str(IPC_PREDICTION_DIR / "chroma_ipc_v1")
)

EMBEDDING_MODEL: str = "text-embedding-3-small"
LLM_CHAT_MODEL: str = "meta-llama/Llama-3.1-8B-Instruct"
GEMINI_MODEL: str = "models/gemini-2.5-flash"
GROQ_MODEL: str = "llama-3.3-70b-versatile"
IPC_LLM_MODEL: str = "openai/text-embedding-3-small"

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
