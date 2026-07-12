"""
Recursive Chunker

Splits documents into overlapping chunks using
LangChain's RecursiveCharacterTextSplitter.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.chunking.chunk_schema import (
    ChunkMetadata,
    DocumentChunk,
)
from src.ingestion.document_schema import Document


class RecursiveChunker:
    """
    Recursive character-based chunker.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(self, document: Document) -> list[DocumentChunk]:
        """
        Split a document into chunks.
        """

        chunks = []

        for page in document.pages:

            split_text = self.text_splitter.split_text(
                page.text
            )

            for chunk_number, text in enumerate(
                split_text,
                start=1,
            ):

                chunk = DocumentChunk(

                    chunk_id=self.generate_chunk_id(
                        document.filename,
                        page.page_number,
                        chunk_number,
                    ),

                    text=text,

                    metadata=ChunkMetadata(

                        document_name=document.filename,

                        file_type=document.filetype,

                        page_number=page.page_number,

                        chunk_number=chunk_number,
                    ),
                )

                chunks.append(chunk)

        return chunks

    @staticmethod
    def generate_chunk_id(
        filename: str,
        page_number: int,
        chunk_number: int,
    ) -> str:
        """
        Generate deterministic chunk IDs.
        """

        filename = filename.replace(" ", "_")

        return (
            f"{filename}"
            f"::page_{page_number:03}"
            f"::chunk_{chunk_number:03}"
        )