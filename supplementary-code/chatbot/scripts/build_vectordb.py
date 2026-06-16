"""Build and persist the Chroma vector database from legal JSON documents.

Loads normalised IPC, CrPC, glossary, and amendments data, chunks them into
:class:`Document` objects, embeds them with OpenAI, and stores the result in
a local Chroma collection.
"""

import logging
from pathlib import Path
from typing import List

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from .load_documents import load_documents
from config.settings import CHATBOT_VECTOR_DB_PATH, DATA_DIR, EMBEDDING_MODEL
from utils.logging_setup import setup_logging

logger: logging.Logger = setup_logging(__name__)


def build_vector_database() -> None:
    """Load legal JSON files, create OpenAI embeddings, and persist a Chroma vector store.

    Raises:
        FileNotFoundError: If a required data file is missing.
        ValueError: If a data file contains invalid JSON.
    """
    data_files: List[Path] = [
        DATA_DIR / "normalized_ipc.json",
        DATA_DIR / "normalized_crpc.json",
        DATA_DIR / "normalized_glossary.json",
        DATA_DIR / "normalized_amendments.json",
    ]

    all_docs: List[Document] = []
    for path in data_files:
        try:
            all_docs.extend(load_documents(path))
            logger.info("Loaded %d documents from %s", len(all_docs), path.name)
        except (FileNotFoundError, ValueError) as exc:
            logger.error("Failed to load %s: %s", path, exc)
            raise

    if not all_docs:
        logger.warning("No documents loaded. Vector DB will be empty.")
        return

    embeddings: OpenAIEmbeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectordb: Chroma = Chroma.from_documents(
        documents=all_docs,
        embedding=embeddings,
        persist_directory=CHATBOT_VECTOR_DB_PATH,
        collection_name="legal_knowledge",
    )

    vectordb.persist()
    logger.info("Vector DB created with %d documents.", len(all_docs))
    logger.info("DB count: %d", vectordb._collection.count())


if __name__ == "__main__":
    build_vector_database()
