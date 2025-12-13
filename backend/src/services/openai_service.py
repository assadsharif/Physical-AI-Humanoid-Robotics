"""OpenAI service for embeddings and chat completion."""

from openai import OpenAI, APIError, RateLimitError
from typing import Optional
import logging

from ..core.config import get_settings
from ..core.prompts import SYSTEM_PROMPT, OFF_TOPIC_RESPONSE, NO_RESULTS_RESPONSE

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI APIs."""

    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.embedding_model = settings.embedding_model
        self.chat_model = settings.chat_model

    async def health_check(self) -> str:
        """
        Check OpenAI API availability.

        Returns:
            'available', 'rate_limited', or 'unavailable'
        """
        try:
            # Make a minimal API call to check availability
            self.client.models.list()
            return "available"
        except RateLimitError:
            return "rate_limited"
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return "unavailable"

    async def create_embedding(self, text: str) -> list[float]:
        """
        Create an embedding vector for the given text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (1536 dimensions for ada-002)
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text,
            )
            return response.data[0].embedding

        except RateLimitError as e:
            logger.warning(f"OpenAI rate limit hit: {e}")
            raise
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def create_embeddings_batch(
        self, texts: list[str], batch_size: int = 100
    ) -> list[list[float]]:
        """
        Create embeddings for multiple texts in batches.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts per API call

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            try:
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch,
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
                logger.info(f"Embedded batch {i // batch_size + 1}")

            except RateLimitError:
                logger.warning("Rate limit hit, waiting...")
                import asyncio
                await asyncio.sleep(60)
                # Retry this batch
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch,
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

        return all_embeddings

    async def generate_response(
        self,
        query: str,
        context_chunks: list[dict],
        conversation_history: Optional[list[dict]] = None,
        selected_text: Optional[str] = None,
    ) -> dict:
        """
        Generate a RAG response using GPT-4.

        Args:
            query: User's question
            context_chunks: Retrieved chunks with content and metadata
            conversation_history: Previous messages in the conversation
            selected_text: User-selected text from the page

        Returns:
            Dictionary with response_text, is_off_topic, and confidence
        """
        # Check if we have any context
        if not context_chunks:
            return {
                "response_text": NO_RESULTS_RESPONSE,
                "is_off_topic": False,
                "confidence": 0.0,
            }

        # Format context from chunks
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(
                f"[{i}] Chapter: {chunk['chapter']}, Section: {chunk.get('section', 'N/A')}\n"
                f"URL: {chunk.get('url', 'N/A')}\n"
                f"Content: {chunk['content']}\n"
            )
        context = "\n---\n".join(context_parts)

        # Format conversation history
        history = ""
        if conversation_history:
            history_parts = []
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = "User" if msg["role"] == "user" else "Assistant"
                history_parts.append(f"{role}: {msg['content']}")
            history = "\n".join(history_parts)

        # Build the prompt
        prompt = SYSTEM_PROMPT.format(
            context=context,
            history=history or "No previous conversation",
            query=query,
            selected_text=selected_text or "None",
        )

        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            response_text = response.choices[0].message.content

            # Check for off-topic indicators
            is_off_topic = any(
                phrase in response_text.lower()
                for phrase in [
                    "i can only answer",
                    "outside the scope",
                    "not covered in the textbook",
                    "cannot help with",
                ]
            )

            # Estimate confidence based on context quality
            avg_score = (
                sum(c.get("score", 0.5) for c in context_chunks) / len(context_chunks)
                if context_chunks
                else 0.0
            )

            return {
                "response_text": response_text,
                "is_off_topic": is_off_topic,
                "confidence": avg_score,
            }

        except RateLimitError:
            logger.warning("Rate limit hit during response generation")
            return {
                "response_text": "The assistant is busy. Please try again in a few seconds.",
                "is_off_topic": False,
                "confidence": 0.0,
            }
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def detect_off_topic(self, query: str) -> bool:
        """
        Quick check if a query is likely off-topic.

        Args:
            query: User's question

        Returns:
            True if query appears to be off-topic
        """
        # Keywords that suggest on-topic queries
        on_topic_keywords = [
            "robot", "humanoid", "ros", "ros2", "simulation", "gazebo",
            "isaac", "control", "locomotion", "kinematic", "dynamic",
            "bipedal", "walking", "manipulation", "grasp", "vla",
            "vision", "language", "action", "ai", "physical",
            "sensor", "actuator", "joint", "motor", "servo",
            "chapter", "textbook", "explain", "what is", "how does",
        ]

        query_lower = query.lower()
        return not any(keyword in query_lower for keyword in on_topic_keywords)
