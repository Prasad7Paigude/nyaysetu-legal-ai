"""Shared logging configuration for all NyaySetu modules.

Provides a single ``setup_logging()`` entry point that all services,
scripts, and entry points use to obtain a configured :class:`logging.Logger`.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    name: str = "nyaysetu",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Configure and return a logger with console (and optional file) output.

    Args:
        name: Logger name (typically ``__name__`` of the caller).
        level: Log level string (e.g. ``"DEBUG"``, ``"INFO"``). Defaults to ``"INFO"``.
        log_file: Optional path to a log file. When provided a
            :class:`logging.FileHandler` is added alongside the console handler.

    Returns:
        A configured :class:`logging.Logger` instance.
    """
    logger = logging.getLogger(name)

    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    else:
        logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
