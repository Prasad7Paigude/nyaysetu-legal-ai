import logging
from typing import Optional

from langchain_openai import ChatOpenAI

from .retriever import get_retriever
from .context_builder import build_context
from .system_prompt import LEGAL_QA_SYSTEM_PROMPT
from .document_selector import select_document
from .document_templates import DOCUMENT_TEMPLATES
from .intent_router import classify_intent, QueryIntent
from .query_quality import is_vague_query
from .clarification import get_clarification_question
from .response_formatter import format_response
from config.settings import LLM_CHAT_MODEL
from utils.logging_setup import setup_logging

logger: logging.Logger = setup_logging(__name__)

PROCEDURAL_REFUSAL_MESSAGE: str = (
    "This system provides legal information only. "
    "It does not provide procedural guidance or instructions."
)

ADVICE_REFUSAL_MESSAGE: str = (
    "This system provides general legal information only. "
    "It cannot predict outcomes or give legal advice."
)


def render_document_template(template: dict) -> str:
    return f"""
{template['what_it_is']}

This document exists to address a specific legal need. 
{template['why_it_exists']}

In practice, it is typically relevant in situations such as the following.
{template['when_it_is_used']}

It is also important to be clear about its limitations.
{template['what_it_does_not_do']}
""".strip()


def detect_document_type(query: str) -> Optional[str]:
    query_lower = query.lower().strip()

    DOCUMENT_MAP: dict = {
        "fir": ["fir", "first information report"],
        "rti": ["rti", "right to information"],
        "bail": ["bail", "bail application", "anticipatory bail"],
        "legal_notice": ["legal notice"]
    }

    for doc_key, keywords in DOCUMENT_MAP.items():
        for kw in keywords:
            if kw in query_lower:
                return doc_key

    return None


def handle_document_explanation(user_query: str) -> str:
    document_key: Optional[str] = detect_document_type(user_query)

    if not document_key or document_key not in DOCUMENT_TEMPLATES:
        return "The information is not available in the current legal knowledge base."

    raw_explanation: str = render_document_template(
        DOCUMENT_TEMPLATES[document_key]
    )

    return format_response(
        title=DOCUMENT_TEMPLATES[document_key]["title"],
        explanation=raw_explanation,
        note="This is general legal information, not legal advice."
    )


def handle_document_selection(user_query: str) -> str:
    selection: Optional[dict] = select_document(user_query)

    if not selection:
        return "The information is not available in the current legal knowledge base."

    explanation: str = (
        f"{selection['document']}\n\n"
        f"{selection['reason']}"
    )

    return format_response(
        title="Suggested Document",
        explanation=explanation,
        note="This is indicative guidance only and not legal advice."
    )


def answer_query(user_query: str) -> str:
    vague_check: dict = is_vague_query(user_query)

    if vague_check["is_vague"]:
        return get_clarification_question(vague_check["reason"])

    intent: QueryIntent = classify_intent(user_query)

    if intent == QueryIntent.PROCEDURAL:
        return PROCEDURAL_REFUSAL_MESSAGE

    if intent == QueryIntent.ADVICE:
        return ADVICE_REFUSAL_MESSAGE

    if intent == QueryIntent.DOCUMENT_EXPLANATION:
        return handle_document_explanation(user_query)

    if intent == QueryIntent.DOCUMENT_SELECTION:
        return handle_document_selection(user_query)

    try:
        retriever = get_retriever()
        docs = retriever.invoke(user_query)
    except Exception:
        logger.exception("Retrieval failed for query: %s", user_query)
        return "The information is not available in the current legal knowledge base."

    if not docs:
        return "The information is not available in the current legal knowledge base."

    context: str = build_context(docs)

    if not context.strip():
        return "The information is not available in the current legal knowledge base."

    try:
        llm = ChatOpenAI(
            model=LLM_CHAT_MODEL,
            temperature=0.25
        )

        messages = [
            {"role": "system", "content": LEGAL_QA_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Legal Context:
{context}

Question:
{user_query}
"""
            }
        ]

        response = llm.invoke(messages)

        return format_response(
            title="Legal Information",
            explanation=response.content,
            note="This is general legal information, not legal advice."
        )
    except Exception:
        logger.exception("LLM invocation failed for query: %s", user_query)
        return "The information is not available in the current legal knowledge base."
