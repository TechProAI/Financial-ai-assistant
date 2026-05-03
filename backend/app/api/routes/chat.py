"""Chat endpoint — main entry into the LangGraph workflow."""
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Citation, AgentTrace
from app.api.dependencies import workflow_dep
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, workflow=Depends(workflow_dep)) -> ChatResponse:
    initial_state = {
        "session_id": req.session_id,
        "user_message": req.message,
        "chat_history": [m.model_dump() for m in req.history],
        "user_profile": req.user_profile,
        "agent_trace": [],
    }

    try:
        result = workflow.invoke(
            initial_state,
            config={
                "run_name": f"finnie_chat_{req.session_id[:8]}",
                "metadata": {
                    "session_id": req.session_id,
                    "user_message": req.message[:100],
                },
                "tags": ["chat", "production"],
            },
        )
    except Exception as e:
        logger.exception("workflow_error")
        raise HTTPException(status_code=500, detail=f"Workflow error: {e}")

    return ChatResponse(
        session_id=req.session_id,
        answer=result.get("final_answer", "I couldn't generate a response. Please try again."),
        citations=result.get("citations", []),
        agent_trace=result.get("agent_trace", []),
        disclaimers=result.get("disclaimers", []),
        data={
            "intent": result.get("intent"),
            "tickers": result.get("tickers", []),
            "market_data": result.get("market_data", {}),
            "news_items": result.get("news_items", []),
        },
    )