"""Pull financial education articles from Wikipedia API."""
import requests
from typing import List, Dict
from app.core.logging import get_logger

logger = get_logger(__name__)

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

# Curated list of Wikipedia articles covering finance fundamentals
FINANCE_TOPICS = [
    "Stock", "Bond_(finance)", "Mutual_fund", "Exchange-traded_fund",
    "Dividend", "Stock_market", "Market_capitalization", "Price–earnings_ratio",
    "Compound_interest", "Dollar_cost_averaging", "Diversification_(finance)",
    "Asset_allocation", "Portfolio_(finance)", "Modern_portfolio_theory",
    "Sharpe_ratio", "Beta_(finance)", "Volatility_(finance)", "Standard_deviation",
    "Risk_management_(financial)", "Rate_of_return",
    "Bull_market", "Bear_market", "Stock_exchange", "Index_fund",
    "Hedge_fund", "Inflation", "Interest_rate", "Yield_curve",
    "Capital_gain", "Short_(finance)", "Option_(finance)", "Futures_contract",
    "Fundamental_analysis", "Technical_analysis", "Efficient-market_hypothesis",
    "Value_investing", "Growth_investing",
    "National_Stock_Exchange_of_India", "BSE_Limited", "Nifty_50", "SENSEX",
    "Securities_and_Exchange_Board_of_India",
    "Systematic_investment_plan", "Demat_account",
    "Goods_and_Services_Tax_(India)", "Income_tax_in_India",
    "Real_estate_investment_trust", "Initial_public_offering",
    "Debt-to-equity_ratio", "Return_on_equity", "Earnings_per_share",
    "Moving_average", "Relative_strength_index",
    "Money_market", "Certificate_of_deposit", "Treasury_security",
    "Cryptocurrency", "Bitcoin", "Blockchain",
    "Financial_literacy", "Personal_finance", "Retirement_planning",
    "Rupee", "Foreign_exchange_market",
]


def fetch_wikipedia_articles(topics: List[str] = None) -> List[Dict[str, str]]:
    """Fetch article summaries from Wikipedia API."""
    topics = topics or FINANCE_TOPICS
    articles = []

    for topic in topics:
        try:
            # Use the summary REST API — simpler and more reliable
            clean_title = topic.replace("_", " ")
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
            resp = requests.get(url, headers={"User-Agent": "FinnieAI/1.0"}, timeout=10)

            if resp.status_code != 200:
                # Try with the original title format
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
                resp = requests.get(url, headers={"User-Agent": "FinnieAI/1.0"}, timeout=10)
                if resp.status_code != 200:
                    logger.warning("wiki_not_found", topic=topic)
                    continue

            data = resp.json()
            extract = data.get("extract", "")
            if len(extract) < 100:
                continue

            title = data.get("title", clean_title)

            # Now fetch the full article for more content
            full_url = f"https://en.wikipedia.org/api/rest_v1/page/mobile-html/{topic}"
            # Use the simpler text extract endpoint instead
            params = {
                "action": "query",
                "titles": clean_title,
                "prop": "extracts",
                "explaintext": True,
                "format": "json",
                "exlimit": 1,
            }
            full_resp = requests.get(
                WIKIPEDIA_API,
                params=params,
                headers={"User-Agent": "FinnieAI/1.0"},
                timeout=10,
            )

            full_text = extract  # fallback to summary
            if full_resp.status_code == 200:
                pages = full_resp.json().get("query", {}).get("pages", {})
                for page_id, page in pages.items():
                    if page_id != "-1" and page.get("extract"):
                        full_text = page["extract"][:3000]
                        break

            articles.append({
                "id": f"wiki_{topic.lower().replace(' ', '_').replace('(', '').replace(')', '')[:50]}",
                "title": title,
                "source": "wikipedia",
                "category": _categorize_topic(topic),
                "text": full_text.strip(),
            })
            logger.info("fetched_wiki_article", title=title, length=len(full_text))

        except Exception as e:
            logger.warning("wiki_fetch_failed", topic=topic, error=str(e))
            continue

    logger.info("wikipedia_fetch_complete", total=len(articles))
    return articles


def _categorize_topic(topic: str) -> str:
    """Simple keyword-based categorization."""
    t = topic.lower()
    if any(w in t for w in ["stock", "equity", "share", "ipo", "demat"]):
        return "stocks"
    if any(w in t for w in ["bond", "debt", "treasury", "certificate"]):
        return "bonds"
    if any(w in t for w in ["fund", "etf", "mutual", "index", "hedge", "sip"]):
        return "funds"
    if any(w in t for w in ["ratio", "beta", "sharpe", "volatility", "deviation", "return"]):
        return "metrics"
    if any(w in t for w in ["india", "nse", "bse", "nifty", "sensex", "sebi", "rupee", "gst"]):
        return "india_market"
    if any(w in t for w in ["crypto", "bitcoin", "blockchain"]):
        return "crypto"
    if any(w in t for w in ["tax", "income", "capital_gain"]):
        return "tax"
    if any(w in t for w in ["analysis", "technical", "fundamental", "moving", "rsi"]):
        return "analysis"
    if any(w in t for w in ["retire", "personal", "literacy", "planning"]):
        return "personal_finance"
    return "general"