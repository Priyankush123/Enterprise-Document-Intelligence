"""
Document Preprocessor

Coordinates all preprocessing steps before chunking.
"""

from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.normalizer import TextNormalizer
from src.preprocessing.language import LanguageDetector


class DocumentPreprocessor:
    """
    Orchestrates preprocessing of documents.
    """

    def __init__(self):

        self.cleaner = TextCleaner()

        self.normalizer = TextNormalizer()

        self.language_detector = LanguageDetector()

    def process(self, document):

        document = self.cleaner.process(document)

        document = self.normalizer.process(document)

        document = self.language_detector.process(document)

        return document