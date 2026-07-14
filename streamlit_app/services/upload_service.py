"""
Upload Service

Connects Streamlit with the indexing pipeline.
"""

import time

from src.chunking.recursive_chunker import RecursiveChunker
from src.embeddings.embedding_model import EmbeddingModel
from src.ingestion.loader_factory import LoaderFactory
from src.pipeline.indexing_pipeline import IndexingPipeline
from src.preprocessing.preprocessor import DocumentPreprocessor
from src.vectordb.chroma_store import ChromaVectorStore


class UploadService:

    def __init__(self):

        self.pipeline = IndexingPipeline(
            loader_factory=LoaderFactory(),
            preprocessor=DocumentPreprocessor(),
            chunker=RecursiveChunker(),
            embedder=EmbeddingModel(),
            vector_store=ChromaVectorStore(),
        )

    def upload(
        self,
        file_path: str,
        progress_callback=None,
    ):

        start = time.perf_counter()

        result = self.pipeline.run(
            file_path=file_path,
            progress_callback=progress_callback,
        )

        elapsed = time.perf_counter() - start

        result.processing_time = elapsed

        return result