"""
Base loader class for all document loaders.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import shutil
import logging


logger = logging.getLogger(__name__)


class BaseLoader(ABC):
    """
    Base class for all document loaders.
    """

    # Child classes will override this
    SUPPORTED_EXTENSIONS = []

    def __init__(self, upload_dir: str = "data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, file_path: str) -> Path:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        return path

    def save_uploaded_file(self, source_path: str) -> Path:
        source = self.validate_file(source_path)

        destination = self.upload_dir / source.name

        shutil.copy(source, destination)

        logger.info(f"Saved {destination}")

        return destination

    @abstractmethod
    def load(self, file_path: str):
        pass