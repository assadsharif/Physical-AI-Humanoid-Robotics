"""Profile API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging

from ...models.schemas import ProfileCreate, ProfileUpdate, ProfileResponse
from ...services.profile_service import ProfileService
from ...core.database import get_db
from ...core.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/profile", tags=["profile"])


def get_profile_service() -> ProfileService:
    """Dependency to get profile service instance."""
    return ProfileService()


@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(
    request: ProfileCreate,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: ProfileService = Depends(get_profile_service),
) -> ProfileResponse:
    """
    Create user profile (authenticated).

    Creates a new profile for the authenticated user.
    Returns 409 if profile already exists.

    Args:
        request: Profile creation data
        user: Authenticated user data
        db: Database session
        service: Profile service

    Returns:
        Created profile
    """
    try:
        user_id = UUID(user["id"])

        # Check if profile already exists
        existing = await service.get_profile(db, user_id)
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Profile already exists for this user"
            )

        # Create profile
        profile = await service.get_or_create_profile(db, user_id, request)

        return ProfileResponse(
            id=str(profile.id),
            user_id=str(profile.user_id),
            experience_level=profile.experience_level,
            preferences=profile.preferences or {},
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile creation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create profile"
        )


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: ProfileService = Depends(get_profile_service),
) -> ProfileResponse:
    """
    Get current user's profile (authenticated).

    Returns profile for the authenticated user.
    Creates profile automatically if it doesn't exist.

    Args:
        user: Authenticated user data
        db: Database session
        service: Profile service

    Returns:
        User profile
    """
    try:
        user_id = UUID(user["id"])

        # Get or create profile
        profile = await service.get_or_create_profile(db, user_id)

        return ProfileResponse(
            id=str(profile.id),
            user_id=str(profile.user_id),
            experience_level=profile.experience_level,
            preferences=profile.preferences or {},
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )

    except Exception as e:
        logger.error(f"Profile retrieval error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve profile"
        )


@router.patch("/preferences", response_model=ProfileResponse)
async def update_preferences(
    request: ProfileUpdate,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: ProfileService = Depends(get_profile_service),
) -> ProfileResponse:
    """
    Update user preferences (authenticated).

    Updates profile preferences for the authenticated user.
    Creates profile if it doesn't exist.

    Args:
        request: Profile update data
        user: Authenticated user data
        db: Database session
        service: Profile service

    Returns:
        Updated profile
    """
    try:
        user_id = UUID(user["id"])

        # Get or create profile
        profile = await service.get_or_create_profile(db, user_id)

        # Update profile
        updated_profile = await service.update_profile(db, user_id, request)

        return ProfileResponse(
            id=str(updated_profile.id),
            user_id=str(updated_profile.user_id),
            experience_level=updated_profile.experience_level,
            preferences=updated_profile.preferences or {},
            created_at=updated_profile.created_at,
            updated_at=updated_profile.updated_at,
        )

    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update profile"
        )


@router.delete("/", status_code=204)
async def delete_profile(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: ProfileService = Depends(get_profile_service),
):
    """
    Delete user profile (authenticated).

    Deletes profile for the authenticated user.
    Does not delete the user account itself.

    Args:
        user: Authenticated user data
        db: Database session
        service: Profile service
    """
    try:
        user_id = UUID(user["id"])

        deleted = await service.delete_profile(db, user_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile deletion error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete profile"
        )
