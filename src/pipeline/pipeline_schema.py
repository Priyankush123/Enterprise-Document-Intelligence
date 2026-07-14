"""
Pipeline data models.

These models represent the outputs of different pipelines.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from src.chunking.chunk_schema import DocumentChunk
from src.ingestion.document_schema import Document


class PipelineStatus(str, Enum):
    """
    Represents the execution status of a pipeline.
    """

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    SKIPPED = "SKIPPED"


class IndexingResult(BaseModel):
    """
    Result returned after indexing a document.
    """

    document: Optional[Document] = None

    chunks: List[DocumentChunk] = Field(default_factory=list)

    embedding_count: int = 0

    processing_time: float = 0.0

    status: PipelineStatus = PipelineStatus.SUCCESS

    message: str = ""

    indexed_at: datetime = Field(
        default_factory=datetime.now
    )

    @property
    def total_chunks(self) -> int:
        return len(self.chunks)

    @property
    def success(self) -> bool:
        return self.status == PipelineStatus.SUCCESS