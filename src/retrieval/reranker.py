"""
Cross Encoder Reranker
"""

from typing import List

from src.models.model_manager import ModelManager
from src.retrieval.search_result import SearchResult
from src.config import RERANKER_MODEL, RERANK_TOP_K



class Reranker:

    def __init__(
        self,
        model_name: str = RERANKER_MODEL,
    ):

        self.manager = ModelManager()

        self.model = self.manager.load_reranker(
            model_name
        )

    def rerank(
        self,
        query: str,
        results: List[SearchResult],
        top_k = RERANK_TOP_K,
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