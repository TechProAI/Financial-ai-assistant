"""LangGraph StateGraph wiring all 6 agents together."""
from typing import Dict
from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.agents.supervisor import SupervisorAgent
from app.agents.education import EducationAgent
from app.agents.market_intelligence import MarketIntelligenceAgent
from app.agents.portfolio_analysis import PortfolioAnalysisAgent
from app.agents.news_sentiment import NewsSentimentAgent
from app.agents.compliance import ComplianceAgent
from app.core.logging import get_logger

logger = get_logger(__name__)


def _route_after_supervisor(state: GraphState) -> str:
    """Conditional edge: choose the domain agent based on classified intent."""
    intent = state.get("intent", "general")
    mapping = {
        "education": "education",
        "market": "market_intelligence",
        "portfolio": "portfolio_analysis",
        "news": "news_sentiment",
        "general": "education",  # default fallback — RAG can handle general questions
    }
    return mapping.get(intent, "education")


def build_workflow():
    """Construct and compile the LangGraph multi-agent workflow."""
    graph = StateGraph(GraphState)

    supervisor = SupervisorAgent()
    education = EducationAgent()
    market = MarketIntelligenceAgent()
    portfolio = PortfolioAnalysisAgent()
    news = NewsSentimentAgent()
    compliance = ComplianceAgent()

    graph.add_node("supervisor_agent", supervisor)
    graph.add_node("education_agent", education)
    graph.add_node("market_agent", market)
    graph.add_node("portfolio_agent", portfolio)
    graph.add_node("news_agent", news)
    graph.add_node("compliance_agent", compliance)

    graph.set_entry_point("supervisor_agent")

    graph.add_conditional_edges(
        "supervisor_agent",
        _route_after_supervisor,
        {
            "education": "education_agent",
            "market_intelligence": "market_agent",
            "portfolio_analysis": "portfolio_agent",
            "news_sentiment": "news_agent",
        },
    )

    for node in ("education_agent", "market_agent", "portfolio_agent", "news_agent"):
        graph.add_edge(node, "compliance_agent")

    graph.add_edge("compliance_agent", END)

    compiled = graph.compile()
    logger.info("workflow_compiled", nodes=6)
    return compiled


_workflow = None


def get_workflow():
    global _workflow
    if _workflow is None:
        _workflow = build_workflow()
    return _workflow