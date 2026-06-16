"""
NyaySetu Flask Backend API — Production-ready API for legal document generation.

Provides REST endpoints for RTI and affidavit generation, requirement analysis,
complexity scoring, and file download.

Reconciliation Notes (vs legacy ``draft-generation/app.py``):
- All 8 routes (``/``, ``/api/analyze``, ``/api/generate/rti``,
  ``/api/generate/affidavit``, ``/api/download/<filename>``,
  ``/api/states``, ``/api/complexity``) preserved with identical
  field requirements and response shapes.
- CORS, ``MAX_CONTENT_LENGTH`` (16 MB), and ``SECRET_KEY`` migrated
  to ``config.settings``.
- ``jurisdiction_rules.json`` resolved via ``DATA_DIR`` instead of
  ``os.path.dirname(__file__)`` (data consolidated to ``data/``).
- ``print()`` replaced with structured logging via ``setup_logging()``.
- Error handlers (404 / 500) return JSON responses, unchanged.
- Entry point: ``app.run(debug=True, host="0.0.0.0", port=5000)``.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from config.settings import ALLOWED_ORIGINS, DATA_DIR, DRAFT_GEN_DIR, SECRET_KEY
from utils.logging_setup import setup_logging

from draft_generation.affidavit_generator_backend import AffidavitGenerator
from draft_generation.database import NyaySetuDB
from draft_generation.orchestrator import DocumentOrchestrator
from draft_generation.rti_generator import RTIGenerator

logger = setup_logging(__name__)

# ---------------------------------------------------------------------------
# CORS origin parsing
# ---------------------------------------------------------------------------
raw_origins: str = ALLOWED_ORIGINS
allowed_origins: List[str] = [
    origin.strip().rstrip("/") for origin in raw_origins.split(",")
]
logger.info("CORS Allowed Origins (cleaned): %s", allowed_origins)

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app: Flask = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = str(DRAFT_GEN_DIR / "outputs")
app.config["SECRET_KEY"] = SECRET_KEY

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
logger.info("Upload Folder initialised at: %s", app.config["UPLOAD_FOLDER"])

# ---------------------------------------------------------------------------
# Shared service instances
# ---------------------------------------------------------------------------
rti_generator: RTIGenerator = RTIGenerator()
affidavit_generator: AffidavitGenerator = AffidavitGenerator()
orchestrator: DocumentOrchestrator = DocumentOrchestrator()
db: NyaySetuDB = NyaySetuDB()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home() -> Any:
    """API health-check endpoint.

    Returns:
        JSON payload with service status and available endpoints.
    """
    return jsonify(
        {
            "status": "success",
            "message": "NyaySetu API v2.0",
            "endpoints": {
                "analyze": "/api/analyze",
                "generate_rti": "/api/generate/rti",
                "generate_affidavit": "/api/generate/affidavit",
                "download": "/api/download/<filename>",
                "states": "/api/states",
            },
            "database": "connected" if db.client is not None else "disconnected",
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/api/analyze", methods=["POST"])
def analyze_requirement() -> Any:
    """Analyse a user requirement and suggest the appropriate document type.

    Request body::

        {"description": "I need RTI for exam records"}

    Returns:
        JSON with analysis including document_type, complexity_score, suggestions.
    """
    try:
        data: Optional[Dict[str, Any]] = request.get_json()
        if not data or "description" not in data:
            return jsonify(
                {"status": "error", "message": "Description is required"}
            ), 400

        analysis: Dict[str, Any] = orchestrator.analyze_requirements(
            data["description"]
        )
        return jsonify({"status": "success", "analysis": analysis})

    except Exception as exc:
        logger.exception("Error in /api/analyze")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/generate/rti", methods=["POST"])
def generate_rti() -> Any:
    """Generate an RTI Application PDF.

    Request body must include ``name``, ``address``, ``state``, ``authority``,
    ``pio_address``, and ``info``.

    Returns:
        JSON with download URL, document hash, reference number, and validation.
    """
    try:
        data: Optional[Dict[str, Any]] = request.get_json()

        required_fields: List[str] = [
            "name",
            "address",
            "state",
            "authority",
            "pio_address",
            "info",
        ]
        missing_fields: List[str] = [
            f for f in required_fields if f not in data
        ]

        if missing_fields:
            return jsonify(
                {
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                }
            ), 400

        result: Dict[str, Any] = rti_generator.generate(data)

        db.store_document(
            doc_type="RTI_APPLICATION",
            user_data=data,
            pdf_path=result["pdf_file"],
            doc_hash=result["document_hash"],
            ref_num=result["reference_number"],
        )

        filename: str = os.path.basename(result["pdf_file"])

        return jsonify(
            {
                "status": "success",
                "document": {
                    "filename": filename,
                    "download_url": f"/api/download/{filename}",
                    "hash": result["document_hash"],
                    "reference_number": result["reference_number"],
                    "validation": result["validation"],
                },
            }
        )

    except Exception as exc:
        logger.exception("Error in /api/generate/rti")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/generate/affidavit", methods=["POST"])
def generate_affidavit() -> Any:
    """Generate an Affidavit PDF.

    Request body must include ``deponent_name``, ``address``, and ``statements``.

    Returns:
        JSON with download URL and document hash.
    """
    try:
        data: Optional[Dict[str, Any]] = request.get_json()

        required_fields: List[str] = ["deponent_name", "address", "statements"]
        missing_fields: List[str] = [
            f for f in required_fields if f not in data
        ]

        if missing_fields:
            return jsonify(
                {
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                }
            ), 400

        result: Dict[str, str] = affidavit_generator.generate(data)

        db.store_document(
            doc_type="AFFIDAVIT",
            user_data=data,
            pdf_path=result["pdf_file"],
            doc_hash=result["document_hash"],
        )

        filename: str = os.path.basename(result["pdf_file"])

        return jsonify(
            {
                "status": "success",
                "document": {
                    "filename": filename,
                    "download_url": f"/api/download/{filename}",
                    "hash": result["document_hash"],
                },
            }
        )

    except Exception as exc:
        logger.exception("Error in /api/generate/affidavit")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/download/<filename>", methods=["GET"])
def download_file(filename: str) -> Any:
    """Serve a previously generated PDF file for download.

    Args:
        filename: Basename of the file to serve.

    Returns:
        The PDF file as an attachment, or a 404 JSON error.
    """
    try:
        file_path: str = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        if not os.path.exists(file_path):
            logger.warning("File not found: %s", file_path)
            return jsonify(
                {"status": "error", "message": "File not found"}
            ), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf",
        )

    except Exception as exc:
        logger.exception("Error in /api/download/%s", filename)
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/states", methods=["GET"])
def get_states() -> Any:
    """Return the list of supported states with their RTI fee and language info.

    Returns:
        JSON payload with a ``states`` array.
    """
    try:
        config_path = DATA_DIR / "jurisdiction_rules.json"
        with open(config_path, "r", encoding="utf-8") as f:
            rules: Dict[str, Any] = json.load(f)

        states: List[Dict[str, Any]] = []
        for state, info in rules.items():
            states.append(
                {
                    "name": state,
                    "fee": info.get("fee"),
                    "bpl_waiver": info.get("bpl_fee_waiver"),
                    "languages": info.get("languages_accepted", []),
                }
            )

        return jsonify({"status": "success", "states": states})

    except Exception as exc:
        logger.exception("Error in /api/states")
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/complexity", methods=["POST"])
def calculate_complexity() -> Any:
    """Calculate a complexity score for a document configuration.

    Request body may include ``type``, ``validation_enabled``, etc.

    Returns:
        JSON with complexity breakdown and level.
    """
    try:
        data: Dict[str, Any] = request.get_json() or {}
        score: Dict[str, Any] = orchestrator.calculate_complexity_score(data)
        return jsonify({"status": "success", "complexity": score})

    except Exception as exc:
        logger.exception("Error in /api/complexity")
        return jsonify({"status": "error", "message": str(exc)}), 500


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error: Any) -> Any:
    """Return a JSON 404 for unknown endpoints."""
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error: Any) -> Any:
    """Return a JSON 500 for unhandled server errors."""
    return jsonify({"status": "error", "message": "Internal server error"}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true", host="0.0.0.0", port=5002)
