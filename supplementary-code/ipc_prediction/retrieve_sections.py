import json
import logging
from pathlib import Path
from typing import Any

import chromadb
import requests

from config.settings import OPENROUTER_API_KEY, EMBEDDING_MODEL, IPC_VECTOR_DB_PATH, DATA_DIR

logger = logging.getLogger(__name__)

COLLECTION_NAME: str = "ipc_sections_v1"
TOP_K: int = 7
OPENROUTER_EMBEDDINGS_URL: str = "https://openrouter.ai/api/v1/embeddings"


def _resolve_persist_directory() -> str:
    configured = Path(IPC_VECTOR_DB_PATH)
    if configured.exists():
        return str(configured)

    candidates = [
        configured,
        Path(__file__).resolve().parent / "chroma_ipc_v1",
        DATA_DIR / "chroma_ipc_v1",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(candidates[0])


def _embed_text(text: str) -> list[float]:
    """Generate an embedding vector for the given text via OpenRouter API.

    Args:
        text: Input text to embed.

    Returns:
        A list of floats representing the embedding vector.

    Raises:
        requests.RequestException: If the API call fails.
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
        response = requests.post(
            OPENROUTER_EMBEDDINGS_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        body = response.json()
        return body["data"][0]["embedding"]
    except requests.RequestException as exc:
        logger.error("Embedding API call failed: %s", exc)
        raise
    except (KeyError, IndexError) as exc:
        logger.error("Unexpected embedding API response structure: %s", exc)
        raise


def _section_sort_key(section_number: str) -> tuple[int, str]:
    section_number = str(section_number).strip()
    digits = ""
    suffix = ""
    for char in section_number:
        if char.isdigit() and suffix == "":
            digits += char
        else:
            suffix += char
    numeric_part = int(digits) if digits else 0
    return numeric_part, suffix


def _normalize_keywords(value: Any) -> Any:
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            return value
    return value


def _format_result(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "section_number": str(metadata.get("section_number", "")),
        "title": metadata.get("title", ""),
        "summary": metadata.get("summary", ""),
        "keywords": _normalize_keywords(metadata.get("keywords", [])),
        "full_text": metadata.get("full_text", ""),
        "offence_type": metadata.get("offence_type", ""),
    }


def _retrieve_with_scores(incident_text: str) -> list[tuple[dict[str, Any], float]]:
    """Retrieve top-K IPC sections with similarity scores for the given incident text.

    Args:
        incident_text: Description of the incident.

    Returns:
        A list of tuples (metadata dict, similarity score) sorted by score descending.
    """
    try:
        client = chromadb.PersistentClient(path=_resolve_persist_directory())
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as exc:
        logger.error("ChromaDB access failed: %s", exc)
        return []

    if incident_text.strip() == "":
        try:
            all_rows = collection.get(include=["metadatas"])
            metadatas = all_rows.get("metadatas", [])
            ordered = sorted(
                metadatas,
                key=lambda row: _section_sort_key(str(row.get("section_number", ""))),
            )
            top_rows = ordered[:TOP_K]
            return [(_format_result(row), 0.0) for row in top_rows]
        except Exception as exc:
            logger.error("ChromaDB get all failed: %s", exc)
            return []

    try:
        query_embedding = _embed_text(incident_text)
    except Exception as exc:
        logger.error("Embedding generation failed: %s", exc)
        return []

    try:
        query_result = collection.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K,
            include=["embeddings", "metadatas", "distances"],
        )
    except Exception as exc:
        logger.error("ChromaDB query failed: %s", exc)
        return []

    metadatas = query_result["metadatas"][0]
    distances = query_result["distances"][0]

    rows: list[tuple[dict[str, Any], float]] = []
    for metadata, distance in zip(metadatas, distances):
        similarity = 1.0 - float(distance)
        rows.append((_format_result(metadata), similarity))

    rows.sort(
        key=lambda row: (
            -row[1],
            _section_sort_key(str(row[0].get("section_number", ""))),
        )
    )
    return rows[:TOP_K]


def retrieve_sections(incident_text: str) -> list[dict[str, Any]]:
    """Public API to retrieve top IPC sections for an incident description.

    Args:
        incident_text: Description of the incident.

    Returns:
        A list of metadata dicts for the top-K matching sections.
    """
    ranked = _retrieve_with_scores(incident_text)
    return [item for item, _ in ranked]


def _test_determinism() -> None:
    deterministic_query = (
        "A person entered another person's home at night and stole cash and jewelry."
    )
    outputs = [retrieve_sections(deterministic_query) for _ in range(5)]
    assert all(output == outputs[0] for output in outputs), "Non-deterministic retrieval detected"
    logger.info("Determinism test passed")


def _test_edge_cases() -> None:
    edge_cases = [
        "",
        "   ",
        (
            "The accused repeatedly issued threats over several months, forced entry into a property, "
            "caused physical injury during confrontation, and removed financial documents and valuables "
            "without consent, while witnesses observed intimidation, damage to property, and attempted "
            "destruction of records before law enforcement intervention."
        ),
        "1234567890 987654321",
    ]

    for case in edge_cases:
        ranked = _retrieve_with_scores(case)
        assert len(ranked) == TOP_K, f"Output length is not {TOP_K}"
        logger.info("Top sections: %s", [row[0]["section_number"] for row in ranked])
        logger.info("Scores: %s", [row[1] for row in ranked])


def main() -> None:
    _test_determinism()
    _test_edge_cases()


if __name__ == "__main__":
    main()
