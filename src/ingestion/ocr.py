"""
OCR Service

Provides OCR functionality for images and scanned documents.
"""

from pathlib import Path
from typing import List, Optional

from src.models.model_manager import ModelManager


class OCRService:
    """
    OCR Service using EasyOCR.
    """

    def __init__(self, languages: Optional[List[str]] = None):

        self.manager = ModelManager()

        self.reader = self.manager.load_ocr(
            languages=languages
        )

    def extract_text(self, image_path: str) -> str:
        """
        Extract text from an image.

        Parameters
        ----------
        image_path : str
            Path to the image.

        Returns
        -------
        str
            Extracted text.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"{image_path} does not exist."
            )

        results = self.reader.readtext(str(image_path))

        text = "\n".join(
            result[1]
            for result in results
        )

        return text.strip()