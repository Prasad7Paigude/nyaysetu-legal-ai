import json
import re
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

EXPECTED_COUNT: int = 522


def _to_text(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def build_embedding_texts(data_dir: Path) -> list[dict[str, str]]:
    """Build embedding text strings from the enriched IPC dataset.

    Reads ipc_enriched_v1.json from the given data directory and constructs
    structured embedding text for each section.

    Args:
        data_dir: Path to the directory containing ipc_enriched_v1.json.

    Returns:
        A list of dicts with 'id' (section number) and 'embedding_text' keys.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        ValueError: If the dataset length does not match EXPECTED_COUNT.
    """
    dataset_path = data_dir / "ipc_enriched_v1.json"
    try:
        with dataset_path.open("r", encoding="utf-8") as file:
            dataset = json.load(file)
    except FileNotFoundError:
        logger.error("Dataset file not found at %s", dataset_path)
        raise
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in dataset file: %s", exc)
        raise

    if len(dataset) != EXPECTED_COUNT:
        raise ValueError(
            f"Dataset length mismatch: expected {EXPECTED_COUNT}, got {len(dataset)}"
        )

    embedding_texts: list[dict[str, str]] = []

    for item in dataset:
        section_number = _to_text(item.get("section_number"))
        title = _to_text(item.get("title"))
        title = title.rstrip(".")
        summary = _to_text(item.get("summary"))
        summary = summary.rstrip(".")
        keywords_raw = item.get("keywords", [])

        if isinstance(keywords_raw, list):
            keywords = ", ".join(_to_text(keyword) for keyword in keywords_raw)
        else:
            keywords = _to_text(keywords_raw)

        embedding_text = (
            f"Section {section_number}: {title}. "
            f"Summary: {summary}. "
            f"Keywords: {keywords}."
        )

        embedding_texts.append(
            {
                "id": section_number,
                "embedding_text": embedding_text,
            }
        )

    if len(embedding_texts) != EXPECTED_COUNT:
        raise ValueError(
            f"Embedding texts length mismatch: expected {EXPECTED_COUNT}, got {len(embedding_texts)}"
        )

    return embedding_texts


def main() -> None:
    from config.settings import DATA_DIR

    embedding_texts = build_embedding_texts(DATA_DIR)
    logger.info("Total sections processed: 522")
    logger.info("Sample embedding text (first item): %s", embedding_texts[0]["embedding_text"])


if __name__ == "__main__":
    main()
