"""
Image Loader

Loads image files and extracts text using OCR.
"""

from pathlib import Path

from src.ingestion.base_loader import BaseLoader
from src.ingestion.document_schema import (
    Document,
    DocumentMetadata,
    Page,
)
from src.models.model_manager import ModelManager


class ImageLoader(BaseLoader):
    """
    Loader for image documents.
    """

    SUPPORTED_EXTENSIONS = [
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
    ]

    def __init__(self, upload_dir: str = "data/uploads"):
        super().__init__(upload_dir)

        self.model_manager = ModelManager()
        self.ocr = self.model_manager.get_ocr()

    def load(self, file_path: str) -> Document:

        image_path = self.validate_file(file_path)

        extracted_text = self.ocr.extract_text(str(image_path))

        page = Page(
            page_number=1,
            text=extracted_text
        )

        metadata = DocumentMetadata(
            title=Path(file_path).stem,
            page_count=1,
        )

        return Document(
            filename=image_path.name,
            filetype=image_path.suffix.lower()[1:],
            pages=[page],
            metadata=metadata,
        )