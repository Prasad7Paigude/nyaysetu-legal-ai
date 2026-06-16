import logging
import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config.settings import PORT
from utils.logging_setup import setup_logging

logger: logging.Logger = setup_logging(__name__)


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "optional-uuid",
                "message": "What is IPC Section 420?"
            }
        }


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    confidence: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "reply": "IPC Section 420 deals with cheating and dishonesty...",
                "session_id": "abc-123",
                "confidence": None
            }
        }


class HealthResponse(BaseModel):
    status: str


app = FastAPI(
    title="AI Legal Chatbot API",
    description="HTTP API for the NyaySetu Legal Chatbot - provides legal information through text interface",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "https://vercel.app"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_session_id() -> str:
    return str(uuid.uuid4())


def safe_chatbot_call(user_message: str) -> str:
    try:
        from chatbot.scripts.rag_pipeline import answer_query
        return answer_query(user_message)
    except Exception:
        logger.exception("Chatbot error for message: %s", user_message)
        return "I apologize, but I'm temporarily unable to process your request. Please try again."


@app.get("/", tags=["Info"])
async def root() -> dict:
    return {
        "service": "AI Legal Chatbot API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "text_chat": "/chat"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    session_id: str = request.session_id or generate_session_id()

    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        reply: str = safe_chatbot_call(request.message.strip())
    except Exception:
        logger.exception("Chat endpoint failed for session: %s", session_id)
        raise HTTPException(status_code=500, detail="Chatbot temporarily unavailable")

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        confidence=None
    )


@app.exception_handler(404)
async def not_found_handler(request, exc) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "Chatbot temporarily unavailable"}
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting AI Legal Chatbot API (Text-only, Memory Optimized)")
    port: int = int(os.environ.get("PORT", PORT))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
