"""Compliance agent: final filter that adds disclaimers and removes risky language."""
import re
from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.graph.state import GraphState

# Phrases that suggest personalized investment advice — softened automatically
RISKY_PATTERNS = [
    (re.compile(r"\byou should buy\b", re.I), "you might consider researching"),
    (re.compile(r"\byou should sell\b", re.I), "you might review"),
    (re.compile(r"\bguaranteed returns?\b", re.I), "potential returns (no guarantees)"),
    (re.compile(r"\bwill definitely\b", re.I), "could"),
    (re.compile(r"\bbest stock to buy\b", re.I), "stock to research"),
]

STANDARD_DISCLAIMER = (
    "This response is for educational purposes only and is not personalized investment advice. "
    "Consult a licensed financial advisor before making investment decisions."
)


class ComplianceAgent(BaseAgent):
    name = "compliance"

    def run(self, state: GraphState) -> Dict[str, Any]:
        draft = state.get("draft_answer") or "I'm not sure how to answer that. Could you rephrase?"

        # Soften risky language
        sanitized = draft
        for pattern, replacement in RISKY_PATTERNS:
            sanitized = pattern.sub(replacement, sanitized)

        disclaimers: List[str] = [STANDARD_DISCLAIMER]
        intent = state.get("intent", "general")
        if intent in ("market", "portfolio"):
            disclaimers.append("Market data may be delayed and should not be the sole basis for decisions.")

        return {
            "final_answer": sanitized,
            "disclaimers": disclaimers,
        }