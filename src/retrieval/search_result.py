"""
Search Result Schema

Defines the data models returned by the retrieval pipeline.
"""

from pydantic import BaseModel, Field


class SearchMetadata(BaseModel):
    """
    Metadata associated with a retrieved chunk.
    """

    document_name: str = Field(
        description="Source document name."
    )

    file_type: str = Field(
        description="Document file type."
    )

    page_number: int = Field(
        description="Page number in the source document."
    )

    chunk_number: int = Field(
        description="Chunk number within the page."
    )


from typing import Optional

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """
    Represents one retrieved chunk from ChromaDB.
    """

    chunk_id: str = Field(
        description="Unique chunk identifier."
    )

    text: str = Field(
        description="Retrieved chunk text."
    )

    score: float = Field(
        description="Vector similarity score from ChromaDB."
    )

    reranker_score: Optional[float] = Field(
        default=None,
        description="CrossEncoder reranker score."
    )

    metadata: SearchMetadata