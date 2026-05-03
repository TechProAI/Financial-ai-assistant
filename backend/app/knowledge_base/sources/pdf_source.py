"""Ingest PDF files into the knowledge base.

Allows users to upload any financial PDF (research reports, guides, etc.)
and add it to the RAG knowledge base.
"""
import os
from typing import List, Dict
from app.core.logging import get_logger

logger = get_logger(__name__)


def extract_from_pdf(pdf_path: str, source_name: str = None) -> List[Dict[str, str]]:
    """Extract text from a PDF and return as documents ready for ingestion."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.error("pymupdf_not_installed", hint="pip install PyMuPDF")
        return []

    if not os.path.exists(pdf_path):
        logger.error("pdf_not_found", path=pdf_path)
        return []

    source = source_name or os.path.basename(pdf_path)
    filename = os.path.splitext(os.path.basename(pdf_path))[0]

    try:
        doc = fitz.open(pdf_path)
        articles = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().strip()

            if len(text) < 50:
                continue

            articles.append({
                "id": f"pdf_{filename.lower().replace(' ', '_')[:30]}_p{page_num + 1}",
                "title": f"{source} - Page {page_num + 1}",
                "source": source,
                "category": "uploaded_document",
                "text": text[:2000],  # Cap per page
            })

        doc.close()
        logger.info("pdf_extracted", path=pdf_path, pages=len(articles))
        return articles

    except Exception as e:
        logger.error("pdf_extraction_failed", path=pdf_path, error=str(e))
        return []