"""
Text Normalizer

Normalizes Unicode text for better embedding quality.
"""

import unicodedata
from copy import deepcopy

from src.ingestion.document_schema import Document


class TextNormalizer:
    """
    Normalizes extracted text.
    """

    @staticmethod
    def normalize_text(text: str) -> str:

        if not text:
            return ""

        # Unicode normalization
        text = unicodedata.normalize("NFKC", text)

        # Smart quotes
        text = text.replace(""", '"')
        text = text.replace(""", '"')

        # Curly apostrophes
        text = text.replace("'", "'")
        text = text.replace("'", "'")

        # Long dash
        text = text.replace("–", "-")
        text = text.replace("—", "-")

        REPLACEMENTS = {
            "\u201c": '"',   # Left double quote
            "\u201d": '"',   # Right double quote
            "\u2018": "'",   # Left single quote
            "\u2019": "'",   # Right single quote
            "\u2013": "-",   # En dash
            "\u2014": "-",   # Em dash
        }

        for old, new in REPLACEMENTS.items():
            text = text.replace(old, new)

        return text

    def process(self, document: Document) -> Document:

        normalized_document = deepcopy(document)

        for page in normalized_document.pages:

            page.text = self.normalize_text(page.text)

        return normalized_document