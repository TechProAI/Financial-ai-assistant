from unittest.mock import patch, MagicMock
from app.services.news_service import NewsService


def _fake_feed(titles_and_summaries):
    feed = MagicMock()
    entries = []
    for title, summary in titles_and_summaries:
        e = {"title": title, "summary": summary, "link": "https://x", "published": "2024-01-01"}
        entries.append(e)
    feed.entries = entries
    return feed


def test_get_ticker_news_positive_sentiment():
    svc = NewsService()
    with patch("app.services.news_service.feedparser.parse") as mock_parse:
        mock_parse.return_value = _fake_feed([("Stock surges on strong profit growth", "Record gains")])
        articles = svc.get_ticker_news("AAPL", limit=5)
        assert len(articles) == 1
        assert articles[0].sentiment == "positive"


def test_get_ticker_news_negative_sentiment():
    svc = NewsService()
    with patch("app.services.news_service.feedparser.parse") as mock_parse:
        mock_parse.return_value = _fake_feed([("Stock drops amid lawsuit and weak earnings", "Bearish decline")])
        articles = svc.get_ticker_news("AAPL", limit=5)
        assert articles[0].sentiment == "negative"


def test_get_market_news_neutral():
    svc = NewsService()
    with patch("app.services.news_service.feedparser.parse") as mock_parse:
        mock_parse.return_value = _fake_feed([("Fed holds rates steady", "No change expected")])
        articles = svc.get_market_news(limit=5)
        assert len(articles) == 1
        assert articles[0].sentiment == "neutral"


def test_news_fetch_handles_exception():
    svc = NewsService()
    with patch("app.services.news_service.feedparser.parse", side_effect=RuntimeError("fail")):
        articles = svc.get_ticker_news("AAPL")
        assert articles == []


def test_news_singleton():
    from app.services import news_service
    news_service._news = None
    a = news_service.get_news_service()
    b = news_service.get_news_service()
    assert a is b