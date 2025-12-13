"""Health check endpoint for monitoring."""

from fastapi import APIRouter, Depends
from datetime import datetime
import logging

from ...models.schemas import HealthResponse, ServiceStatus
from ...services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["health"])


def get_rag_service() -> RAGService:
    """Dependency to get RAG service instance."""
    return RAGService()


@router.get("/health", response_model=HealthResponse)
async def health_check(
    rag_service: RAGService = Depends(get_rag_service),
) -> HealthResponse:
    """
    Check health status of all services.

    Returns:
        HealthResponse with overall status and individual service statuses
    """
    try:
        statuses = await rag_service.health_check()

        # Determine overall health
        all_connected = all(
            status in ("connected", "available")
            for status in statuses.values()
        )

        any_disconnected = any(
            status in ("disconnected", "unavailable")
            for status in statuses.values()
        )

        if all_connected:
            overall_status = "healthy"
        elif any_disconnected:
            overall_status = "unhealthy"
        else:
            overall_status = "degraded"

        return HealthResponse(
            status=overall_status,
            services=ServiceStatus(
                qdrant=statuses.get("qdrant", "disconnected"),
                neon=statuses.get("neon", "disconnected"),
                openai=statuses.get("openai", "unavailable"),
            ),
            timestamp=datetime.utcnow(),
        )

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            services=ServiceStatus(
                qdrant="disconnected",
                neon="disconnected",
                openai="unavailable",
            ),
            timestamp=datetime.utcnow(),
        )
