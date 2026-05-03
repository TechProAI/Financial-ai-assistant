"""Education agent: answers financial concept questions using RAG."""
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.services.rag_service import get_rag_service
from app.services.llm_service import get_llm_service

SYSTEM_PROMPT = """You are Finnie, a friendly financial educator for beginners.
Explain concepts in simple, jargon-free language. Use short paragraphs and concrete examples.
You MUST ground your answer in the provided context snippets. Cite them inline using [1], [2], etc.
If the context does not contain the answer, say so honestly and suggest what the user could research.
Never give personalized investment advice — stick to education.
"""


class EducationAgent(BaseAgent):
    name = "education"

    def __init__(self):
        self.rag = get_rag_service()
        self.llm = get_llm_service()

    def run(self, state: GraphState) -> Dict[str, Any]:
        query = state["user_message"]
        chunks = self.rag.retrieve(query, top_k=5)
        context, citations = self.rag.format_context(chunks)

        user_prompt = (
            f"Context:\n{context or '(no relevant context found)'}\n\n"
            f"User question: {query}\n\n"
            f"Answer clearly and cite the context snippets where applicable."
        )

        answer = self.llm.chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        return {
            "rag_context": context,
            "citations": citations,
            "draft_answer": answer,
        }