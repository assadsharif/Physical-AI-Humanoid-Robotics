"""Qdrant vector database service for similarity search."""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import ResponseHandlingException
from typing import Optional
import logging
import hashlib
import uuid

from ..core.config import get_settings

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""

    def __init__(self):
        settings = get_settings()
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        self.max_results = settings.max_chunks_retrieved

    async def health_check(self) -> bool:
        """Check if Qdrant is accessible."""
        try:
            collections = self.client.get_collections()
            return any(
                c.name == self.collection_name for c in collections.collections
            )
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False

    async def search(
        self,
        query_vector: list[float],
        limit: Optional[int] = None,
        chapter_filter: Optional[str] = None,
    ) -> list[dict]:
        """
        Search for similar chunks in the vector database.

        Args:
            query_vector: Embedding vector for the query
            limit: Maximum number of results (default: max_chunks_retrieved)
            chapter_filter: Optional chapter to filter results

        Returns:
            List of matching chunks with metadata and scores
        """
        try:
            search_limit = limit or self.max_results

            # Note: Chapter filtering requires an index on the chapter field in Qdrant.
            # For now, we rely on semantic search relevance. Chapter context is still
            # available in RAG pipeline for LLM processing, just not for vector filtering.
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=search_limit,
                with_payload=True,
            )

            return [
                {
                    "chunk_id": str(result.id),
                    "content": result.payload.get("content", ""),
                    "chapter": result.payload.get("chapter", "Unknown"),
                    "section": result.payload.get("section", ""),
                    "heading": result.payload.get("heading", ""),
                    "url": result.payload.get("source_url", ""),
                    "anchor": result.payload.get("anchor", ""),
                    "score": result.score,
                }
                for result in response.points
            ]

        except ResponseHandlingException as e:
            logger.error(f"Qdrant search failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Qdrant search: {e}")
            raise

    async def search_by_text_context(
        self,
        query_vector: list[float],
        selected_text: str,
        limit: Optional[int] = None,
    ) -> list[dict]:
        """
        Search with additional filtering for selected text context.

        Args:
            query_vector: Embedding vector for the query
            selected_text: User-selected text to match against
            limit: Maximum number of results

        Returns:
            List of matching chunks prioritizing those containing selected text
        """
        # First, do a standard search
        results = await self.search(query_vector, limit=limit)

        # Boost scores for chunks that contain parts of the selected text
        selected_words = set(selected_text.lower().split())
        for result in results:
            content_words = set(result["content"].lower().split())
            overlap = len(selected_words & content_words)
            if overlap > 0:
                # Boost score based on word overlap
                boost = min(0.2, overlap * 0.02)
                result["score"] = min(1.0, result["score"] + boost)

        # Re-sort by boosted score
        results.sort(key=lambda x: x["score"], reverse=True)

        return results

    async def upsert_chunks(
        self,
        chunks: list[dict],
        vectors: list[list[float]],
    ) -> bool:
        """
        Insert or update chunks in the vector database.

        Args:
            chunks: List of chunk metadata dictionaries
            vectors: Corresponding embedding vectors

        Returns:
            True if successful
        """
        try:
            points = [
                models.PointStruct(
                    id=str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.get("chunk_id", str(i)))),
                    vector=vector,
                    payload={
                        "content": chunk["content"],
                        "chapter": chunk.get("chapter", ""),
                        "section": chunk.get("section", ""),
                        "heading": chunk.get("heading", ""),
                        "source_url": chunk.get("source_url", ""),
                        "anchor": chunk.get("anchor", ""),
                        "file_path": chunk.get("file_path", ""),
                        "doc_id": chunk.get("doc_id", ""),
                        "chunk_id": chunk.get("chunk_id", str(i)),
                    },
                )
                for i, (chunk, vector) in enumerate(zip(chunks, vectors))
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            logger.info(f"Upserted {len(points)} chunks to Qdrant")
            return True

        except Exception as e:
            logger.error(f"Failed to upsert chunks: {e}")
            raise

    async def create_collection_if_not_exists(self, vector_size: int = 1536) -> bool:
        """
        Create the collection if it doesn't exist.

        Args:
            vector_size: Dimension of embedding vectors (default: 1536 for ada-002)

        Returns:
            True if collection exists or was created
        """
        try:
            collections = self.client.get_collections()
            if any(c.name == self.collection_name for c in collections.collections):
                logger.info(f"Collection '{self.collection_name}' already exists")
                return True

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )
            logger.info(f"Created collection '{self.collection_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise
