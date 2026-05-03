"""Base agent class defining the common interface."""
import time
from abc import ABC, abstractmethod
from app.graph.state import GraphState
from app.models.schemas import AgentTrace
from app.core.logging import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all agents in the graph."""

    name: str = "base"

    @abstractmethod
    def run(self, state: GraphState) -> GraphState:
        """Subclasses implement the agent's core logic."""
        raise NotImplementedError

    def __call__(self, state: GraphState) -> GraphState:
        """Entrypoint wrapper that records timing and handles exceptions gracefully."""
        start = time.perf_counter()
        try:
            logger.info("agent_start", agent=self.name)
            updates = self.run(state)
        except Exception as e:
            logger.exception("agent_failed", agent=self.name, error=str(e))
            updates = {"error": f"[{self.name}] {e}"}
        duration_ms = (time.perf_counter() - start) * 1000
        trace = AgentTrace(agent=self.name, action="run", duration_ms=round(duration_ms, 2))
        # Because `agent_trace` uses add reducer, return a list of one
        updates["agent_trace"] = [trace]
        logger.info("agent_end", agent=self.name, duration_ms=round(duration_ms, 2))
        return updates