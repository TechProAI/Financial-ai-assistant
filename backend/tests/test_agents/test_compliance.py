from app.agents.compliance import ComplianceAgent


def test_compliance_adds_disclaimer(base_state):
    base_state["draft_answer"] = "Stocks are pieces of ownership."
    base_state["intent"] = "education"
    agent = ComplianceAgent()
    result = agent(base_state)
    assert len(result["disclaimers"]) >= 1
    assert "educational purposes" in result["disclaimers"][0].lower()


def test_compliance_softens_risky_language(base_state):
    base_state["draft_answer"] = "You should buy AAPL, it's guaranteed returns."
    base_state["intent"] = "market"
    agent = ComplianceAgent()
    result = agent(base_state)
    assert "you should buy" not in result["final_answer"].lower()
    assert "guaranteed returns" not in result["final_answer"].lower()
    assert len(result["disclaimers"]) >= 2