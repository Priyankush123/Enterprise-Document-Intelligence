"""
Text Cleaner

Cleans extracted document text before chunking.
"""

import re
from copy import deepcopy

from src.ingestion.document_schema import Document


class TextCleaner:
    """
    Cleans extracted text while preserving document structure.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean a single text block.
        """

        if not text:
            return ""

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove trailing spaces
        text = "\n".join(
            line.strip()
            for line in text.splitlines()
        )

        return text.strip()

    def process(self, document: Document) -> Document:
        """
        Clean every page in the document.
        """

        cleaned_document = deepcopy(document)

        for page in cleaned_document.pages:
            page.text = self.clean_text(page.text)

        return cleaned_document