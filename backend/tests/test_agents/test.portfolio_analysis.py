from app.agents.portfolio_analysis import PortfolioAnalysisAgent


def test_portfolio_agent_without_data(mock_llm, base_state):
    agent = PortfolioAnalysisAgent()
    result = agent(base_state)
    assert "Portfolio tab" in result["draft_answer"]


def test_portfolio_agent_with_data(mock_llm, base_state):
    mock_llm.chat.return_value = "Your portfolio looks diversified."
    base_state["portfolio_analysis"] = {
        "total_value": 10000, "total_return_pct": 12.0,
        "metrics": {"sharpe_ratio": 1.2}, "allocations": {"AAPL": 50},
        "recommendations": ["Rebalance"],
    }
    agent = PortfolioAnalysisAgent()
    result = agent(base_state)
    assert "draft_answer" in result