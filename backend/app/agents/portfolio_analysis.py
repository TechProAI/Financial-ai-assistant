"""Portfolio Analysis agent: calculates risk/return metrics for user holdings."""
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.llm_service import get_llm_service

SYSTEM_PROMPT = """You are a portfolio analyst. Explain portfolio metrics in simple terms for a beginner.
Interpret Sharpe ratio, volatility, beta, and drawdown. Be encouraging but honest about risks.
Never guarantee future performance."""


class PortfolioAnalysisAgent(BaseAgent):
    """This agent is typically invoked via the dedicated /portfolio endpoint, but it can
    also narrate pre-computed portfolio results inside the chat graph."""

    name = "portfolio_analysis"

    def __init__(self):
        self.llm = get_llm_service()

    def run(self, state: GraphState) -> Dict[str, Any]:
        analysis = state.get("portfolio_analysis") or {}
        if not analysis:
            return {
                "draft_answer": "To analyze a portfolio, please use the Portfolio tab to provide your "
                                "holdings (ticker, quantity, and average cost).",
            }

        prompt = (
            f"User question: {state['user_message']}\n\n"
            f"Portfolio analysis:\n"
            f"Total value: ${analysis.get('total_value')}\n"
            f"Total return: {analysis.get('total_return_pct')}%\n"
            f"Metrics: {analysis.get('metrics')}\n"
            f"Allocations: {analysis.get('allocations')}\n"
            f"Recommendations: {analysis.get('recommendations')}\n"
        )
        answer = self.llm.chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return {"draft_answer": answer}