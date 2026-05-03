"""RAG orchestration: retrieve -> re-rank -> format with citations."""
from typing import List, Tuple
from app.services.vector_store import get_vector_store
from app.models.domain import RetrievedChunk
from app.models.schemas import Citation
from app.core.logging import get_logger

logger = get_logger(__name__)

MIN_SCORE = 0.5


class RAGService:
    """Retrieves and formats context chunks for grounded generation."""

    def __init__(self):
        self.vs = get_vector_store()

    def retrieve(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        """Retrieve relevant chunks, filtering out low-scoring ones."""
        chunks = self.vs.query(query, top_k=top_k)
        filtered = [c for c in chunks if c.score >= MIN_SCORE]
        logger.info("rag_retrieved", query=query[:60], returned=len(filtered), total=len(chunks))
        return filtered

    def format_context(self, chunks: List[RetrievedChunk]) -> Tuple[str, List[Citation]]:
        """Return a context string and parallel citations list."""
        if not chunks:
            return "", []

        context_parts = []
        citations = []
        for i, c in enumerate(chunks, start=1):
            context_parts.append(f"[{i}] {c.title}\n{c.text}")
            citations.append(
                Citation(
                    source=c.source,
                    title=c.title,
                    snippet=c.text[:200] + ("..." if len(c.text) > 200 else ""),
                    score=round(c.score, 4),
                )
            )
        return "\n\n".join(context_parts), citations


_rag: "RAGService | None" = None


def get_rag_service() -> RAGService:
    global _rag
    if _rag is None:
        _rag = RAGService()
    return _rag