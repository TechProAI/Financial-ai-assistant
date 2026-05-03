from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_chat_endpoint():
    with patch("app.api.routes.chat.workflow_dep") as mock_dep:
        fake_wf = MagicMock()
        fake_wf.invoke.return_value = {
            "final_answer": "Stocks are ownership.",
            "citations": [],
            "agent_trace": [],
            "disclaimers": ["Educational only."],
            "intent": "education",
            "tickers": [],
            "market_data": {},
            "news_items": [],
        }
        mock_dep.return_value = fake_wf
        app.dependency_overrides = {}
        from app.api.dependencies import workflow_dep
        app.dependency_overrides[workflow_dep] = lambda: fake_wf

        r = client.post("/chat", json={"session_id": "s1", "message": "What is a stock?"})
        assert r.status_code == 200
        body = r.json()
        assert body["answer"] == "Stocks are ownership."
        assert body["disclaimers"]
        app.dependency_overrides = {}