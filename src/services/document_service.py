"""
Document Service

Provides document management functionality for the application.
"""

from typing import Any

from src.vectordb.chroma_store import ChromaVectorStore


class DocumentService:
    """
    Service for managing indexed documents.
    """

    def __init__(
        self,
        vector_store: ChromaVectorStore | None = None,
    ):

        self.vector_store = (
            vector_store
            if vector_store is not None
            else ChromaVectorStore()
        )

    # --------------------------------------------------

    def get_documents(self):

        return self.vector_store.list_documents()

    # --------------------------------------------------

    def delete_document(
        self,
        document_name: str,
    ) -> bool:

        if not self.vector_store.document_exists(
            document_name
        ):
            return False

        self.vector_store.delete_document(
            document_name
        )

        return True

    # --------------------------------------------------

    def document_exists(
        self,
        document_name: str,
    ) -> bool:

        return self.vector_store.document_exists(
            document_name
        )

    # --------------------------------------------------

    def get_statistics(self) -> dict[str, Any]:

        return {

            "documents":
                self.vector_store.count_documents(),

            "chunks":
                self.vector_store.count_chunks(),

            "collection":
                self.vector_store.collection.name,
        }

    # --------------------------------------------------

    def clear_database(self):

        self.vector_store.clear_database()

    # --------------------------------------------------

    def get_collection_info(self):

        return self.vector_store.get_collection_info()