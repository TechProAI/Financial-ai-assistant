"""API request and response schemas."""
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[datetime] = None


class UserProfile(BaseModel):
    """User financial profile used for personalization."""
    risk_appetite: Literal["conservative", "moderate", "aggressive"] = "moderate"
    experience_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    goals: List[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=128)
    message: str = Field(..., min_length=1, max_length=4000)
    history: List[ChatMessage] = Field(default_factory=list)
    user_profile: Optional[UserProfile] = None


class Citation(BaseModel):
    source: str
    title: str
    snippet: str
    score: float


class AgentTrace(BaseModel):
    agent: str
    action: str
    duration_ms: float


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    agent_trace: List[AgentTrace] = Field(default_factory=list)
    disclaimers: List[str] = Field(default_factory=list)
    data: Dict[str, Any] = Field(default_factory=dict)


class PortfolioHolding(BaseModel):
    ticker: str
    quantity: float = Field(..., gt=0)
    avg_cost: float = Field(..., ge=0)


class PortfolioAnalyzeRequest(BaseModel):
    holdings: List[PortfolioHolding]
    benchmark: str = "SPY"


class PortfolioAnalyzeResponse(BaseModel):
    total_value: float
    total_cost: float
    total_return_pct: float
    allocations: Dict[str, float]
    metrics: Dict[str, float]
    recommendations: List[str]


class QuoteResponse(BaseModel):
    ticker: str
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    currency: str = "USD"
    timestamp: datetime


class HealthResponse(BaseModel):
    status: str
    version: str
    services: Dict[str, str]