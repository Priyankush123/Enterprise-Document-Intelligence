"""
PDF Loader

Reads a PDF document using PyMuPDF and converts it into the
standard Document schema used throughout the project.
"""

from pathlib import Path
from typing import List
from datetime import datetime

import fitz  # PyMuPDF

from src.ingestion.base_loader import BaseLoader
from src.ingestion.document_schema import (
    Document,
    DocumentMetadata,
    Page,
)


class PDFLoader(BaseLoader):
    """
    Loader for PDF documents.
    """

    SUPPORTED_EXTENSIONS = [".pdf"]

    def load(self, file_path: str) -> Document:
        """
        Load a PDF and return a standardized Document object.
        """

        pdf_path = self.validate_file(file_path)

        pdf = fitz.open(pdf_path)

        metadata = self.extract_metadata(pdf)

        pages = self.extract_pages(pdf)

        pdf.close()

        return Document(
            filename=pdf_path.name,
            filetype="pdf",
            pages=pages,
            metadata=metadata,
        )

    def extract_pages(self, pdf: fitz.Document) -> List[Page]:
        """
        Extract text from every page.
        """

        pages = []

        for index, page in enumerate(pdf):

            text = page.get_text("text")

            pages.append(
                Page(
                    page_number=index + 1,
                    text=text.strip()
                )
            )

        return pages

    def extract_metadata(
        self,
        pdf: fitz.Document
    ) -> DocumentMetadata:
        """
        Extract PDF metadata.
        """

        meta = pdf.metadata

        return DocumentMetadata(
            title=meta.get("title"),
            author=meta.get("author"),
            subject=meta.get("subject"),
            creator=meta.get("creator"),
            producer=meta.get("producer"),
            created_at=self.parse_pdf_date(meta.get("creationDate")),
            modified_at=self.parse_pdf_date(meta.get("modDate")),
            page_count=len(pdf)
        )

    @staticmethod
    def parse_pdf_date(date_string: str):
        """
        Convert PDF date string to Python datetime.

        Example:
        D:20240125113045
        """

        if not date_string:
            return None

        try:

            if date_string.startswith("D:"):
                date_string = date_string[2:]

            return datetime.strptime(
                date_string[:14],
                "%Y%m%d%H%M%S"
            )

        except Exception:
            return None