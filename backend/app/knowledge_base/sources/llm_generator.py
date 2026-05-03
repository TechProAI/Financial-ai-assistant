"""Generate high-quality financial education articles using OpenAI.

This is a production-grade approach: instead of hardcoding content,
we use an LLM to generate structured, consistent articles on a
curated syllabus. Each article is original content optimized for RAG retrieval.
"""
from typing import List, Dict
from app.services.llm_service import get_llm_service
from app.core.logging import get_logger

logger = get_logger(__name__)

# Comprehensive syllabus covering beginner to advanced topics
SYLLABUS = [
    # === BASICS ===
    ("basics", "What is a Stock and How Does Ownership Work"),
    ("basics", "Understanding Bonds and Fixed Income Investments"),
    ("basics", "What are Dividends and How Do They Work"),
    ("basics", "How Stock Exchanges Work: NSE, BSE, NYSE"),
    ("basics", "Understanding Market Capitalization: Large Cap, Mid Cap, Small Cap"),
    ("basics", "What is a Demat Account and How to Open One in India"),
    ("basics", "Understanding Trading Hours and Market Sessions"),
    ("basics", "What is Face Value, Book Value, and Market Value"),
    ("basics", "Understanding Bid Price, Ask Price, and Spread"),
    ("basics", "What are Blue Chip Stocks"),

    # === INVESTMENT VEHICLES ===
    ("investment_vehicles", "Mutual Funds Explained: Types and How They Work"),
    ("investment_vehicles", "Exchange Traded Funds: How ETFs Differ from Mutual Funds"),
    ("investment_vehicles", "Index Funds: Why Warren Buffett Recommends Them"),
    ("investment_vehicles", "Systematic Investment Plans: Power of SIP in India"),
    ("investment_vehicles", "Real Estate Investment Trusts: Investing in Property Without Buying"),
    ("investment_vehicles", "Gold ETFs and Sovereign Gold Bonds in India"),
    ("investment_vehicles", "Fixed Deposits vs Debt Mutual Funds"),
    ("investment_vehicles", "Government Securities and Treasury Bills"),
    ("investment_vehicles", "Corporate Bonds and Debentures"),
    ("investment_vehicles", "ELSS Funds: Tax Saving Mutual Funds Under Section 80C"),

    # === RISK AND PORTFOLIO ===
    ("risk_management", "Understanding Risk Tolerance and Risk Appetite"),
    ("risk_management", "Diversification: The Only Free Lunch in Investing"),
    ("risk_management", "Asset Allocation Strategies for Different Age Groups"),
    ("risk_management", "Portfolio Rebalancing: When and How to Do It"),
    ("risk_management", "Understanding Correlation Between Assets"),
    ("risk_management", "Hedging Strategies for Retail Investors"),
    ("risk_management", "Sector Diversification and Why It Matters"),
    ("risk_management", "International Diversification for Indian Investors"),
    ("risk_management", "Understanding Maximum Drawdown"),
    ("risk_management", "Concentration Risk: When One Stock Dominates Your Portfolio"),

    # === METRICS AND ANALYSIS ===
    ("metrics", "Sharpe Ratio: Measuring Risk-Adjusted Returns"),
    ("metrics", "Understanding Beta and Market Sensitivity"),
    ("metrics", "Volatility and Standard Deviation in Simple Terms"),
    ("metrics", "Price to Earnings Ratio: Valuation Made Simple"),
    ("metrics", "Price to Book Ratio and When to Use It"),
    ("metrics", "Debt to Equity Ratio: Measuring Company Leverage"),
    ("metrics", "Return on Equity: Measuring Company Profitability"),
    ("metrics", "Earnings Per Share and Its Importance"),
    ("metrics", "Dividend Yield: Income from Your Investments"),
    ("metrics", "PEG Ratio: Growth at a Reasonable Price"),

    # === STRATEGIES ===
    ("strategy", "Dollar Cost Averaging and Rupee Cost Averaging"),
    ("strategy", "Value Investing: Finding Undervalued Stocks"),
    ("strategy", "Growth Investing: Betting on Future Earnings"),
    ("strategy", "Momentum Investing: Following Market Trends"),
    ("strategy", "Buy and Hold: The Power of Long Term Investing"),
    ("strategy", "Contrarian Investing: Going Against the Crowd"),
    ("strategy", "Dividend Growth Investing Strategy"),
    ("strategy", "Core and Satellite Portfolio Strategy"),
    ("strategy", "Lump Sum vs SIP: Which is Better"),
    ("strategy", "The Three Fund Portfolio for Beginners"),

    # === INDIAN MARKET SPECIFIC ===
    ("india_market", "Understanding NIFTY 50 and SENSEX"),
    ("india_market", "How SEBI Protects Indian Investors"),
    ("india_market", "IPO Process in India: From Filing to Listing"),
    ("india_market", "Understanding F&O Trading on NSE"),
    ("india_market", "Circuit Breakers and Price Bands in Indian Markets"),
    ("india_market", "Mutual Fund Categories as Defined by SEBI"),
    ("india_market", "Understanding NAV in Mutual Funds"),
    ("india_market", "Direct vs Regular Mutual Fund Plans"),
    ("india_market", "What is T+1 Settlement in Indian Markets"),
    ("india_market", "Role of RBI in Indian Financial Markets"),

    # === TAX ===
    ("tax", "Capital Gains Tax in India: Short Term vs Long Term"),
    ("tax", "Section 80C: Tax Saving Investment Options in India"),
    ("tax", "Understanding TDS on Dividends and Interest Income"),
    ("tax", "Tax Harvesting: Legally Reducing Your Tax Liability"),
    ("tax", "HUF and Tax Planning for Indian Families"),
    ("tax", "NRI Investment and Taxation in India"),

    # === BEHAVIORAL FINANCE ===
    ("behavior", "Common Investing Mistakes Beginners Make"),
    ("behavior", "Loss Aversion: Why Losses Hurt More Than Gains"),
    ("behavior", "Herd Mentality in Stock Markets"),
    ("behavior", "Anchoring Bias in Investment Decisions"),
    ("behavior", "Recency Bias and How It Affects Your Portfolio"),
    ("behavior", "FOMO in Investing: Fear of Missing Out"),
    ("behavior", "Overconfidence Bias in Trading"),
    ("behavior", "Sunk Cost Fallacy in Investments"),

    # === TECHNICAL ANALYSIS ===
    ("technical_analysis", "Introduction to Technical Analysis and Charts"),
    ("technical_analysis", "Moving Averages: SMA and EMA Explained"),
    ("technical_analysis", "RSI: Relative Strength Index for Beginners"),
    ("technical_analysis", "Support and Resistance Levels"),
    ("technical_analysis", "Candlestick Patterns Every Investor Should Know"),
    ("technical_analysis", "Volume Analysis in Stock Trading"),

    # === ADVANCED ===
    ("advanced", "Options Trading Basics: Calls and Puts"),
    ("advanced", "Futures Contracts and How They Work"),
    ("advanced", "Understanding Short Selling"),
    ("advanced", "What are Derivatives and Why They Exist"),
    ("advanced", "Margin Trading: Risks and Rewards"),
    ("advanced", "Algorithmic Trading: An Overview"),
    ("advanced", "Understanding Yield Curves and Their Signals"),
    ("advanced", "Efficient Market Hypothesis Explained"),
    ("advanced", "Modern Portfolio Theory Simplified"),
    ("advanced", "Factor Investing: Size, Value, Momentum"),

    # === PERSONAL FINANCE ===
    ("personal_finance", "Building an Emergency Fund Before Investing"),
    ("personal_finance", "How to Start Investing with Small Amounts"),
    ("personal_finance", "Retirement Planning in India: NPS, EPF, PPF"),
    ("personal_finance", "Health Insurance and Term Insurance Basics"),
    ("personal_finance", "Setting Financial Goals: Short, Medium, Long Term"),
    ("personal_finance", "Power of Compound Interest Over Decades"),
    ("personal_finance", "Inflation and Its Impact on Your Savings"),
    ("personal_finance", "Budgeting Basics: 50-30-20 Rule"),
    ("personal_finance", "Debt Management: Good Debt vs Bad Debt"),
    ("personal_finance", "Estate Planning and Will Creation Basics"),

    # === CRYPTO ===
    ("crypto", "Cryptocurrency Basics: Bitcoin and Beyond"),
    ("crypto", "Blockchain Technology Simplified"),
    ("crypto", "Crypto Regulation in India"),
    ("crypto", "DeFi: Decentralized Finance Explained"),
    ("crypto", "Risks of Cryptocurrency Investment"),
]

