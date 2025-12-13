"""Profile management service."""

from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import logging

from ..models.database import User, UserProfile
from ..models.schemas import ProfileCreate, ProfileUpdate, ProfileResponse

logger = logging.getLogger(__name__)


class ProfileService:
    """Service for managing user profiles."""

    def __init__(self):
        """Initialize profile service."""
        pass

    async def get_or_create_profile(
        self,
        db: AsyncSession,
        user_id: UUID,
        profile_data: Optional[ProfileCreate] = None
    ) -> UserProfile:
        """
        Get existing profile or create new one.

        Args:
            db: Database session
            user_id: User ID
            profile_data: Optional profile creation data

        Returns:
            UserProfile instance
        """
        # Try to get existing profile
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if profile:
            return profile

        # Create new profile
        profile_dict = profile_data.model_dump() if profile_data else {}

        profile = UserProfile(
            user_id=user_id,
            experience_level=profile_dict.get("experience_level", "beginner"),
            preferences=profile_dict.get("preferences", {})
        )

        db.add(profile)
        await db.flush()  # Get ID without committing

        logger.info(f"Created profile for user {user_id}")
        return profile

    async def get_profile(
        self,
        db: AsyncSession,
        user_id: UUID
    ) -> Optional[UserProfile]:
        """
        Get user profile by user ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            UserProfile or None
        """
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_profile(
        self,
        db: AsyncSession,
        user_id: UUID,
        profile_update: ProfileUpdate
    ) -> Optional[UserProfile]:
        """
        Update user profile.

        Args:
            db: Database session
            user_id: User ID
            profile_update: Updated profile data

        Returns:
            Updated UserProfile or None if not found
        """
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            return None

        # Update only provided fields
        update_data = profile_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(profile, field, value)

        await db.flush()

        logger.info(f"Updated profile for user {user_id}")
        return profile

    async def delete_profile(
        self,
        db: AsyncSession,
        user_id: UUID
    ) -> bool:
        """
        Delete user profile.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            True if deleted, False if not found
        """
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            return False

        await db.delete(profile)
        await db.flush()

        logger.info(f"Deleted profile for user {user_id}")
        return True

    async def health_check(self) -> dict:
        """
        Service health check.

        Returns:
            Status dict
        """
        return {"status": "healthy", "service": "ProfileService"}
