"""
Response Generator

Combines retrieval with the LLM to generate answers.
"""

from src.llm.llm_client import LLMClient
from src.llm.prompt_template import PromptTemplate
from src.llm.response_schema import RAGResponse
from src.retrieval.retrieval_pipeline import RetrievalPipeline


class ResponseGenerator:
    """
    Complete RAG pipeline.
    """

    def __init__(self):

        self.pipeline = RetrievalPipeline()

        self.llm = LLMClient()

    def generate(
        self,
        question: str,
    ) -> RAGResponse:
        """
        Generate an answer using Retrieval-Augmented Generation.
        """

        context, sources = self.pipeline.retrieve_context(
            question
        )

        prompt = PromptTemplate.build(
            question=question,
            context=context,
        )

        answer = self.llm.generate(prompt)

        return RAGResponse(

            question=question,

            answer=answer,

            sources=sources,

            model_name=self.llm.model_name,
        )