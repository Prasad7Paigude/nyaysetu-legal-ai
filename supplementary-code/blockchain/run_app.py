"""Entry point for the NyaySetu file-storage Flask application."""

import os
from typing import Optional

from blockchain.app import app
from config.settings import PORT
from utils.logging_setup import setup_logging

logger = setup_logging(__name__)


def main() -> None:
    """Start the Flask development server on the configured port."""
    port: int = int(os.environ.get("PORT", str(PORT)))
    logger.info("Starting NyaySetu app on port %d", port)
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
