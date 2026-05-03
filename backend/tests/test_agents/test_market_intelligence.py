from app.agents.market_intelligence import MarketIntelligenceAgent


def test_market_agent_with_tickers(mock_llm, mock_market, base_state):
    mock_llm.chat.return_value = "AAPL is trading at $190.50."
    base_state["tickers"] = ["AAPL"]
    agent = MarketIntelligenceAgent()
    result = agent(base_state)
    assert "AAPL" in result["market_data"]
    assert result["draft_answer"]


def test_market_agent_without_tickers(mock_llm, mock_market, base_state):
    base_state["tickers"] = []
    agent = MarketIntelligenceAgent()
    result = agent(base_state)
    assert "ticker" in result["draft_answer"].lower()