GENERATION_PROMPT = """You are a financial education content writer creating articles for Finnie,
an AI-powered financial literacy platform targeting Indian investors (beginners to intermediate).

Write a comprehensive educational article on the topic: "{topic}"

Requirements:
- Write 400-600 words
- Use simple, jargon-free language. When you must use a technical term, define it immediately
- Include practical Indian examples where relevant (use INR, mention Indian markets, SEBI, etc.)
- Include at least one concrete numerical example
- Structure: brief intro → explanation → example → key takeaway
- Be factual and balanced — never give buy/sell advice
- Write in a friendly, encouraging tone suitable for someone new to investing

Write ONLY the article content, no title or metadata."""


def generate_articles(
    syllabus: List[tuple] = None,
    batch_size: int = 5,
) -> List[Dict[str, str]]:
    """Generate educational articles using OpenAI for each syllabus topic."""
    syllabus = syllabus or SYLLABUS
    llm = get_llm_service()
    articles = []

    for i, (category, topic) in enumerate(syllabus):
        try:
            logger.info("generating_article", index=i + 1, total=len(syllabus), topic=topic)

            text = llm.chat(
                messages=[
                    {"role": "system", "content": GENERATION_PROMPT.replace("{topic}", topic)},
                    {"role": "user", "content": f"Write the article about: {topic}"},
                ],
                temperature=0.4,
            )

            if len(text.strip()) < 100:
                logger.warning("article_too_short", topic=topic)
                continue

            article_id = f"gen_{i:03d}_{topic.lower().replace(' ', '_').replace(':', '')[:40]}"
            articles.append({
                "id": article_id,
                "title": topic,
                "source": "finnie_generated",
                "category": category,
                "text": text.strip(),
            })
            logger.info("article_generated", topic=topic, length=len(text))

        except Exception as e:
            logger.error("article_generation_failed", topic=topic, error=str(e))
            continue

    logger.info("generation_complete", total=len(articles))
    return articles