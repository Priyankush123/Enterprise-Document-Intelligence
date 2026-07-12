"""
Text Loader

Loads plain text (.txt) files and converts them into
the standard Document schema.
"""

from pathlib import Path

from src.ingestion.base_loader import BaseLoader
from src.ingestion.document_schema import (
    Document,
    DocumentMetadata,
    Page,
)


class TextLoader(BaseLoader):
    """
    Loader for plain text files.
    """

    SUPPORTED_EXTENSIONS = [".txt"]

    def load(self, file_path: str) -> Document:

        text_path = self.validate_file(file_path)

        with open(text_path, "r", encoding="utf-8") as file:
            text = file.read()

        page = Page(
            page_number=1,
            text=text
        )

        metadata = DocumentMetadata(
            title=text_path.stem,
            page_count=1,
        )

        return Document(
            filename=text_path.name,
            filetype="txt",
            pages=[page],
            metadata=metadata,
        )