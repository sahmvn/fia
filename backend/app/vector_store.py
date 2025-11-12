import os
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.config import settings


class VectorStore:
    """Manages the vector database for manipulation patterns."""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key
        )
        self.persist_directory = settings.chroma_persist_directory
        self.collection_name = "manipulation_patterns"
        self._vector_store: Optional[Chroma] = None

    def initialize(self):
        """Initialize or load the vector store."""
        os.makedirs(self.persist_directory, exist_ok=True)

        self._vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

        # Verify initialization
        if self._vector_store is None:
            raise RuntimeError("Failed to initialize vector store")

        print(f"✓ Vector store initialized (collection: {self.collection_name})")
        return self

    def add_documents(self, documents: List[Document]):
        """Add documents to the vector store."""
        if not self._vector_store:
            raise ValueError("Vector store not initialized. Call initialize() first.")

        self._vector_store.add_documents(documents)
        print(f"Added {len(documents)} documents to vector store")

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents."""
        if not self._vector_store:
            raise ValueError("Vector store not initialized. Call initialize() first.")

        return self._vector_store.similarity_search(query, k=k)

    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """Search for similar documents with relevance scores."""
        if not self._vector_store:
            raise ValueError("Vector store not initialized. Call initialize() first.")

        return self._vector_store.similarity_search_with_score(query, k=k)

    def get_retriever(self, search_kwargs: Optional[dict] = None):
        """Get a retriever for the vector store."""
        if not self._vector_store:
            raise ValueError("Vector store not initialized. Call initialize() first.")

        if search_kwargs is None:
            search_kwargs = {"k": 4}

        return self._vector_store.as_retriever(search_kwargs=search_kwargs)

    def clear(self):
        """Clear all documents from the vector store."""
        print(f"Clearing collection: {self.collection_name}")

        if self._vector_store:
            try:
                self._vector_store.delete_collection()
                print("✓ Collection deleted")
            except Exception as e:
                print(f"Warning: Error deleting collection: {e}")

        self._vector_store = None
        print("Reinitializing vector store...")

        # Reinitialize after clearing
        self.initialize()

        # Double-check initialization worked
        if self._vector_store is None:
            raise RuntimeError("Failed to reinitialize vector store after clear")

        return self

    @property
    def vector_store(self):
        """Get the underlying vector store."""
        return self._vector_store


# Global vector store instance
vector_store = VectorStore()
