"""News & Sentiment agent: fetches recent news and characterizes sentiment."""
from typing import Dict, Any
from dataclasses import asdict
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.news_service import get_news_service
from app.services.llm_service import get_llm_service

SYSTEM_PROMPT = """You are a financial news analyst. Given recent headlines, summarize the key themes
and overall sentiment (positive/negative/neutral) in 3-5 sentences. Stay factual and neutral.
Do not speculate about future prices."""


class NewsSentimentAgent(BaseAgent):
    name = "news_sentiment"

    def __init__(self):
        self.news = get_news_service()
        self.llm = get_llm_service()

    def run(self, state: GraphState) -> Dict[str, Any]:
        tickers = state.get("tickers") or []
        if tickers:
            articles = []
            for t in tickers[:2]:
                articles.extend(self.news.get_ticker_news(t, limit=5))
        else:
            articles = self.news.get_market_news(limit=8)

        if not articles:
            return {
                "news_items": [],
                "draft_answer": "I couldn't fetch news right now. Please try again shortly.",
            }

        headlines = "\n".join(
            f"- [{a.sentiment}] {a.title} ({a.source})" for a in articles
        )
        answer = self.llm.chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"User question: {state['user_message']}\n\nHeadlines:\n{headlines}"},
            ],
            temperature=0.3,
        )
        return {
            "news_items": [asdict(a) for a in articles],
            "draft_answer": answer,
        }