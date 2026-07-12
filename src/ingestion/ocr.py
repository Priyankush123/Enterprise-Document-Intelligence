"""
OCR Service

Provides OCR functionality for images and scanned documents.
"""

from pathlib import Path
from typing import List, Optional

import easyocr


class OCRService:
    """
    OCR Service using EasyOCR.

    The EasyOCR Reader is initialized only once and reused
    for all OCR requests.
    """

    _reader = None

    def __init__(
        self,
        languages: Optional[List[str]] = None
    ):

        if languages is None:
            languages = ["en"]

        if OCRService._reader is None:

            OCRService._reader = easyocr.Reader(
                languages,
                gpu=False
            )

    def extract_text(
        self,
        image_path: str
    ) -> str:

        image_path = Path(image_path)

        results = OCRService._reader.readtext(
            str(image_path)
        )

        text = "\n".join(
            result[1]
            for result in results
        )

        return text.strip()