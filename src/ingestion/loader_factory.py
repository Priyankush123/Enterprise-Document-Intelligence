"""
Loader Factory

Returns the appropriate loader based on file extension.
"""

from pathlib import Path

from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.docx_loader import DOCXLoader
from src.ingestion.pptx_loader import PPTXLoader
from src.ingestion.text_loader import TextLoader
from src.ingestion.image_loader import ImageLoader
from src.ingestion.excel_loader import ExcelLoader


class LoaderFactory:
    """
    Factory for creating document loaders.
    """

    _loaders = [
        PDFLoader,
        DOCXLoader,
        PPTXLoader,
        TextLoader,
        ImageLoader,
        ExcelLoader,
    ]

    @classmethod
    def get_loader(cls, file_path: str):

        extension = Path(file_path).suffix.lower()

        for loader_cls in cls._loaders:

            if extension in loader_cls.SUPPORTED_EXTENSIONS:
                return loader_cls()

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    @classmethod
    def supported_extensions(cls):

        extensions = []

        for loader_cls in cls._loaders:
            extensions.extend(loader_cls.SUPPORTED_EXTENSIONS)

        return sorted(extensions)