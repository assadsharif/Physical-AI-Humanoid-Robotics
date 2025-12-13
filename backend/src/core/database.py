"""Database configuration and session management."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import logging

from .config import get_settings

logger = logging.getLogger(__name__)

# Declarative base for all models
Base = declarative_base()


class DatabaseConfig:
    """Singleton database configuration."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        settings = get_settings()

        # Convert postgres:// to postgresql+asyncpg://
        database_url = settings.database_url
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace(
                "postgresql://", "postgresql+asyncpg://", 1
            )

        self.engine = create_async_engine(
            database_url,
            echo=settings.debug,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before checkout
            pool_recycle=3600,   # Recycle connections after 1 hour
        )

        self.async_session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        self._initialized = True
        logger.info("Database engine initialized")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session with automatic commit/rollback."""
        async with self.async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def health_check(self) -> bool:
        """Check database connectivity."""
        try:
            async with self.engine.connect() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    async def close(self):
        """Close all database connections."""
        await self.engine.dispose()
        logger.info("Database engine closed")


# Global instance
db_config = DatabaseConfig()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async for session in db_config.get_session():
        yield session
