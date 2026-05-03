"""Shared pytest fixtures."""
import pytest
from unittest.mock import MagicMock
from app.models.schemas import UserProfile


@pytest.fixture
def mock_llm(mocker):
    """Patch LLMService across the codebase."""
    mock = MagicMock()
    mock.chat.return_value = "mocked response"
    mock.embed.return_value = [[0.1] * 1536]
    mocker.patch("app.services.llm_service.get_llm_service", return_value=mock)
    mocker.patch("app.agents.supervisor.get_llm_service", return_value=mock)
    mocker.patch("app.agents.education.get_llm_service", return_value=mock)
    mocker.patch("app.agents.market_intelligence.get_llm_service", return_value=mock)
    mocker.patch("app.agents.portfolio_analysis.get_llm_service", return_value=mock)
    mocker.patch("app.agents.news_sentiment.get_llm_service", return_value=mock)
    return mock


@pytest.fixture
def mock_vector_store(mocker):
    from app.models.domain import RetrievedChunk
    mock = MagicMock()
    mock.query.return_value = [
        RetrievedChunk(text="A stock is ownership", source="kb", title="What is a Stock", score=0.92),
    ]
    mock.upsert.return_value = 1
    mocker.patch("app.services.vector_store.get_vector_store", return_value=mock)
    mocker.patch("app.services.rag_service.get_vector_store", return_value=mock)
    return mock


@pytest.fixture
def mock_market(mocker):
    mock = MagicMock()
    mock.get_quote.return_value = {
        "ticker": "AAPL", "price": 190.5, "change": 1.2, "change_percent": 0.63,
        "volume": 50000000, "market_cap": 3e12, "pe_ratio": 28.5,
        "day_high": 192.0, "day_low": 189.0, "company_name": "Apple Inc",
        "sector": "Technology", "timestamp": "2024-01-01T00:00:00",
    }
    mocker.patch("app.services.market_data.get_market_data_service", return_value=mock)
    mocker.patch("app.agents.market_intelligence.get_market_data_service", return_value=mock)
    return mock


@pytest.fixture
def sample_profile():
    return UserProfile(risk_appetite="moderate", experience_level="beginner", goals=["retirement"])


@pytest.fixture
def base_state():
    return {
        "session_id": "test-session",
        "user_message": "What is a stock?",
        "chat_history": [],
        "user_profile": None,
        "agent_trace": [],
    }