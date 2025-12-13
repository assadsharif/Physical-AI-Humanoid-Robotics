"""Chat API endpoint for RAG-powered responses."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging

from ...models.schemas import ChatRequest, ChatResponse
from ...services.rag_service import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


def get_rag_service() -> RAGService:
    """Dependency to get RAG service instance."""
    return RAGService()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
) -> ChatResponse:
    """
    Process a chat query and return a RAG-generated response.

    Args:
        request: Chat request with query, session_id, optional selected_text

    Returns:
        ChatResponse with generated answer and source citations
    """
    try:
        # Validate query
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty",
            )

        # Convert page_context to dict if present
        page_context = None
        if request.page_context:
            page_context = {
                "chapter_id": request.page_context.chapter_id,
                "section_id": request.page_context.section_id,
                "url": request.page_context.url,
            }

        # Process through RAG pipeline
        response = await rag_service.process_chat(
            query=request.query,
            session_id=request.session_id,
            selected_text=request.selected_text,
            page_context=page_context,
            conversation_history=None,  # TODO: Load from database
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred processing your request",
        )


@router.options("/chat")
async def chat_options():
    """Handle CORS preflight for chat endpoint."""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
    )
