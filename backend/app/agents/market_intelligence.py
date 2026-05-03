"""Market Intelligence agent: fetches real-time quotes and basic fundamentals."""
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.market_data import get_market_data_service
from app.services.llm_service import get_llm_service
from app.core.exceptions import MarketDataError

SYSTEM_PROMPT = """You are a market analyst. Given real-time market data, produce a concise
beginner-friendly summary highlighting: current price, daily change, trading volume, key
fundamentals (market cap, P/E), and one or two observations about the data.
Do NOT make price predictions or give buy/sell advice."""


class MarketIntelligenceAgent(BaseAgent):
    name = "market_intelligence"

    def __init__(self):
        self.md = get_market_data_service()
        self.llm = get_llm_service()

    def run(self, state: GraphState) -> Dict[str, Any]:
        tickers = state.get("tickers") or []
        if not tickers:
            return {
                "draft_answer": "I can fetch market data, but I couldn't detect a ticker in your message. "
                                "Could you specify one? Examples:\n"
                                "- US stocks: AAPL, MSFT, TSLA, GOOGL\n"
                                "- Indian stocks: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS\n"
                                "- Or just say the company name like 'Reliance' or 'Apple'",
                "market_data": {},
            }

        quotes: Dict[str, Any] = {}
        errors = []
        for t in tickers[:5]:
            try:
                quotes[t] = self.md.get_quote(t)
            except MarketDataError as e:
                errors.append(str(e))

        if not quotes:
            return {
                "draft_answer": "I couldn't fetch live data for those tickers right now. "
                                "Please verify the symbols and try again.",
                "market_data": {"errors": errors},
            }

        summary_input = "\n".join(
            f"{t}: price=${q['price']} ({q['change_percent']:+.2f}%), volume={q['volume']}, "
            f"market_cap={q.get('market_cap')}, P/E={q.get('pe_ratio')}"
            for t, q in quotes.items()
        )

        answer = self.llm.chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"User question: {state['user_message']}\n\nData:\n{summary_input}"},
            ],
            temperature=0.3,
        )

        return {"market_data": quotes, "draft_answer": answer}