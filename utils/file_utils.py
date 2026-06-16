"""File-system helpers for directory creation, JSON persistence, and path resolution.

All data-file reads should go through :func:`resolve_data_path` to honour
the centralised ``DATA_DIR`` configuration.
"""

import json
from pathlib import Path
from typing import Any, Union


def ensure_dir(path: Union[str, Path]) -> Path:
    """Create *path* (and any missing parents) if it does not already exist.

    Args:
        path: Directory path to ensure.

    Returns:
        The resolved :class:`Path` of the created / existing directory.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_data_path(relative_path: str) -> Path:
    """Resolve a path relative to the project-wide ``DATA_DIR``.

    Args:
        relative_path: Path fragment to append to ``DATA_DIR``
            (e.g. ``"jurisdiction_rules.json"``).

    Returns:
        Absolute :class:`Path` under the data directory.
    """
    from config.settings import DATA_DIR

    return DATA_DIR / relative_path


def load_json(path: Union[str, Path]) -> Any:
    """Deserialise a JSON file.

    Args:
        path: File path (string or :class:`Path`).

    Returns:
        Parsed JSON content as a Python object (typically ``dict`` or ``list``).
    """
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, path: Union[str, Path], indent: int = 2) -> None:
    """Serialise *data* to a JSON file with pretty-printing.

    Args:
        data: Python object to serialise.
        path: Output file path.
        indent: Number of spaces per indentation level (default ``2``).
    """
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
        f.write("\n")


def resolve_module_path(relative_path: str, module_file: str) -> Path:
    """Resolve *relative_path* against the directory containing *module_file*.

    Args:
        relative_path: Path fragment (e.g. ``"outputs"``).
        module_file: The ``__file__`` value of the calling module.

    Returns:
        Absolute :class:`Path` under the caller's directory.
    """
    return Path(module_file).resolve().parent / relative_path
