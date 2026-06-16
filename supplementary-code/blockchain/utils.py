"""Utility functions for the blockchain file-storage system."""

import base64
import time
from datetime import datetime
from typing import Optional, Tuple, Union


def encode_file_to_base64(file_bytes: bytes) -> str:
    """Encode raw file bytes to a Base64 ASCII string.

    Args:
        file_bytes: Raw byte content of a file.

    Returns:
        UTF-8 decoded Base64 string.
    """
    return base64.b64encode(file_bytes).decode("utf-8")


def decode_base64_to_file(base64_string: str) -> bytes:
    """Decode a Base64 string back to the original file bytes.

    Args:
        base64_string: Base64-encoded content.

    Returns:
        Original binary data.
    """
    return base64.b64decode(base64_string)


def format_file_size(size_bytes: Union[int, float]) -> str:
    """Convert a byte count into a human-readable string (e.g. ``1.5 MB``).

    Args:
        size_bytes: File size in bytes.

    Returns:
        Formatted size string with appropriate unit (B / KB / MB / GB / TB / PB).
    """
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def format_timestamp(timestamp: float) -> str:
    """Format a Unix timestamp as a human-readable date-time string.

    Args:
        timestamp: Seconds since the Unix epoch.

    Returns:
        Formatted string in ``YYYY-MM-DD HH:MM:SS`` format.
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_current_timestamp() -> float:
    """Return the current Unix timestamp.

    Returns:
        Current value of :func:`time.time()`.
    """
    return time.time()


def validate_file_data(file_data: dict) -> Tuple[bool, Optional[str]]:
    """Ensure a file-transaction dict contains all required fields with valid
    types.

    Required fields: ``user``, ``v_file``, ``file_data``, ``file_size``.
    ``file_size`` must be coercible to ``int``.

    Args:
        file_data: Dictionary representing a file transaction.

    Returns:
        A tuple ``(is_valid, error_message)``. When valid the error message is
        ``None``.
    """
    required_fields = ["user", "v_file", "file_data", "file_size"]

    for field in required_fields:
        if field not in file_data:
            return False, f"Missing required field: {field}"

    try:
        int(file_data["file_size"])
    except (ValueError, TypeError):
        return False, "file_size must be a valid number"

    return True, None


def truncate_string(s: str, max_length: int = 50) -> str:
    """Truncate *s* to at most *max_length* characters, appending ``...`` when
    truncated.

    Args:
        s: The string to truncate.
        max_length: Maximum allowed length (including the ellipsis).

    Returns:
        Truncated string.
    """
    if len(s) <= max_length:
        return s
    return s[: max_length - 3] + "..."
