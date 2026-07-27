"""
Chat API

Exposes the RAG pipeline through FastAPI.
"""

import logging

from fastapi import APIRouter, HTTPException

from backend.schema.chat import (
    ChatRequest,
    ChatResponse,
    Source
)

from src.llm.response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

# Create once
response_generator = ResponseGenerator()


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    """
    Ask a question to the RAG system.
    """

    try:

        response = response_generator.generate(
            question=request.question,
        )

        return ChatResponse(
            question=response.question,
            answer=response.answer,
            sources=[ Source(
                    document_name=s.metadata.document_name,
                    page_number=s.metadata.page_number,
                    chunk_number=s.metadata.chunk_number,
                )
                for s in response.sources],
            model_name=response.model_name,
            retrieval_count=response.retrieval_count,
            processing_time=response.processing_time,
        )

    except Exception as e:

        logger.exception(
            "Chat generation failed."
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )