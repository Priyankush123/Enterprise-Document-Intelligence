"""
Chunk Schema

Defines the chunk models used throughout the RAG pipeline.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    """
    Metadata associated with a chunk.
    """

    document_name: str

    file_type: str

    page_number: int

    chunk_number: int

    source: Optional[str] = None


class DocumentChunk(BaseModel):

    chunk_id: str

    text: str

    metadata: ChunkMetadata

    created_at: datetime = Field(
        default_factory=datetime.now
    )