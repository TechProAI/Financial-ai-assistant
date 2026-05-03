from app.agents.education import EducationAgent


def test_education_uses_rag(mock_llm, mock_vector_store, base_state):
    mock_llm.chat.return_value = "Stocks are ownership in a company [1]."
    agent = EducationAgent()
    result = agent(base_state)
    assert "draft_answer" in result
    assert len(result["citations"]) > 0