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


class ExperienceLevel(str, Enum):
    """User experience levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ProfilePreferences(BaseModel):
    """User preferences stored as JSON."""

    theme: Optional[str] = Field(None, description="UI theme preference")
    notifications_enabled: bool = Field(True, description="Enable notifications")
    default_chapter: Optional[str] = Field(None, description="Default chapter to open")
    language: str = Field("en", description="Preferred language")

    class Config:
        extra = "allow"  # Allow additional fields


class ProfileCreate(BaseModel):
    """Request schema for creating a profile."""

    experience_level: ExperienceLevel = Field(
        ExperienceLevel.BEGINNER,
        description="User's experience level"
    )
    preferences: Optional[ProfilePreferences] = Field(
        None,
        description="User preferences"
    )


class ProfileUpdate(BaseModel):
    """Request schema for updating a profile."""

    experience_level: Optional[ExperienceLevel] = Field(
        None,
        description="Updated experience level"
    )
    preferences: Optional[ProfilePreferences] = Field(
        None,
        description="Updated preferences"
    )


class ProfileResponse(BaseModel):
    """Response schema for profile endpoints."""

    id: str = Field(..., description="Profile ID")
    user_id: str = Field(..., description="User ID")
    experience_level: ExperienceLevel = Field(..., description="Experience level")
    preferences: dict = Field(default_factory=dict, description="User preferences")
    created_at: datetime = Field(..., description="Profile creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # Enable ORM mode


class UserResponse(BaseModel):
    """Response schema for user data."""

    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User display name")
    profile: Optional[ProfileResponse] = Field(None, description="User profile")

    class Config:
        from_attributes = True
