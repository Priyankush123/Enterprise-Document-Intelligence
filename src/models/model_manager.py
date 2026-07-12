"""
Model Manager

Responsible for loading and managing heavy AI models.

Models are initialized only once and reused
throughout the application.
"""

from typing import Optional

from src.ingestion.ocr import OCRService


class ModelManager:
    """
    Singleton manager for AI models.
    """

    _instance = None

    _ocr = None
    _embedder = None
    _reranker = None
    _llm = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def get_ocr(self):

        if self._ocr is None:
            self._ocr = OCRService()

        return self._ocr

    def get_embedder(self):

        return self._embedder

    def get_reranker(self):

        return self._reranker

    def get_llm(self):

        return self._llm