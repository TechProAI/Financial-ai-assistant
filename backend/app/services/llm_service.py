"""OpenAI LLM wrapper with retries and structured output support."""
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

try:
    from langsmith.wrappers import wrap_openai
except ImportError:
    wrap_openai = lambda x: x
from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import LLMServiceError

logger = get_logger(__name__)


class LLMService:
    """Thin wrapper around OpenAI chat completions with retries."""

    def __init__(self, model: Optional[str] = None):
        self.client = wrap_openai(OpenAI(api_key=settings.OPENAI_API_KEY))
        self.model = model or settings.OPENAI_MODEL

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type((APITimeoutError, RateLimitError, APIError)),
        reraise=True,
    )
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
    ) -> str:
        """Send a chat completion request and return the text response."""
        try:
            kwargs: Dict[str, Any] = {
                "model": model or self.model,
                "messages": messages,
                "temperature": temperature if temperature is not None else settings.OPENAI_TEMPERATURE,
            }
            if response_format:
                kwargs["response_format"] = response_format

            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content or ""
            logger.debug("llm_response", model=kwargs["model"], tokens=response.usage.total_tokens if response.usage else None)
            return content
        except Exception as e:
            logger.error("llm_request_failed", error=str(e))
            raise LLMServiceError(f"LLM request failed: {e}") from e

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        try:
            response = self.client.embeddings.create(
                model=settings.PINECONE_EMBEDDING_MODEL,
                input=texts,
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error("embedding_failed", error=str(e))
            raise LLMServiceError(f"Embedding failed: {e}") from e


_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Singleton accessor."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service