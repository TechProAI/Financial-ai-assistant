"""Supervisor agent: classifies intent, extracts tickers, decides routing."""
import json
import re
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.llm_service import get_llm_service
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """You are the supervisor of a multi-agent financial assistant named Finnie.

Classify the user's message into ONE of these intents:
- education: general financial concepts, definitions, "how does X work", learning topics
- market: asking about a stock price, quote, company fundamentals, historical performance
- portfolio: portfolio analysis, allocation, diversification, risk metrics (user mentions holdings/positions)
- news: recent news, sentiment, what's happening with X
- general: greetings, small talk, clarifying questions, off-topic

Also extract any stock tickers mentioned. Rules for ticker extraction:
1. If the user mentions a US company by name, infer the ticker (e.g., "Apple" → "AAPL", "Microsoft" → "MSFT", "Tesla" → "TSLA")
2. If the user mentions an Indian company by name, infer the NSE ticker with .NS suffix:
   - "Reliance" → "RELIANCE.NS"
   - "TCS" or "Tata Consultancy" → "TCS.NS"
   - "Infosys" → "INFY.NS"
   - "HDFC Bank" → "HDFCBANK.NS"
   - "ICICI Bank" → "ICICIBANK.NS"
   - "Wipro" → "WIPRO.NS"
   - "Tata Motors" → "TATAMOTORS.NS"
   - "Bharti Airtel" or "Airtel" → "BHARTIARTL.NS"
   - "ITC" → "ITC.NS"
   - "Adani" → "ADANIENT.NS"
   - "Zomato" → "ZOMATO.NS"
   - "Bajaj Finance" → "BAJFINANCE.NS"
   - "SBI" or "State Bank" → "SBIN.NS"
   - "Kotak" → "KOTAKBANK.NS"
   - "HUL" or "Hindustan Unilever" → "HINDUNILVR.NS"
   - "Maruti" → "MARUTI.NS"
   - "Asian Paints" → "ASIANPAINT.NS"
   - "Sun Pharma" → "SUNPHARMA.NS"
   - "L&T" or "Larsen" → "LT.NS"
   - For any other Indian company, use the company name in uppercase with .NS suffix
3. If the user already provides a ticker with .NS or .BO suffix, use it as-is
4. If unsure whether a company is Indian or US, default to US ticker format

Respond ONLY with valid JSON in this exact format:
{"intent": "education|market|portfolio|news|general", "tickers": ["RELIANCE.NS"], "needs_rag": true, "needs_market_data": false}
"""


class SupervisorAgent(BaseAgent):
    name = "supervisor"

    def __init__(self):
        self.llm = get_llm_service()

    def run(self, state: GraphState) -> Dict[str, Any]:
        message = state["user_message"]

        raw = self.llm.chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
            model=settings.OPENAI_SUPERVISOR_MODEL,
        )

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("supervisor_parse_failed", raw=raw)
            parsed = {"intent": "general", "tickers": [], "needs_rag": False, "needs_market_data": False}

        intent = parsed.get("intent", "general")
        tickers = [
            t.upper()
            for t in parsed.get("tickers", [])
            if re.match(r"^[A-Z]{1,20}(\.(NS|BO))?$", t.upper())
        ]

        return {
            "intent": intent,
            "tickers": tickers,
            "needs_rag": bool(parsed.get("needs_rag", intent == "education")),
            "needs_market_data": bool(parsed.get("needs_market_data", intent in ("market", "portfolio", "news"))),
        }