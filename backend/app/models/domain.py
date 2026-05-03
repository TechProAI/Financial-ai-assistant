"""Internal domain models used between services and agents."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class RetrievedChunk:
    """A chunk retrieved from the vector store."""
    text: str
    source: str
    title: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NewsArticle:
    title: str
    summary: str
    url: str
    published: str
    source: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None