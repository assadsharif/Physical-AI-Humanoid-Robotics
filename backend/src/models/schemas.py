"""Pydantic schemas for API request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PageContext(BaseModel):
    """Context about the current page the user is viewing."""

    chapter_id: str = Field(..., description="Current chapter identifier")
    section_id: Optional[str] = Field(None, description="Current section identifier")
    url: str = Field(..., description="Current page URL")


class ChatRequest(BaseModel):
    """Request schema for POST /api/chat."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User's question (max 500 chars)",
    )
    session_id: str = Field(..., description="Conversation session identifier (UUID)")
    selected_text: Optional[str] = Field(
        None,
        max_length=2000,
        description="User-selected text from the page (max 2000 chars)",
    )
    page_context: Optional[PageContext] = Field(
        None, description="Context about current page"
    )


class Citation(BaseModel):
    """A citation/source reference in the response."""

    chapter: str = Field(..., description="Chapter name/number")
    section: str = Field(..., description="Section name")
    url: str = Field(..., description="URL to the source")
    anchor: Optional[str] = Field(None, description="URL anchor for deep linking")
    snippet: Optional[str] = Field(
        None, max_length=200, description="Relevant text snippet"
    )
    relevance_score: float = Field(
        ..., ge=0, le=1, description="Relevance score (0-1)"
    )


class Provenance(BaseModel):
    """Metadata about how the response was generated."""

    chunks_retrieved: int = Field(..., description="Number of chunks retrieved")
    model_used: str = Field(..., description="LLM model used for generation")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")


class ChatResponse(BaseModel):
    """Response schema for POST /api/chat."""

    response_text: str = Field(..., description="Generated response text")
    sources: list[Citation] = Field(
        default_factory=list, description="Source citations"
    )
    provenance: Provenance = Field(..., description="Response generation metadata")
    conversation_id: str = Field(..., description="Conversation identifier")
    is_off_topic: bool = Field(
        False, description="Whether the query was off-topic"
    )
    status: str = Field("OK", description="Response status (OK/ERROR)")


class SearchResult(BaseModel):
    """A single search result from vector similarity search."""

    chunk_id: str = Field(..., description="Unique chunk identifier")
    content: str = Field(..., description="Chunk text content")
    chapter: str = Field(..., description="Source chapter")
    section: str = Field(..., description="Source section")
    score: float = Field(..., ge=0, le=1, description="Similarity score (0-1)")
    url: Optional[str] = Field(None, description="Source URL")


class SearchRequest(BaseModel):
    """Request schema for GET /api/search."""

    q: str = Field(..., min_length=1, max_length=500, description="Search query")
    limit: int = Field(10, ge=1, le=50, description="Maximum results to return")
    chapter: Optional[str] = Field(None, description="Filter by chapter")


class SearchResponse(BaseModel):
    """Response schema for GET /api/search."""

    results: list[SearchResult] = Field(
        default_factory=list, description="Search results"
    )
    total: int = Field(..., description="Total matching results")


class ServiceStatusEnum(str, Enum):
    """Service connection status."""

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RATE_LIMITED = "rate_limited"


class ServiceStatus(BaseModel):
    """Status of external services."""

    qdrant: str = Field(..., description="Qdrant connection status")
    neon: str = Field(..., description="Neon Postgres connection status")
    openai: str = Field(..., description="OpenAI API status")


class HealthStatusEnum(str, Enum):
    """Overall health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthResponse(BaseModel):
    """Response schema for GET /api/health."""

    status: str = Field(..., description="Overall health status")
    services: ServiceStatus = Field(..., description="Individual service statuses")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Health check timestamp"
    )
