"""
Model Manager

Centralized manager for reusable AI models.
"""

from typing import Optional


class ModelManager:
    """
    Singleton manager for reusable AI models.
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._ocr = None
            cls._instance._embedder = None
            cls._instance._reranker = None
            cls._instance._llm = None

        return cls._instance

    # ---------------- OCR ---------------- #

    def load_ocr(self, languages=None):

        if self._ocr is None:

            from easyocr import Reader

            if languages is None:
                languages = ["en"]

            self._ocr = Reader(
                languages,
                gpu=False,
            )

        return self._ocr

    def get_ocr(self):

        return self._ocr

    # ------------ Embedder ------------ #

    def load_embedder(
        self,
        model_name: str,
    ):

        if self._embedder is None:

            from sentence_transformers import (
                SentenceTransformer,
            )

            self._embedder = SentenceTransformer(
                model_name
            )

        return self._embedder

    def get_embedder(self):

        return self._embedder

    # ------------ Reranker ------------ #

    def load_reranker(
        self,
        model_name: str,
    ):

        if self._reranker is None:

            from sentence_transformers import (
                CrossEncoder,
            )

            self._reranker = CrossEncoder(
                model_name
            )

        return self._reranker

    def get_reranker(self):

        return self._reranker

    # ---------------- LLM ---------------- #

    def set_llm(self, llm):

        self._llm = llm

    def get_llm(self):

        return self._llm