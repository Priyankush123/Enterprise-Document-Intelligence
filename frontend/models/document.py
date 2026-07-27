from datetime import datetime

from pydantic import BaseModel


class DocumentModel(BaseModel):

    id: int
    filename: str
    file_type: str
    file_size: int
    total_pages: int
    total_chunks: int
    uploaded_at: datetime