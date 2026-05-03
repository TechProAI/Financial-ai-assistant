"""Custom exception hierarchy for the application."""


class FinnieException(Exception):
    """Base exception for all Finnie errors."""
    def __init__(self, message: str, code: str = "finnie_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class AgentExecutionError(FinnieException):
    """Raised when an agent fails to execute."""
    def __init__(self, agent: str, message: str):
        super().__init__(f"[{agent}] {message}", code="agent_error")
        self.agent = agent


class MarketDataError(FinnieException):
    """Raised when market data fetching fails."""
    def __init__(self, message: str):
        super().__init__(message, code="market_data_error")


class VectorStoreError(FinnieException):
    """Raised when vector store operations fail."""
    def __init__(self, message: str):
        super().__init__(message, code="vector_store_error")


class LLMServiceError(FinnieException):
    """Raised when the LLM service fails."""
    def __init__(self, message: str):
        super().__init__(message, code="llm_error")


class ComplianceViolationError(FinnieException):
    """Raised when a response violates compliance rules."""
    def __init__(self, message: str):
        super().__init__(message, code="compliance_violation")