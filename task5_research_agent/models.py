from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """Single mock search result."""

    title: str
    url: str
    snippet: str


class ResearchSummary(BaseModel):
    """Structured output from the research agent."""
    
    question: str = Field(description="Original user research question")
    short_answer: str = Field(description="One paragraph, high-level answer")
    key_points: List[str] = Field(
        description="Bullet-point list of key findings, 3–7 items"
    )
    assumptions: List[str] = Field(
        description="Explicit assumptions or caveats the model is relying on"
    )
    sources: List[str] = Field(
        description="Human-readable list of sources used (URLs or titles)"
    )
    num_snippets: int = 0

@dataclass
class ResearchDependencies:
    """
    Dependencies available to the agent.

    In a real system this might include:
    - HTTP clients
    - Vector DB handle
    - Configuration flags
    """

    max_snippets: int = 5
    created_at: datetime = datetime.utcnow()


@dataclass
class ResearchContext:
    """Simple context object used in our own logging / orchestration."""

    question: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    num_snippets: int = 0

    def mark_completed(self) -> None:
        self.completed_at = datetime.utcnow()
