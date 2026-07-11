"""
Document schema used throughout the Enterprise Document Intelligence Platform.

Every loader (PDF, DOCX, PPTX, TXT, Image) converts its output
into these models so that the downstream pipeline works with
a unified document structure.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Page(BaseModel):
    """
    Represents a single page (or slide) of a document.
    """

    page_number: int = Field(..., ge=1)
    text: str = Field(default="")


class DocumentMetadata(BaseModel):
    """
    Metadata associated with a document.
    """

    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None

    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    page_count: int = 0

    language: Optional[str] = None


class Document(BaseModel):
    """
    Standard document object used across the entire project.
    """

    filename: str

    filetype: str

    pages: List[Page]

    metadata: DocumentMetadata

    extracted_at: datetime = Field(default_factory=datetime.now)