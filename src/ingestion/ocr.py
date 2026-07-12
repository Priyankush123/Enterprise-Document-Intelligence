"""
OCR Service

Provides OCR functionality for images and scanned documents.
"""

from pathlib import Path

import easyocr


class OCRService:
    """
    OCR Service using EasyOCR.
    """

    def __init__(self, languages=None):

        if languages is None:
            languages = ["en"]

        self.reader = easyocr.Reader(languages)

    def extract_text(self, image_path: str) -> str:
        """
        Extract text from an image.
        """

        image_path = Path(image_path)

        results = self.reader.readtext(str(image_path))

        text = "\n".join(
            result[1]
            for result in results
        )

        return text.strip()