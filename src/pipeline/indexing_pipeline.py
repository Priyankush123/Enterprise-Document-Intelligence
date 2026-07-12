"""
Indexing Pipeline
"""

import time

from src.ingestion.base_loader import BaseLoader
from src.pipeline.pipeline_schema import (
    IndexingResult,
    PipelineStatus,
)


class IndexingPipeline:
    """
    Pipeline responsible for indexing uploaded documents.
    """

    def __init__(
        self,
        loader: BaseLoader,
        preprocessor=None,
        chunker=None,
        embedder=None,
        vector_store=None,
    ):
        self.loader = loader
        self.preprocessor = preprocessor
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

    def run(self, file_path: str) -> IndexingResult:

        start_time = time.perf_counter()

        try:

            # Step 1
            document = self.loader.load(file_path)

            # Step 2
            if self.preprocessor:
                document = self.preprocessor.process(document)

            # Step 3
            chunks = []

            if self.chunker:
                chunks = self.chunker.split(document)

            # Step 4
            embeddings = []

            if self.embedder:
                embeddings = self.embedder.embed(chunks)

            # Step 5
            if self.vector_store:
                self.vector_store.add(chunks, embeddings)

            processing_time = (
                time.perf_counter() - start_time
            )

            return IndexingResult(
                document=document,
                chunks=chunks,
                embedding_count=len(embeddings),
                processing_time=processing_time,
                status=PipelineStatus.SUCCESS,
                message="Document indexed successfully.",
            )

        except Exception as e:

            processing_time = (
                time.perf_counter() - start_time
            )

            return IndexingResult(
                document=None,
                chunks=[],
                embedding_count=0,
                processing_time=processing_time,
                status=PipelineStatus.FAILED,
                message=str(e),
            )