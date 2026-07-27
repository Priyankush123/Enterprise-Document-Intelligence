"""
Dashboard Statistics API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.document import Document
from backend.schema.stats import StatsResponse

from src.embeddings.embedding_model import EmbeddingModel
from src.llm.llm_client import LLMClient
from src.vectordb.chroma_store import ChromaVectorStore

router = APIRouter(
    prefix="/stats",
    tags=["Dashboard"],
)

vector_store = ChromaVectorStore()
embedder = EmbeddingModel()
llm = LLMClient()


@router.get(
    "/",
    response_model=StatsResponse,
)
def get_stats(
    db: Session = Depends(get_db),
):
    total_documents = (
        db.query(Document).count()
    )

    total_chunks = (
        vector_store.count_chunks()
    )

    return StatsResponse(
        total_documents=total_documents,
        total_chunks=total_chunks,
        embedding_model=embedder.model_name,
        llm_model=llm.model_name,
        vector_database="ChromaDB",
        api_status="Running",
        database_status="Connected",
    )