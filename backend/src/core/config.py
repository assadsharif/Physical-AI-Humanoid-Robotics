"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_env: str = "development"
    debug: bool = False
    cors_origins: str = "http://localhost:3000"

    # OpenAI
    openai_api_key: str
    embedding_model: str = "text-embedding-ada-002"
    chat_model: str = "gpt-4-turbo-preview"

    # Qdrant
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "textbook_chunks"

    # Database
    database_url: str

    # RAG Settings
    max_chunks_retrieved: int = 5
    chunk_size: int = 400
    chunk_overlap: int = 50

    # Rate Limiting
    rate_limit_per_minute: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
