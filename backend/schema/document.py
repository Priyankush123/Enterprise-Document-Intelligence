from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    total_pages: int
    total_chunks: int
    uploaded_at: datetime

    class Config:
        from_attributes = True