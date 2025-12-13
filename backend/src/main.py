"""FastAPI application for RAG Chatbot backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .core.config import get_settings
from .api.routes import chat_router, search_router, health_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Physical AI Textbook RAG Chatbot",
        description="RAG-powered chatbot API for the Physical AI & Humanoid Robotics textbook",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Configure CORS
    origins = settings.cors_origins.split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(chat_router)
    app.include_router(search_router)
    app.include_router(health_router)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting RAG Chatbot API...")
        logger.info(f"Environment: {settings.app_env}")
        logger.info(f"Debug mode: {settings.debug}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down RAG Chatbot API...")

    @app.get("/")
    async def root():
        return {
            "name": "Physical AI Textbook RAG Chatbot",
            "version": "1.0.0",
            "docs": "/docs" if settings.debug else "disabled",
        }

    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
