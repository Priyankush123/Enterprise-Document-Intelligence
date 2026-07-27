"""
Embedding Model

Generates dense vector embeddings using
Sentence Transformers.
"""

from typing import List

from src.chunking.chunk_schema import DocumentChunk
from src.models.model_manager import ModelManager
from src.config import EMBEDDING_MODEL


class EmbeddingModel:
    """
    Embedding model wrapper.
    """

    DOCUMENT_PREFIX = (
        "Represent this document for retrieval: "
    )

    QUERY_PREFIX = (
        "Represent this question for searching relevant documents: "
    )

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
    ):

        self.model_name = model_name

        self.manager = ModelManager()

        self.model = self.manager.load_embedder(
            model_name
        )

    def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for a document.
        """

        embedding = self.model.encode(
            self.DOCUMENT_PREFIX + text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_query(
        self,
        query: str,
    ) -> List[float]:
        """
        Generate embedding for a user query.
        """

        embedding = self.model.encode(
            self.QUERY_PREFIX + query,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_chunks(
        self,
        chunks: List[DocumentChunk],
    ) -> List[List[float]]:

        if not chunks:
            return []

        texts = [
            self.DOCUMENT_PREFIX + chunk.text
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return embeddings.tolist()