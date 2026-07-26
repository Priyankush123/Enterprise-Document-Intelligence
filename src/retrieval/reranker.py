"""
Cross Encoder Reranker
"""

from typing import List

from src.models.model_manager import ModelManager
from src.retrieval.search_result import SearchResult


class Reranker:

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):

        self.manager = ModelManager()

        self.model = self.manager.load_reranker(
            model_name
        )

    def rerank(
        self,
        query: str,
        results: List[SearchResult],
        top_k: int = 3,
    ) -> List[SearchResult]:

        if not results:
            return []

        pairs = [
            (query, result.text)
            for result in results
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(results, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        reranked = []

        for result, score in ranked[:top_k]:

            result.reranker_score = float(score)

            reranked.append(result)

        return reranked