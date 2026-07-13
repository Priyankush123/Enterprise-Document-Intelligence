"""
Retriever

Performs semantic retrieval from ChromaDB.
"""

from typing import List

from src.embeddings.embedding_model import EmbeddingModel
from src.vectordb.chroma_store import ChromaVectorStore


class Retriever:
    """
    Semantic retriever using embeddings and ChromaDB.
    """

    def __init__(
        self,
        vector_store: ChromaVectorStore,
        embedder: EmbeddingModel,
    ):

        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ):

        query_embedding = self.embedder.embed_query(
            query
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results