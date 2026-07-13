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
        retrieve_top_k: int = 10,
        rerank_top_k: int = 3,
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
        Convert retrieved chunks into a context string
        for the LLM.
        """

        context = []

        for index, result in enumerate(results, start=1):

            context.append(

                f"""Source {index}
Document : {result.metadata.document_name}
Page : {result.metadata.page_number}

{result.text}
"""
            )

        return "\n\n".join(context)

    def retrieve_context(
        self,
        query: str,
        retrieve_top_k: int = 10,
        rerank_top_k: int = 3,
    ):

        results = self.retrieve(

            query=query,

            retrieve_top_k=retrieve_top_k,

            rerank_top_k=rerank_top_k,
        )

        context = self.build_context(results)

        return context, results