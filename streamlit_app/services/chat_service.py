"""
Chat Service

Acts as the bridge between Streamlit and the RAG backend.
"""

import time

from src.llm.response_generator import ResponseGenerator


class ChatService:

    def __init__(self):

        self.generator = ResponseGenerator()

    def ask(self, question: str):

        start = time.perf_counter()

        response = self.generator.generate(question)

        elapsed = time.perf_counter() - start

        return response, elapsed