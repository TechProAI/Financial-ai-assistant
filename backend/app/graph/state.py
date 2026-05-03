"""LangGraph state definition for the multi-agent workflow."""
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from operator import add
from app.models.schemas import Citation, AgentTrace, UserProfile


class GraphState(TypedDict, total=False):
    """Shared state passed between all agents in the LangGraph workflow."""

    # Input
    session_id: str
    user_message: str
    chat_history: List[Dict[str, str]]
    user_profile: Optional[UserProfile]

    # Routing
    intent: str                     # education | market | portfolio | news | general
    tickers: List[str]              # extracted tickers from user message
    needs_rag: bool
    needs_market_data: bool

    # Agent outputs (each agent may contribute)
    rag_context: str
    citations: List[Citation]
    market_data: Dict[str, Any]
    portfolio_analysis: Dict[str, Any]
    news_items: List[Dict[str, Any]]

    # Final output
    draft_answer: str
    final_answer: str
    disclaimers: List[str]

    # Telemetry — uses `add` reducer so each agent can append without clobbering
    agent_trace: Annotated[List[AgentTrace], add]

    # Control
    error: Optional[str]