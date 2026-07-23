"""
Chat API Schemas
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question for the RAG system."
    )


class Source(BaseModel):
    document_name: str
    page_number: int
    chunk_number: int


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]
    model_name: str
    retrieval_count: int
    processing_time: float