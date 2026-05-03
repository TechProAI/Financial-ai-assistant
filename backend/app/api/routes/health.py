"""Health check endpoint."""
from fastapi import APIRouter
from app import __version__
from app.models.schemas import HealthResponse
from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=__version__,
        services={
            "llm": settings.OPENAI_MODEL,
            "vector_store": settings.PINECONE_INDEX_NAME,
            "market_data": settings.MARKET_DATA_PROVIDER,
        },
    )