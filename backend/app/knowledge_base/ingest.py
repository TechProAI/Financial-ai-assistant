"""Unified ingestion pipeline: fetches from all sources and loads into Pinecone.

Sources:
1. Wikipedia — free, CC-licensed financial articles
2. LLM Generator — AI-generated articles on a curated syllabus
3. PDF — user-uploaded documents
"""
from typing import List, Dict, Optional
from app.services.vector_store import get_vector_store
from app.core.logging import get_logger

logger = get_logger(__name__)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80


def _chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks for better retrieval."""
    if len(text) <= size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _prepare_documents(articles: List[Dict[str, str]]) -> List[Dict]:
    """Chunk articles into documents ready for Pinecone upsert."""
    docs = []
    for article in articles:
        chunks = _chunk_text(article["text"])
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"{article['id']}_chunk_{i}",
                "text": chunk,
                "metadata": {
                    "title": article["title"],
                    "source": article["source"],
                    "category": article.get("category", "general"),
                    "article_id": article["id"],
                    "chunk_index": i,
                },
            })
    return docs


def ingest_from_wikipedia() -> int:
    """Fetch Wikipedia articles and ingest into Pinecone."""
    from app.knowledge_base.sources.wikipedia_source import fetch_wikipedia_articles

    logger.info("ingesting_wikipedia")
    articles = fetch_wikipedia_articles()
    if not articles:
        logger.warning("no_wikipedia_articles_fetched")
        return 0

    docs = _prepare_documents(articles)
    vs = get_vector_store()
    count = vs.upsert(docs)
    logger.info("wikipedia_ingestion_complete", articles=len(articles), chunks=count)
    return count


def ingest_from_generator() -> int:
    """Generate articles using OpenAI and ingest into Pinecone."""
    from app.knowledge_base.sources.llm_generator import generate_articles

    logger.info("ingesting_generated_articles")
    articles = generate_articles()
    if not articles:
        logger.warning("no_articles_generated")
        return 0

    docs = _prepare_documents(articles)
    vs = get_vector_store()
    count = vs.upsert(docs)
    logger.info("generator_ingestion_complete", articles=len(articles), chunks=count)
    return count


def ingest_from_pdf(pdf_path: str, source_name: str = None) -> int:
    """Extract text from a PDF and ingest into Pinecone."""
    from app.knowledge_base.sources.pdf_source import extract_from_pdf

    logger.info("ingesting_pdf", path=pdf_path)
    articles = extract_from_pdf(pdf_path, source_name)
    if not articles:
        logger.warning("no_content_from_pdf", path=pdf_path)
        return 0

    docs = _prepare_documents(articles)
    vs = get_vector_store()
    count = vs.upsert(docs)
    logger.info("pdf_ingestion_complete", pages=len(articles), chunks=count)
    return count


def ingest_all(
    include_wikipedia: bool = True,
    include_generated: bool = True,
    pdf_paths: Optional[List[str]] = None,
) -> Dict[str, int]:
    """Run the full ingestion pipeline from all sources."""
    results = {}

    if include_wikipedia:
        results["wikipedia"] = ingest_from_wikipedia()

    if include_generated:
        results["generated"] = ingest_from_generator()

    if pdf_paths:
        pdf_total = 0
        for path in pdf_paths:
            pdf_total += ingest_from_pdf(path)
        results["pdf"] = pdf_total

    total = sum(results.values())
    logger.info("full_ingestion_complete", results=results, total_chunks=total)
    return results