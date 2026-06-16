"""Chroma vector-store retriever for the legal knowledge base.

Provides a single ``get_retriever()`` factory that returns a configured
:class:`langchain.schema.BaseRetriever` over the ``legal_knowledge`` collection.
"""

from typing import Any

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from config.settings import CHATBOT_VECTOR_DB_PATH, EMBEDDING_MODEL


def get_retriever() -> Any:
    """Build and return a Chroma retriever over the legal-knowledge collection.

    The retriever uses cosine similarity search and returns the top-3
    most relevant documents for a given query.

    Returns:
        A :class:`langchain.schema.BaseRetriever` instance backed by Chroma.
    """
    embeddings: OpenAIEmbeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectordb: Chroma = Chroma(
        persist_directory=CHATBOT_VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name="legal_knowledge",
    )

    return vectordb.as_retriever(search_kwargs={"k": 3})
