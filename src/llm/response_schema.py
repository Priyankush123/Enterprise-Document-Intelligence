"""
Response Schema
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.retrieval.search_result import SearchResult


class RAGResponse(BaseModel):
    """
    Final response returned by the RAG pipeline.
    """

    question: str

    answer: str

    sources: List[SearchResult]

    model_name: str

    retrieval_count: int

    processing_time: float
