import json
import logging
from pathlib import Path
from typing import Any

import chromadb
import requests

from config.settings import OPENROUTER_API_KEY, EMBEDDING_MODEL, IPC_VECTOR_DB_PATH, DATA_DIR
from ipc_prediction.build_embedding_texts import build_embedding_texts

logger = logging.getLogger(__name__)

COLLECTION_NAME: str = "ipc_sections_v1"
OPENROUTER_EMBEDDINGS_URL: str = "https://openrouter.ai/api/v1/embeddings"

EXPECTED_COUNT: int = 522


def load_dataset(data_dir: Path) -> list[dict[str, Any]]:
    """Load the enriched IPC dataset from JSON.

    Args:
        data_dir: Path to the data directory.

    Returns:
        A list of dataset records.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
    """
    dataset_path = data_dir / "ipc_enriched_v1.json"
    try:
        with dataset_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Dataset file not found at %s", dataset_path)
        raise
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in dataset file: %s", exc)
        raise


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding vector via OpenRouter API.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text,
    }
    try:
        response = requests.post(OPENROUTER_EMBEDDINGS_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["data"][0]["embedding"]
    except requests.RequestException as exc:
        logger.error("Embedding generation API call failed: %s", exc)
        raise
    except (KeyError, IndexError) as exc:
        logger.error("Unexpected embedding API response: %s", exc)
        raise


def main() -> None:
    try:
        embedding_texts = build_embedding_texts(DATA_DIR)
        assert len(embedding_texts) == EXPECTED_COUNT, (
            f"Expected {EXPECTED_COUNT} embedding texts, got {len(embedding_texts)}"
        )

        dataset = load_dataset(DATA_DIR)
        assert len(dataset) == EXPECTED_COUNT, (
            f"Expected {EXPECTED_COUNT} dataset items, got {len(dataset)}"
        )

        metadata_map = {str(item["section_number"]): item for item in dataset}

        vectors: list[list[float]] = []
        for et in embedding_texts:
            embedding = generate_embedding(et["embedding_text"])
            vectors.append(embedding)

        assert len(vectors) == EXPECTED_COUNT, (
            f"Expected {EXPECTED_COUNT} vectors, got {len(vectors)}"
        )

        persist_path = IPC_VECTOR_DB_PATH
        client = chromadb.PersistentClient(path=persist_path)

        try:
            client.delete_collection(name=COLLECTION_NAME)
            logger.info("Deleted existing collection '%s'", COLLECTION_NAME)
        except Exception:
            pass

        collection = client.create_collection(name=COLLECTION_NAME)

        ids: list[str] = []
        embeddings: list[list[float]] = []
        metadatas_list: list[dict[str, Any]] = []

        for i, et in enumerate(embedding_texts):
            section_id = et["id"]
            ids.append(section_id)
            embeddings.append(vectors[i])

            original = metadata_map[section_id]
            metadatas_list.append({
                "section_number": str(original.get("section_number", "")),
                "title": str(original.get("title", "")),
                "summary": str(original.get("summary", "")),
                "keywords": json.dumps(original.get("keywords", [])),
                "full_text": str(original.get("full_text", "")),
                "offence_type": str(original.get("offence_type", "")),
            })

        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas_list)
        logger.info("Inserted %d records into collection '%s'", len(ids), COLLECTION_NAME)

        assert collection.count() == EXPECTED_COUNT, (
            f"Expected {EXPECTED_COUNT} items in collection, got {collection.count()}"
        )

        sample = collection.get(ids=[ids[0]], include=["embeddings", "metadatas"])
        assert len(sample["embeddings"][0]) > 0, "Sample embedding is empty"
        required_fields = ["section_number", "title", "summary", "keywords", "full_text", "offence_type"]
        assert all(key in sample["metadatas"][0] for key in required_fields), "Metadata fields missing"

        vector_dim = len(vectors[0])
        logger.info("Total sections embedded: %d", EXPECTED_COUNT)
        logger.info("Chroma collection: %s", COLLECTION_NAME)
        logger.info("Vector dimension: %d", vector_dim)
        logger.info("Persistence directory: %s", persist_path)

    except Exception as exc:
        logger.error("Embedding generation pipeline failed: %s", exc)
        raise


if __name__ == "__main__":
    main()
