"""Search API endpoint for vector similarity search."""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
import logging

from ...models.schemas import SearchResponse
from ...services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["search"])


def get_rag_service() -> RAGService:
    """Dependency to get RAG service instance."""
    return RAGService()


@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1, max_length=500, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    chapter: Optional[str] = Query(None, description="Filter by chapter"),
    rag_service: RAGService = Depends(get_rag_service),
) -> SearchResponse:
    """
    Perform vector similarity search on textbook content.

    Args:
        q: Search query
        limit: Maximum number of results (1-50)
        chapter: Optional chapter filter

    Returns:
        SearchResponse with matching chunks and scores
    """
    try:
        results = await rag_service.search(
            query=q,
            limit=limit,
            chapter_filter=chapter,
        )

        return SearchResponse(
            results=results,
            total=len(results),
        )

    except Exception as e:
        logger.error(f"Search endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred processing your search",
        )
