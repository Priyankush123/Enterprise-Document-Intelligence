"""
Retrieval Pipeline

Coordinates retrieval and reranking.
"""

from typing import List

from src.embeddings.embedding_model import EmbeddingModel
from src.retrieval.retriever import Retriever
from src.retrieval.reranker import Reranker
from src.retrieval.search_result import SearchResult
from src.vectordb.chroma_store import ChromaVectorStore
from src.config import VECTOR_TOP_K, RERANK_TOP_K


class RetrievalPipeline:
    """
    Complete retrieval pipeline.

    Query
        ↓
    Retriever
        ↓
    Reranker
        ↓
    Return best chunks
    """

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.vector_store = ChromaVectorStore()

        self.retriever = Retriever(

            vector_store=self.vector_store,

            embedder=self.embedder,
        )

        self.reranker = Reranker()

    def retrieve(
        self,
        query: str,
        retrieve_top_k = VECTOR_TOP_K,
        rerank_top_k = RERANK_TOP_K,
    ) -> List[SearchResult]:

        retrieved = self.retriever.retrieve(

            query=query,

            top_k=retrieve_top_k,
        )

        reranked = self.reranker.rerank(

            query=query,

            results=retrieved,

            top_k=rerank_top_k,
        )

        return reranked

    def build_context(
            self,
            results: List[SearchResult],
        ) -> str:
            """
            Build a structured context for the LLM.
            """

            sections = []

            for index, result in enumerate(results, start=1):

                sections.append(
                    f"""
        ### Source {index}

        Document: {result.metadata.document_name}
        Page: {result.metadata.page_number}

        Content:
        {result.text}
        """.strip()
                )

            return "\n\n----------------------------------------\n\n".join(
                sections
            )

    def retrieve_context(
        self,
        query: str,
        retrieve_top_k = VECTOR_TOP_K,
        rerank_top_k = RERANK_TOP_K,
    ):

        results = self.retrieve(

            query=query,

            retrieve_top_k=retrieve_top_k,

            rerank_top_k=rerank_top_k,
        )

        context = self.build_context(results)

        return context, results
    