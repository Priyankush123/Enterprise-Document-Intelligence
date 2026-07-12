"""
Language Detection

Detects the language of extracted document text.
"""

from copy import deepcopy

from langdetect import detect, LangDetectException

from src.ingestion.document_schema import Document


class LanguageDetector:
    """
    Detects the language of a document.
    """

    def detect_language(self, text: str) -> str:

        if not text.strip():
            return "unknown"

        try:
            return detect(text)

        except LangDetectException:
            return "unknown"

    def process(self, document: Document) -> Document:

        processed_document = deepcopy(document)

        combined_text = "\n".join(
            page.text
            for page in processed_document.pages
        )

        language = self.detect_language(combined_text)

        processed_document.metadata.language = language

        return processed_document