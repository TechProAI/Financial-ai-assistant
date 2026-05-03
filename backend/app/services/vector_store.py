"""Pinecone vector store wrapper."""
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import VectorStoreError
from app.models.domain import RetrievedChunk
from app.services.llm_service import get_llm_service

logger = get_logger(__name__)


class VectorStore:
    """Pinecone-based vector store for RAG."""

    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.llm = get_llm_service()
        self._ensure_index()
        self.index = self.pc.Index(self.index_name)

    def _ensure_index(self) -> None:
        """Create index if it does not already exist."""
        existing = [idx.name for idx in self.pc.list_indexes()]
        if self.index_name not in existing:
            logger.info("creating_pinecone_index", name=self.index_name)
            self.pc.create_index(
                name=self.index_name,
                dimension=settings.PINECONE_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=settings.PINECONE_CLOUD,
                    region=settings.PINECONE_REGION,
                ),
            )

    def upsert(self, documents: List[Dict[str, Any]]) -> int:
        """Upsert documents with auto-generated embeddings. Each document has id, text, metadata."""
        try:
            texts = [d["text"] for d in documents]
            embeddings = self.llm.embed(texts)

            vectors = []
            for doc, emb in zip(documents, embeddings):
                md = dict(doc.get("metadata", {}))
                md["text"] = doc["text"]  # store text in metadata for retrieval
                vectors.append({"id": doc["id"], "values": emb, "metadata": md})

            # Batch upserts in groups of 100
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                self.index.upsert(vectors=vectors[i:i + batch_size])

            logger.info("upserted_documents", count=len(vectors))
            return len(vectors)
        except Exception as e:
            logger.error("upsert_failed", error=str(e))
            raise VectorStoreError(f"Upsert failed: {e}") from e

    def query(self, query_text: str, top_k: int = 5, filter: Optional[Dict[str, Any]] = None) -> List[RetrievedChunk]:
        """Semantic similarity search."""
        try:
            query_embedding = self.llm.embed([query_text])[0]
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter,
            )
            chunks: List[RetrievedChunk] = []
            for match in results.matches:
                md = match.metadata or {}
                chunks.append(
                    RetrievedChunk(
                        text=md.get("text", ""),
                        source=md.get("source", "unknown"),
                        title=md.get("title", "Untitled"),
                        score=float(match.score),
                        metadata=md,
                    )
                )
            return chunks
        except Exception as e:
            logger.error("query_failed", error=str(e))
            raise VectorStoreError(f"Query failed: {e}") from e


_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store