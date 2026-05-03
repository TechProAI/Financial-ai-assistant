from unittest.mock import patch, MagicMock
import pytest
from app.services.llm_service import LLMService
from app.core.exceptions import LLMServiceError


def test_llm_chat_success():
    with patch("app.services.llm_service.OpenAI") as mock_openai:
        client = MagicMock()
        response = MagicMock()
        response.choices = [MagicMock(message=MagicMock(content="hello"))]
        response.usage = MagicMock(total_tokens=10)
        client.chat.completions.create.return_value = response
        mock_openai.return_value = client

        svc = LLMService()
        result = svc.chat([{"role": "user", "content": "hi"}])
        assert result == "hello"


def test_llm_chat_with_response_format():
    with patch("app.services.llm_service.OpenAI") as mock_openai:
        client = MagicMock()
        response = MagicMock()
        response.choices = [MagicMock(message=MagicMock(content='{"k":"v"}'))]
        response.usage = MagicMock(total_tokens=5)
        client.chat.completions.create.return_value = response
        mock_openai.return_value = client

        svc = LLMService()
        result = svc.chat(
            [{"role": "user", "content": "hi"}],
            response_format={"type": "json_object"},
            temperature=0.0,
            model="gpt-4o-mini",
        )
        assert result == '{"k":"v"}'


def test_llm_chat_raises_on_failure():
    with patch("app.services.llm_service.OpenAI") as mock_openai:
        client = MagicMock()
        client.chat.completions.create.side_effect = ValueError("boom")
        mock_openai.return_value = client

        svc = LLMService()
        with pytest.raises(LLMServiceError):
            svc.chat([{"role": "user", "content": "hi"}])


def test_llm_embed_success():
    with patch("app.services.llm_service.OpenAI") as mock_openai:
        client = MagicMock()
        response = MagicMock()
        response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        client.embeddings.create.return_value = response
        mock_openai.return_value = client

        svc = LLMService()
        result = svc.embed(["text"])
        assert result == [[0.1, 0.2, 0.3]]


def test_llm_embed_raises_on_failure():
    with patch("app.services.llm_service.OpenAI") as mock_openai:
        client = MagicMock()
        client.embeddings.create.side_effect = RuntimeError("fail")
        mock_openai.return_value = client

        svc = LLMService()
        with pytest.raises(LLMServiceError):
            svc.embed(["text"])


def test_llm_singleton():
    from app.services import llm_service
    llm_service._llm_service = None
    with patch("app.services.llm_service.OpenAI"):
        a = llm_service.get_llm_service()
        b = llm_service.get_llm_service()
        assert a is b