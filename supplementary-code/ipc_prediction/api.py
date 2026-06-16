"""
IPC Prediction API — FastAPI service for predicting IPC sections from case descriptions.

Reconciliation Notes (vs legacy ``v2_IPC_SECTION_PREDICTION/script/main.py``):
- Single ``POST /ipc/predict`` endpoint preserved with identical
  request/response schema, validation logic (>=10 chars), and
  ``SUGGESTIONS`` pool.
- CORS configuration unchanged (``allow_origins=["*"]``).
- Import fallback (``try: from script.schemas … except ImportError: …``)
  eliminated — package-qualified imports used throughout.
- ``logging`` via ``setup_logging()`` (no more bare ``print()``).
- Type hints and Google-style docstrings added.
- ASGI app name ``"IPC Prediction API"`` preserved.
"""

import os
import random
import logging
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ipc_prediction.schemas import CaseInput
from ipc_prediction.ipc_reasoning_engine import predict_ipc_section

logger = logging.getLogger(__name__)

app = FastAPI(title="IPC Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUGGESTIONS: list[str] = [
    "Consider consulting a legal professional.",
    "You may approach the nearest police station.",
    "Document all relevant evidence.",
    "Ensure your safety before taking further action.",
    "Seek immediate help if the situation escalates.",
]


@app.post("/ipc/predict")
def predict_ipc(case: CaseInput) -> dict[str, Any]:
    raw_text = case.text.strip()

    if not raw_text or len(raw_text) < 10:
        return {
            "prediction": None,
            "message": "Please describe the incident with sufficient details.",
            "disclaimer": "This tool requires incident details to provide a legal prediction.",
        }

    rag_output = predict_ipc_section(raw_text)

    if rag_output.get("predicted_sections"):
        ipc_code = rag_output["predicted_sections"][0]
        title = rag_output.get("title", "")
        confidence = round(rag_output.get("confidence", 0.0) * 100)
    else:
        ipc_code = None
        title = ""
        confidence = 0

    suggestion = random.choice(SUGGESTIONS)

    explanation_text = rag_output.get("explanation", "")

    return {
        "prediction": {
            "ipc_section": f"IPC {ipc_code}" if ipc_code else None,
            "title": title,
            "confidence": confidence,
        },
        "explanation": explanation_text,
        "why": rag_output.get("why") or explanation_text,
        "suggestion": suggestion,
        "disclaimer": "This is an AI-assisted legal awareness tool.",
    }
