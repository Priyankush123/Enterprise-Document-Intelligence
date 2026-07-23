from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.document import Document

from src.pipeline.pipeline_schema import PipelineStatus
from src.pipeline.indexing_pipeline import IndexingPipeline

# Import your existing instances/services
from src.ingestion.loader_factory import LoaderFactory
from src.preprocessing.preprocessor import DocumentPreprocessor
from src.chunking.recursive_chunker import RecursiveChunker
from src.embeddings.embedding_model import EmbeddingModel
from src.vectordb.chroma_store import ChromaVectorStore

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_DIR = Path("storage")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Create the pipeline ONCE
pipeline = IndexingPipeline(
    loader_factory=LoaderFactory,
    preprocessor=DocumentPreprocessor(),
    chunker=RecursiveChunker(),
    embedder=EmbeddingModel(),
    vector_store=ChromaVectorStore(),
)


@router.post("/")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    file_path = UPLOAD_DIR / file.filename

    try:

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run indexing pipeline
        result = pipeline.run(str(file_path))

        if result.status == PipelineStatus.FAILED:

            raise HTTPException(
                status_code=500,
                detail=result.message,
            )

        if result.status == PipelineStatus.SKIPPED:

            raise HTTPException(
                status_code=409,
                detail=result.message,
            )

        # Save metadata
        document = Document(
            filename=result.document.filename,
            file_type=file.content_type,
            file_size=file_path.stat().st_size,
            total_pages=result.document.total_pages,
            total_chunks=len(result.chunks),
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "status": result.status.value,
            "message": result.message,
            "document_id": document.id,
            "filename": document.filename,
            "pages": document.total_pages,
            "chunks": document.total_chunks,
            "embedding_count": result.embedding_count,
            "processing_time": round(result.processing_time, 2),
        }

    except HTTPException:
        raise

    except Exception as e:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        file.file.close()