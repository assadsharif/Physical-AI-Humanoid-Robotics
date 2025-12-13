"""Authentication and authorization utilities."""

from typing import Optional
from fastapi import Depends, HTTPException, Header
import httpx
import logging

from .config import get_settings

logger = logging.getLogger(__name__)


class AuthServiceError(Exception):
    """Raised when auth service is unavailable."""
    pass


async def validate_session_token(token: str) -> dict:
    """
    Validate session token with auth service.

    Args:
        token: Session token from Authorization header

    Returns:
        User data from session

    Raises:
        HTTPException: 401 if token is invalid or expired
        AuthServiceError: If auth service is unreachable
    """
    settings = get_settings()

    try:
        async with httpx.AsyncClient(timeout=settings.auth_service_timeout) as client:
            response = await client.get(
                f"{settings.auth_service_url}/api/auth/session",
                headers={"Authorization": f"Bearer {token}"},
            )

            if response.status_code == 200:
                session_data = response.json()
                return session_data.get("user")

            elif response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or expired session token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            else:
                logger.error(f"Auth service returned {response.status_code}")
                raise AuthServiceError("Auth service error")

    except httpx.TimeoutException:
        logger.error("Auth service timeout")
        raise AuthServiceError("Auth service timeout")

    except httpx.RequestError as e:
        logger.error(f"Auth service connection error: {e}")
        raise AuthServiceError("Auth service unavailable")


async def get_current_user_optional(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> Optional[dict]:
    """
    Get current user from Authorization header (optional).

    Returns None if no token provided or token is invalid.
    Used for endpoints that support both authenticated and anonymous access.

    Args:
        authorization: Authorization header value

    Returns:
        User data dict or None
    """
    if not authorization:
        return None

    try:
        # Extract token (format: "Bearer <token>")
        if not authorization.startswith("Bearer "):
            return None

        token = authorization[7:]  # Remove "Bearer " prefix

        user_data = await validate_session_token(token)
        return user_data

    except (HTTPException, AuthServiceError):
        # Silently return None for optional auth
        return None


async def get_current_user(
    user: Optional[dict] = Depends(get_current_user_optional)
) -> dict:
    """
    Get current user from Authorization header (required).

    Raises 401 if not authenticated.
    Used for endpoints that require authentication.

    Args:
        user: User data from optional dependency

    Returns:
        User data dict

    Raises:
        HTTPException: 401 if not authenticated
    """
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def auth_service_health_check() -> dict:
    """
    Check auth service health.

    Returns:
        Dict with status information
    """
    settings = get_settings()

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(
                f"{settings.auth_service_url}/api/health"
            )

            if response.status_code == 200:
                return {
                    "status": "connected",
                    "url": settings.auth_service_url,
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
            else:
                return {
                    "status": "degraded",
                    "url": settings.auth_service_url,
                    "error": f"HTTP {response.status_code}"
                }
    except Exception as e:
        return {
            "status": "disconnected",
            "url": settings.auth_service_url,
            "error": str(e)
        }
