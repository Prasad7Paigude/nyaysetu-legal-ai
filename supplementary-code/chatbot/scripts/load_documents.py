import json
from pathlib import Path
from typing import Any, Dict, List, Union

from langchain_core.documents import Document


def load_documents(json_path: Union[str, Path]) -> List[Document]:
    docs: List[Document] = []
    path = Path(json_path)

    try:
        with path.open("r", encoding="utf-8") as f:
            data: List[Dict[str, Any]] = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")

    for item in data:
        content = f"""
{item['identifier']} — {item['title_or_term']}

{item['bare_text']}

Explanation:
{item['plain_english_explanation']}
"""
        metadata: Dict[str, str] = {
            "law_type": item["law_type"],
            "identifier": item["identifier"],
            "source": item["source"]
        }

        docs.append(
            Document(
                page_content=content.strip(),
                metadata=metadata
            )
        )

    return docs
