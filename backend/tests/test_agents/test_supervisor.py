import json
from app.agents.supervisor import SupervisorAgent


def test_supervisor_classifies_education(mock_llm, base_state):
    mock_llm.chat.return_value = json.dumps(
        {"intent": "education", "tickers": [], "needs_rag": True, "needs_market_data": False}
    )
    agent = SupervisorAgent()
    result = agent(base_state)
    assert result["intent"] == "education"
    assert result["needs_rag"] is True


def test_supervisor_extracts_tickers(mock_llm, base_state):
    mock_llm.chat.return_value = json.dumps(
        {"intent": "market", "tickers": ["AAPL", "MSFT"], "needs_rag": False, "needs_market_data": True}
    )
    base_state["user_message"] = "How is Apple and Microsoft doing?"
    agent = SupervisorAgent()
    result = agent(base_state)
    assert "AAPL" in result["tickers"]
    assert "MSFT" in result["tickers"]


def test_supervisor_handles_invalid_json(mock_llm, base_state):
    mock_llm.chat.return_value = "not-json"
    agent = SupervisorAgent()
    result = agent(base_state)
    assert result["intent"] == "general"