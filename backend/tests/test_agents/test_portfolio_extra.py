from app.agents.portfolio_analysis import PortfolioAnalysisAgent


def test_portfolio_agent_with_full_analysis(mock_llm):
    mock_llm.chat.return_value = "Your Sharpe ratio of 1.2 is solid."
    state = {
        "session_id": "s1",
        "user_message": "How is my portfolio?",
        "agent_trace": [],
        "portfolio_analysis": {
            "total_value": 50000,
            "total_return_pct": 15.0,
            "metrics": {
                "sharpe_ratio": 1.2,
                "annualized_volatility_pct": 18.5,
                "beta": 1.05,
                "max_drawdown_pct": -12.3,
            },
            "allocations": {"AAPL": 40, "MSFT": 35, "GOOGL": 25},
            "recommendations": ["Consider adding bonds"],
        },
    }
    agent = PortfolioAnalysisAgent()
    result = agent(state)
    assert "draft_answer" in result
    assert "Sharpe" in result["draft_answer"]