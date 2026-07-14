"""
Indexing Pipeline

Coordinates the complete document indexing workflow.
"""

import logging
import time
from typing import Callable, Optional

from src.chunking.recursive_chunker import RecursiveChunker
from src.embeddings.embedding_model import EmbeddingModel
from src.ingestion.loader_factory import LoaderFactory
from src.pipeline.pipeline_schema import (
    IndexingResult,
    PipelineStatus,
)
from src.preprocessing.preprocessor import DocumentPreprocessor
from src.vectordb.chroma_store import ChromaVectorStore


logger = logging.getLogger(__name__)


class IndexingPipeline:
    """
    Complete indexing pipeline.

    File
        ↓
    Loader
        ↓
    Preprocessor
        ↓
    Chunker
        ↓
    Embeddings
        ↓
    ChromaDB
    """

    def __init__(
        self,
        loader_factory: LoaderFactory,
        preprocessor: Optional[DocumentPreprocessor] = None,
        chunker: Optional[RecursiveChunker] = None,
        embedder: Optional[EmbeddingModel] = None,
        vector_store: Optional[ChromaVectorStore] = None,
    ):

        self.loader_factory = loader_factory

        self.preprocessor = preprocessor

        self.chunker = chunker

        self.embedder = embedder

        self.vector_store = vector_store

    def run(
        self,
        file_path: str,
        progress_callback: Optional[
            Callable[[str, int], None]
        ] = None,
    ) -> IndexingResult:

        start_time = time.perf_counter()

        try:

            def update(message: str, progress: int):

                logger.info(message)

                if progress_callback:

                    progress_callback(
                        message,
                        progress,
                    )

            # ----------------------------------------

            update("Loading document...", 10)

            loader = self.loader_factory.get_loader(
                file_path
            )

            document = loader.load(file_path)

            # ----------------------------------------

            if (
                self.vector_store
                and self.vector_store.document_exists(
                    document.filename
                )
            ):

                return IndexingResult(

                    document=document,

                    chunks=[],

                    embedding_count=0,

                    processing_time=(
                        time.perf_counter()
                        - start_time
                    ),

                    status=PipelineStatus.SKIPPED,

                    message="Document already indexed.",
                )

            # ----------------------------------------

            if self.preprocessor:

                update("Preprocessing...", 25)

                document = self.preprocessor.process(
                    document
                )

            # ----------------------------------------

            chunks = []

            if self.chunker:

                update("Chunking...", 50)

                chunks = self.chunker.split(
                    document
                )

            # ----------------------------------------

            embeddings = []

            if self.embedder:

                update(
                    "Generating embeddings...",
                    75,
                )

                embeddings = (
                    self.embedder.embed_chunks(
                        chunks
                    )
                )

            # ----------------------------------------

            if (
                self.vector_store
                and chunks
                and embeddings
            ):

                update(
                    "Saving vectors...",
                    95,
                )

                self.vector_store.add(

                    chunks=chunks,

                    embeddings=embeddings,
                )

            processing_time = (
                time.perf_counter()
                - start_time
            )

            update("Completed", 100)

            return IndexingResult(

                document=document,

                chunks=chunks,

                embedding_count=len(
                    embeddings
                ),

                processing_time=processing_time,

                status=PipelineStatus.SUCCESS,

                message="Document indexed successfully.",
            )

        except Exception as e:

            logger.exception(
                "Indexing failed."
            )

            processing_time = (
                time.perf_counter()
                - start_time
            )

            return IndexingResult(

                document=None,

                chunks=[],

                embedding_count=0,

                processing_time=processing_time,

                status=PipelineStatus.FAILED,

                message=str(e),
            )