from app.core.exceptions import (
    FinnieException, AgentExecutionError, MarketDataError,
    VectorStoreError, LLMServiceError, ComplianceViolationError,
)


def test_finnie_exception():
    e = FinnieException("base error")
    assert e.code == "finnie_error"
    assert str(e) == "base error"


def test_agent_execution_error():
    e = AgentExecutionError("supervisor", "failed to classify")
    assert e.agent == "supervisor"
    assert "supervisor" in e.message


def test_market_data_error():
    e = MarketDataError("no quote")
    assert e.code == "market_data_error"


def test_vector_store_error():
    e = VectorStoreError("upsert failed")
    assert e.code == "vector_store_error"


def test_llm_service_error():
    e = LLMServiceError("timeout")
    assert e.code == "llm_error"


def test_compliance_violation_error():
    e = ComplianceViolationError("risky language")
    assert e.code == "compliance_violation"