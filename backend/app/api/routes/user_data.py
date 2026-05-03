"""Endpoints for user-specific data: chat sessions, holdings, watchlist."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.auth import get_current_user, get_supabase
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/user", tags=["user"])


# ── Schemas ──

class SessionOut(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    citations: list = []
    agent_trace: list = []
    disclaimers: list = []
    extra_data: dict = {}
    created_at: str


class SaveMessageRequest(BaseModel):
    session_id: str
    role: str
    content: str
    citations: list = []
    agent_trace: list = []
    disclaimers: list = []
    extra_data: dict = {}


class HoldingIn(BaseModel):
    ticker: str
    quantity: float
    avg_cost: float


class WatchlistIn(BaseModel):
    ticker: str


# ── Chat Sessions ──

@router.get("/sessions", response_model=List[SessionOut])
def list_sessions(user: dict = Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("chat_sessions") \
        .select("*") \
        .eq("user_id", user["id"]) \
        .order("updated_at", desc=True) \
        .execute()
    return result.data


@router.post("/sessions")
def create_session(user: dict = Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("chat_sessions") \
        .insert({"user_id": user["id"], "title": "New Chat"}) \
        .execute()
    return result.data[0]


@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, user: dict = Depends(get_current_user)):
    sb = get_supabase()
    sb.table("chat_sessions") \
        .delete() \
        .eq("id", session_id) \
        .eq("user_id", user["id"]) \
        .execute()
    return {"deleted": True}


# ── Chat Messages ──

@router.get("/sessions/{session_id}/messages", response_model=List[MessageOut])
def get_messages(session_id: str, user: dict = Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("chat_messages") \
        .select("*") \
        .eq("session_id", session_id) \
        .eq("user_id", user["id"]) \
        .order("created_at") \
        .execute()
    return result.data


@router.post("/messages")
def save_message(req: SaveMessageRequest, user: dict = Depends(get_current_user)):
    sb = get_supabase()

    # Update session title from first user message
    if req.role == "user":
        sb.table("chat_sessions") \
            .update({"title": req.content[:50], "updated_at": "now()"}) \
            .eq("id", req.session_id) \
            .eq("user_id", user["id"]) \
            .execute()

    result = sb.table("chat_messages") \
        .insert({
            "session_id": req.session_id,
            "user_id": user["id"],
            "role": req.role,
            "content": req.content,
            "citations": req.citations,
            "agent_trace": req.agent_trace,
            "disclaimers": req.disclaimers,
            "extra_data": req.extra_data,
        }) \
        .execute()
    return result.data[0]


# ── Holdings ──

@router.get("/holdings")
def get_holdings(user: dict = Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("holdings") \
        .select("*") \
        .eq("user_id", user["id"]) \
        .execute()
    return result.data


@router.post("/holdings")
def upsert_holding(req: HoldingIn, user: dict = Depends(get_current_user)):
    sb = get_supabase()
    # Check if ticker exists
    existing = sb.table("holdings") \
        .select("*") \
        .eq("user_id", user["id"]) \
        .eq("ticker", req.ticker.upper()) \
        .execute()

    if existing.data:
        # Update quantity
        new_qty = existing.data[0]["quantity"] + req.quantity
        result = sb.table("holdings") \
            .update({"quantity": new_qty, "avg_cost": req.avg_cost}) \
            .eq("id", existing.data[0]["id"]) \
            .execute()
    else:
        result = sb.table("holdings") \
            .insert({
                "user_id": user["id"],
                "ticker": req.ticker.upper(),
                "quantity": req.quantity,
                "avg_cost": req.avg_cost,
            }) \
            .execute()
    return result.data[0]


@router.delete("/holdings/{ticker}")
def delete_holding(ticker: str, user: dict = Depends(get_current_user)):
    sb = get_supabase()
    sb.table("holdings") \
        .delete() \
        .eq("user_id", user["id"]) \
        .eq("ticker", ticker.upper()) \
        .execute()
    return {"deleted": True}


# ── Watchlist ──

@router.get("/watchlist")
def get_watchlist(user: dict = Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("watchlist") \
        .select("*") \
        .eq("user_id", user["id"]) \
        .order("created_at") \
        .execute()
    return result.data


@router.post("/watchlist")
def add_to_watchlist(req: WatchlistIn, user: dict = Depends(get_current_user)):
    sb = get_supabase()
    try:
        result = sb.table("watchlist") \
            .insert({"user_id": user["id"], "ticker": req.ticker.upper()}) \
            .execute()
        return result.data[0]
    except Exception:
        # Already exists — ignore
        return {"ticker": req.ticker.upper(), "exists": True}


@router.delete("/watchlist/{ticker}")
def remove_from_watchlist(ticker: str, user: dict = Depends(get_current_user)):
    sb = get_supabase()
    sb.table("watchlist") \
        .delete() \
        .eq("user_id", user["id"]) \
        .eq("ticker", ticker.upper()) \
        .execute()
    return {"deleted": True}