from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.document import Document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/")
def create_document(db: Session = Depends(get_db)):

    document = Document(
        filename="sample.pdf",
        file_type="pdf",
        file_size=2048,
        total_pages=12,
        total_chunks=38
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return document

@router.get("/")
def get_documents(db: Session = Depends(get_db)):

    documents = db.query(Document).all()

    return documents

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if document is None:
        return {"message": "Document not found"}

    db.delete(document)

    db.commit()

    return {"message": "Document deleted"}