"""
Retrieval Evaluation

Evaluates the retrieval quality of the RAG pipeline.
"""

from dataclasses import dataclass
from typing import List

from src.embeddings.embedding_model import EmbeddingModel
from src.retrieval.retriever import Retriever
from src.retrieval.reranker import Reranker
from src.vectordb.chroma_store import ChromaVectorStore


# ----------------------------------------------------
# Test Query
# ----------------------------------------------------

@dataclass
class TestQuery:

    query: str

    expected: str


# ----------------------------------------------------
# Evaluator
# ----------------------------------------------------

class RetrievalEvaluator:

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.vector_store = ChromaVectorStore()

        self.retriever = Retriever(

            vector_store=self.vector_store,

            embedder=self.embedder,
        )

        self.reranker = Reranker()

    def evaluate(

        self,

        test_queries: List[TestQuery],

        top_k: int = 5,

    ):

        total = len(test_queries)

        passed = 0

        print("=" * 100)

        print("RETRIEVAL EVALUATION")

        print("=" * 100)

        for index, test in enumerate(test_queries, start=1):

            print("\n")

            print("=" * 100)

            print(f"Test Case {index}")

            print("=" * 100)

            print(f"Question : {test.query}")

            print(f"Expected : {test.expected}")

            print()

            results = self.retriever.retrieve(

                query=test.query,

                top_k=top_k,

            )

            results = self.reranker.rerank(

                query=test.query,

                results=results,

                top_k=3,

            )

            found = False

            for rank, result in enumerate(results, start=1):

                print("-" * 80)

                print(f"Rank : {rank}")

                print(f"Score : {result.score:.4f}")

                print(result.metadata)

                print()

                print(result.text)

                print()

                if test.expected.lower() in result.text.lower():

                    found = True

            if found:

                passed += 1

                print("✅ PASS")

            else:

                print("❌ FAIL")

        accuracy = passed / total * 100

        print("\n")

        print("=" * 100)

        print("SUMMARY")

        print("=" * 100)

        print(f"Passed : {passed}/{total}")

        print(f"Accuracy : {accuracy:.2f}%")

        print("=" * 100)