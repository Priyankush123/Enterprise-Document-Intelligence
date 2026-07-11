"""
Base loader class for all document loaders.

Every document loader (PDF, DOCX, PPTX, TXT, Image)
inherits from this class.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import shutil
import logging


logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """
    Abstract base class for document loaders.
    """

    def __init__(self, upload_dir: str = "data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file_path: str) -> Path:
        """
        Validate that the file exists.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        return path

    def save_uploaded_file(self, source_path: str) -> Path:
        """
        Save uploaded file inside uploads directory.
        """

        source = self.validate_file(source_path)

        destination = self.upload_dir / source.name

        shutil.copy(source, destination)

        logger.info("Saved file: %s", destination)

        return destination

    @abstractmethod
    def load(self, file_path: str):
        """
        Extract document contents.

        Must be implemented by subclasses.
        """
        pass