"""Knowledge base ingestion pipeline.

Usage:
    # Ingest everything (Wikipedia + generated articles):
    python -m scripts.ingest_kb

    # Wikipedia only (faster, no OpenAI cost):
    python -m scripts.ingest_kb --wikipedia-only

    # Generated articles only:
    python -m scripts.ingest_kb --generated-only

    # Ingest a PDF:
    python -m scripts.ingest_kb --pdf path/to/document.pdf
"""
import argparse
from app.core.logging import configure_logging, get_logger
from dotenv import load_dotenv

load_dotenv()


def main():
    configure_logging()
    logger = get_logger(__name__)

    parser = argparse.ArgumentParser(description="Finnie AI Knowledge Base Ingestion")
    parser.add_argument("--wikipedia-only", action="store_true", help="Only ingest from Wikipedia")
    parser.add_argument("--generated-only", action="store_true", help="Only ingest LLM-generated articles")
    parser.add_argument("--pdf", type=str, help="Path to a PDF file to ingest")
    parser.add_argument("--all", action="store_true", default=True, help="Ingest from all sources")
    args = parser.parse_args()

    from app.knowledge_base.ingest import ingest_all, ingest_from_wikipedia, ingest_from_generator, ingest_from_pdf

    if args.pdf:
        count = ingest_from_pdf(args.pdf)
        print(f"✓ Ingested {count} chunks from PDF")
        return

    if args.wikipedia_only:
        count = ingest_from_wikipedia()
        print(f"✓ Ingested {count} chunks from Wikipedia")
        return

    if args.generated_only:
        count = ingest_from_generator()
        print(f"✓ Ingested {count} chunks from generated articles")
        return

    # Default: ingest everything
    print("Starting full ingestion pipeline...")
    print("Step 1/2: Fetching from Wikipedia...")
    results = ingest_all(include_wikipedia=True, include_generated=True)

    print("\n=== Ingestion Complete ===")
    for source, count in results.items():
        print(f"  {source}: {count} chunks")
    print(f"  TOTAL: {sum(results.values())} chunks")
    print("✓ Knowledge base is ready")


if __name__ == "__main__":
    main()