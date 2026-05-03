"""News fetching with lightweight sentiment scoring."""
from typing import List, Optional
import feedparser
from app.core.logging import get_logger
from app.models.domain import NewsArticle

logger = get_logger(__name__)

POSITIVE_TERMS = {"gain", "surge", "rally", "beat", "growth", "profit", "upgrade", "bullish", "record", "strong"}
NEGATIVE_TERMS = {"loss", "drop", "fall", "miss", "decline", "downgrade", "bearish", "weak", "cut", "lawsuit", "crash"}


class NewsService:
    """Fetches market news via Yahoo Finance RSS feeds."""

    BASE_URL = "https://feeds.finance.yahoo.com/rss/2.0/headline"

    def get_ticker_news(self, ticker: str, limit: int = 5) -> List[NewsArticle]:
        """Fetch news for a specific ticker."""
        url = f"{self.BASE_URL}?s={ticker.upper()}&region=US&lang=en-US"
        return self._parse_feed(url, limit)

    def get_market_news(self, limit: int = 10) -> List[NewsArticle]:
        """Fetch broad market news."""
        url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US"
        return self._parse_feed(url, limit)

    def _parse_feed(self, url: str, limit: int) -> List[NewsArticle]:
        try:
            feed = feedparser.parse(url)
            articles: List[NewsArticle] = []
            for entry in feed.entries[:limit]:
                text = f"{entry.get('title', '')} {entry.get('summary', '')}"
                sentiment, score = self._score_sentiment(text)
                articles.append(
                    NewsArticle(
                        title=entry.get("title", ""),
                        summary=entry.get("summary", "")[:300],
                        url=entry.get("link", ""),
                        published=entry.get("published", ""),
                        source="Yahoo Finance",
                        sentiment=sentiment,
                        sentiment_score=score,
                    )
                )
            return articles
        except Exception as e:
            logger.warning("news_fetch_failed", url=url, error=str(e))
            return []

    @staticmethod
    def _score_sentiment(text: str) -> tuple[str, float]:
        """Very lightweight keyword-based sentiment; fine for demonstration."""
        t = text.lower()
        pos = sum(1 for w in POSITIVE_TERMS if w in t)
        neg = sum(1 for w in NEGATIVE_TERMS if w in t)
        if pos == 0 and neg == 0:
            return "neutral", 0.0
        score = (pos - neg) / (pos + neg)
        if score > 0.2:
            return "positive", round(score, 2)
        if score < -0.2:
            return "negative", round(score, 2)
        return "neutral", round(score, 2)


_news: Optional[NewsService] = None


def get_news_service() -> NewsService:
    global _news
    if _news is None:
        _news = NewsService()
    return _news