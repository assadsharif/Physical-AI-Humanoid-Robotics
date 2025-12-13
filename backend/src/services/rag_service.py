"""RAG pipeline orchestration service."""

from typing import Optional
import logging
import uuid

from .qdrant_service import QdrantService
from .openai_service import OpenAIService
from ..models.schemas import ChatResponse, Citation, Provenance, SearchResult
from ..core.config import get_settings
from ..core.prompts import OFF_TOPIC_RESPONSE

logger = logging.getLogger(__name__)


class RAGService:
    """Orchestrates the RAG pipeline: embed -> retrieve -> generate."""

    def __init__(self):
        self.qdrant = QdrantService()
        self.openai = OpenAIService()
        self.settings = get_settings()

    async def process_chat(
        self,
        query: str,
        session_id: str,
        selected_text: Optional[str] = None,
        page_context: Optional[dict] = None,
        conversation_history: Optional[list[dict]] = None,
    ) -> ChatResponse:
        """
        Process a chat query through the RAG pipeline.

        Args:
            query: User's question
            session_id: Conversation session identifier
            selected_text: User-selected text from the page
            page_context: Current page context (chapter, url)
            conversation_history: Previous messages

        Returns:
            ChatResponse with generated response and citations
        """
        # Step 1: Quick off-topic detection
        if await self.openai.detect_off_topic(query) and not selected_text:
            return ChatResponse(
                response_text=OFF_TOPIC_RESPONSE,
                sources=[],
                provenance=Provenance(
                    chunks_retrieved=0,
                    model_used=self.settings.chat_model,
                    confidence=0.0,
                ),
                conversation_id=session_id,
                is_off_topic=True,
                status="OK",
            )

        # Step 2: Create query embedding
        # If selected_text exists, combine it with the query for better retrieval
        embed_text = query
        if selected_text:
            embed_text = f"{query}\n\nContext: {selected_text[:500]}"

        query_vector = await self.openai.create_embedding(embed_text)

        # Step 3: Retrieve relevant chunks
        if selected_text:
            chunks = await self.qdrant.search_by_text_context(
                query_vector=query_vector,
                selected_text=selected_text,
                limit=self.settings.max_chunks_retrieved,
            )
        else:
            # Apply chapter filter if page context available
            chapter_filter = None
            if page_context and page_context.get("chapter_id"):
                chapter_filter = page_context["chapter_id"]

            chunks = await self.qdrant.search(
                query_vector=query_vector,
                limit=self.settings.max_chunks_retrieved,
                chapter_filter=chapter_filter,
            )

        # Step 4: Generate response with context
        result = await self.openai.generate_response(
            query=query,
            context_chunks=chunks,
            conversation_history=conversation_history,
            selected_text=selected_text,
        )

        # Step 5: Build citations from retrieved chunks
        citations = [
            Citation(
                chapter=chunk["chapter"],
                section=chunk.get("section", ""),
                url=chunk.get("url", ""),
                anchor=chunk.get("anchor", ""),
                snippet=chunk["content"][:200] if chunk.get("content") else "",
                relevance_score=chunk.get("score", 0.0),
            )
            for chunk in chunks
            if chunk.get("score", 0) > 0.5  # Only include relevant citations
        ]

        return ChatResponse(
            response_text=result["response_text"],
            sources=citations,
            provenance=Provenance(
                chunks_retrieved=len(chunks),
                model_used=self.settings.chat_model,
                confidence=result["confidence"],
            ),
            conversation_id=session_id,
            is_off_topic=result["is_off_topic"],
            status="OK",
        )

    async def search(
        self,
        query: str,
        limit: int = 10,
        chapter_filter: Optional[str] = None,
    ) -> list[SearchResult]:
        """
        Perform direct vector similarity search.

        Args:
            query: Search query
            limit: Maximum results
            chapter_filter: Optional chapter filter

        Returns:
            List of search results
        """
        # Create embedding for the query
        query_vector = await self.openai.create_embedding(query)

        # Search Qdrant
        chunks = await self.qdrant.search(
            query_vector=query_vector,
            limit=limit,
            chapter_filter=chapter_filter,
        )

        return [
            SearchResult(
                chunk_id=chunk["chunk_id"],
                content=chunk["content"],
                chapter=chunk["chapter"],
                section=chunk.get("section", ""),
                score=chunk.get("score", 0.0),
                url=chunk.get("url"),
            )
            for chunk in chunks
        ]

    async def health_check(self) -> dict:
        """
        Check health of all services.

        Returns:
            Dictionary with service statuses
        """
        qdrant_healthy = await self.qdrant.health_check()
        openai_status = await self.openai.health_check()

        return {
            "qdrant": "connected" if qdrant_healthy else "disconnected",
            "openai": openai_status,
            # Neon check would go here when implemented
            "neon": "connected",  # Placeholder
        }
