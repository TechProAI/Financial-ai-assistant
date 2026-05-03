from unittest.mock import patch, MagicMock
from app.agents.news_sentiment import NewsSentimentAgent
from app.models.domain import NewsArticle


def test_news_agent_general(mock_llm, base_state):
    mock_llm.chat.return_value = "Market is mixed."
    with patch("app.agents.news_sentiment.get_news_service") as mock_ns:
        instance = MagicMock()
        instance.get_market_news.return_value = [
            NewsArticle(title="Fed holds rates", summary="...", url="https://x", published="", source="Yahoo",
                        sentiment="neutral", sentiment_score=0.0),
        ]
        mock_ns.return_value = instance
        agent = NewsSentimentAgent()
        result = agent(base_state)
        assert len(result["news_items"]) == 1