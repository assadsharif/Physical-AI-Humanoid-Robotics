# Implementation Narrative: RAG Chatbot for Physical AI Textbook

**Feature**: RAG Chatbot
**Phase**: 2
**Date**: 2025-12-12
**Status**: Conceptual Narrative (No Implementation Code)

---

## Overview

This document provides a conceptual narrative for implementing the RAG chatbot. Per constitution principles, this contains NO executable implementation code—only architectural descriptions, data flow explanations, and conceptual pseudocode for illustration.

---

## System Context

The RAG chatbot is an embedded assistant within the Physical AI & Humanoid Robotics Docusaurus textbook. Readers interact with the chatbot to:

1. Ask questions about textbook content
2. Get explanations of selected/highlighted text
3. Navigate to relevant chapters via citations

The system is composed of four primary modules:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM BOUNDARY                                │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Docusaurus │  │   FastAPI   │  │   Qdrant    │  │    Neon     │    │
│  │  Frontend   │  │   Backend   │  │   Cloud     │  │   Postgres  │    │
│  │             │  │             │  │             │  │             │    │
│  │ ChatWidget  │  │ RAG Pipeline│  │ Vectors     │  │ Conversations│    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        ┌─────────────────────┐
                        │     OpenAI API      │
                        │  (External Service) │
                        └─────────────────────┘
```

---

## Module A: Content Ingestion Pipeline

### Purpose

Transform the 28-chapter MDX textbook content into searchable vector embeddings stored in Qdrant Cloud.

### Conceptual Flow

```
INGESTION PIPELINE (Batch Process)
==================================

Step 1: Discovery
─────────────────
  Scan: my-project/docs/**/*.mdx
  Output: List of file paths (28 chapters)

Step 2: Parsing
───────────────
  For each MDX file:
    - Parse frontmatter (title, chapter_id, sidebar_position)
    - Extract text content
    - Remove JSX components (keep text children)
    - Identify section boundaries (h2, h3 headings)
    - Output: List of (section_id, title, content, url) tuples

Step 3: Chunking
────────────────
  For each section:
    - Split content into chunks (~500 tokens)
    - Apply 100 token overlap for context continuity
    - Prefer paragraph boundaries over arbitrary splits
    - Attach metadata: chapter_id, section_id, url, title

  ILLUSTRATIVE PSEUDOCODE (NOT FOR PRODUCTION):
  ```
  function chunk_content(text, max_tokens=500, overlap=100):
    chunks = []
    paragraphs = split_by_paragraphs(text)
    current_chunk = ""

    for paragraph in paragraphs:
      if token_count(current_chunk + paragraph) <= max_tokens:
        current_chunk += paragraph
      else:
        chunks.append(current_chunk)
        # Overlap: keep last N tokens from previous chunk
        current_chunk = get_last_tokens(current_chunk, overlap) + paragraph

    if current_chunk:
      chunks.append(current_chunk)

    return chunks
  ```

Step 4: Embedding
─────────────────
  For each chunk:
    - Call OpenAI Embeddings API (ada-002)
    - Receive 1536-dimensional vector
    - Handle rate limits with exponential backoff
    - Track progress and costs

  Rate Limit Strategy:
    - Batch chunks into groups of 100
    - Wait 60 seconds between batches if rate limited
    - Log embedding costs for monitoring

Step 5: Upload to Qdrant
────────────────────────
  For each embedded chunk:
    - Create point with vector and payload
    - Payload includes: chapter_id, section_id, title, url, content
    - Batch upsert to collection (100 points per batch)

  Collection Schema:
    - Name: textbook_chunks
    - Vector size: 1536
    - Distance: Cosine
    - Payload indexes: chapter_id, section_id
```

### Verification Criteria

- [ ] All 28 chapters processed
- [ ] ~500 chunks created with consistent sizing
- [ ] Test searches return semantically relevant results
- [ ] No duplicate content from overlapping chunks

---

## Module B: FastAPI Backend

### Purpose

Serve the RAG pipeline via HTTP endpoints, coordinating embedding, retrieval, generation, and conversation management.

### API Architecture

```
BACKEND SERVICE ARCHITECTURE
============================

                    ┌─────────────────────────────────────┐
                    │           FastAPI App               │
                    │                                     │
                    │  ┌────────────────────────────────┐│
                    │  │         Middleware              ││
                    │  │  - CORS (textbook domain only) ││
                    │  │  - Rate limiting               ││
                    │  │  - Request validation          ││
                    │  └────────────────────────────────┘│
                    │                                     │
    HTTP Request    │  ┌────────────────────────────────┐│
    ───────────────►│  │         Routes Layer           ││
                    │  │  /api/health  → HealthRoute    ││
                    │  │  /api/search  → SearchRoute    ││
                    │  │  /api/chat    → ChatRoute      ││
                    │  └────────────────────────────────┘│
                    │                  │                  │
                    │                  ▼                  │
                    │  ┌────────────────────────────────┐│
                    │  │       Services Layer           ││
                    │  │  - EmbeddingService            ││
                    │  │  - QdrantService               ││
                    │  │  - OpenAIService               ││
                    │  │  - ConversationService         ││
                    │  │  - RAGService                  ││
                    │  └────────────────────────────────┘│
                    │                                     │
                    └─────────────────────────────────────┘
```

### Endpoint: POST /api/chat

**Conceptual Request Flow**:

```
CHAT REQUEST LIFECYCLE
======================

1. Request Arrives
   ┌─────────────────────────────────────────────────┐
   │ POST /api/chat                                   │
   │ {                                                │
   │   "query": "What is Zero Moment Point?",         │
   │   "session_id": "abc-123",                       │
   │   "selected_text": null,                         │
   │   "page_context": { "chapter_id": "ch19" }       │
   │ }                                                │
   └─────────────────────────────────────────────────┘
                           │
                           ▼
2. Validation & Rate Check
   - Validate request against Pydantic schema
   - Check session rate limit (30 req/min)
   - Reject if over limit (429 response)
                           │
                           ▼
3. Load Conversation History
   - Query Neon for session_id
   - Retrieve last 10 messages
   - Format for context window
                           │
                           ▼
4. Generate Query Embedding
   - Call OpenAI ada-002
   - Convert query to 1536-dim vector
   - ~100ms latency
                           │
                           ▼
5. Retrieve Relevant Chunks
   - Query Qdrant with embedding
   - Top-5 chunks with relevance scores
   - Filter by chapter if page_context provided
   - ~200ms latency
                           │
                           ▼
6. Construct RAG Prompt
   ┌─────────────────────────────────────────────────┐
   │ SYSTEM: You are the Physical AI Textbook        │
   │         Assistant. ONLY answer from context.    │
   │                                                  │
   │ CONTEXT:                                         │
   │ [Chunk 1: Chapter 19, Section 2]                │
   │ Zero Moment Point (ZMP) is defined as...        │
   │                                                  │
   │ [Chunk 2: Chapter 19, Section 3]                │
   │ The relationship between ZMP and CoM...         │
   │                                                  │
   │ CONVERSATION HISTORY:                            │
   │ (last 10 messages if any)                       │
   │                                                  │
   │ USER: What is Zero Moment Point?                │
   └─────────────────────────────────────────────────┘
                           │
                           ▼
7. Generate Response
   - Call OpenAI GPT-4 with RAG prompt
   - Parse response for citations
   - Detect if off-topic (is_off_topic flag)
   - ~2-3s latency
                           │
                           ▼
8. Save to Conversation History
   - Store user message in Neon
   - Store assistant response in Neon
   - Include citations as JSONB
                           │
                           ▼
9. Return Response
   ┌─────────────────────────────────────────────────┐
   │ {                                                │
   │   "response": "Zero Moment Point (ZMP) is...",  │
   │   "citations": [                                │
   │     { "chapter": "19", "section": "2",           │
   │       "url": "/docs/part-v/ch19#zmp" }          │
   │   ],                                             │
   │   "conversation_id": "conv-456",                │
   │   "is_off_topic": false                         │
   │ }                                                │
   └─────────────────────────────────────────────────┘
```

### Off-Topic Detection Strategy

```
OFF-TOPIC DETECTION
===================

Method: Two-stage detection

Stage 1: Retrieval Signal
  - If top retrieval score < 0.3, likely off-topic
  - If no chunks retrieved, definitely off-topic

Stage 2: LLM Classification
  - System prompt instructs model to classify
  - If model cannot answer from context, respond with:
    "I can only answer questions about the Physical AI textbook."

ILLUSTRATIVE PSEUDOCODE (NOT FOR PRODUCTION):
```
function detect_off_topic(query, retrieved_chunks):
  # Stage 1: Check retrieval quality
  if len(retrieved_chunks) == 0:
    return True, "No relevant content found"

  max_score = max(chunk.score for chunk in retrieved_chunks)
  if max_score < 0.3:
    return True, "Low relevance scores"

  # Stage 2: LLM will further classify via system prompt
  return False, None
```
```

### Conversation Context Window Management

```
CONTEXT WINDOW STRATEGY
=======================

Problem: GPT-4 has token limits; long conversations may exceed

Solution: Sliding window with summarization fallback

ILLUSTRATIVE APPROACH:

1. Keep last 10 messages (user + assistant pairs)
2. If approaching context limit (~3000 tokens):
   - Summarize older messages
   - Keep summary + last 5 messages
3. Always include system prompt + retrieved chunks first

Token Budget:
  - System prompt: ~300 tokens
  - Retrieved chunks (5x): ~2500 tokens
  - Conversation history: ~1000 tokens
  - User query: ~100 tokens
  - Response buffer: ~1000 tokens
  Total: ~5000 tokens (fits GPT-4 8K context)
```

---

## Module C: React ChatWidget

### Purpose

Provide an accessible, responsive chat interface embedded in Docusaurus pages.

### Component Architecture

```
CHATWIDGET COMPONENT TREE
=========================

<ChatWidget>                    (Container)
  │
  ├── <ChatToggle>              (Floating button to open/close)
  │
  └── <ChatPanel>               (Expandable chat interface)
        │
        ├── <ChatHeader>        (Title + close button)
        │
        ├── <MessageList>       (Conversation display)
        │     │
        │     ├── <Message role="user">
        │     │     └── User query text
        │     │
        │     └── <Message role="assistant">
        │           ├── Response text
        │           └── <CitationList>
        │                 └── <Citation> (clickable link)
        │
        ├── <ChatInput>         (Query input + submit)
        │
        └── <SelectionContext>  (Shows selected text if any)
```

### State Management

```
CHATWIDGET STATE
================

State Shape:
{
  isOpen: boolean,           // Panel visibility
  isLoading: boolean,        // API call in progress
  messages: Message[],       // Conversation history
  sessionId: string,         // Anonymous session identifier
  selectedText: string|null, // User-highlighted text
  error: string|null         // Error message if any
}

Actions:
- OPEN_CHAT: Set isOpen = true, focus input
- CLOSE_CHAT: Set isOpen = false, return focus to trigger
- SUBMIT_QUERY: Set isLoading = true, call API
- RECEIVE_RESPONSE: Add message, set isLoading = false
- SET_SELECTION: Capture selected text for context
- CLEAR_SELECTION: Remove selection context
- SET_ERROR: Display error message

ILLUSTRATIVE STATE FLOW:

User clicks chat icon
  → OPEN_CHAT
  → Panel slides in, focus moves to input

User types query, presses Enter
  → SUBMIT_QUERY
  → Loading indicator shown
  → API call to /api/chat

Response received
  → RECEIVE_RESPONSE
  → Message added to list
  → Scroll to bottom

User clicks close
  → CLOSE_CHAT
  → Panel slides out
  → Focus returns to chat icon
```

### Text Selection Detection

```
SELECTION HANDLER CONCEPT
=========================

Purpose: Detect when user highlights text in textbook content

Trigger: User selects text in .markdown-content area

Flow:
1. Listen for 'mouseup' event on content container
2. Get window.getSelection() text
3. If text length > 10 chars and < 2000 chars:
   - Show small "Ask about this" button near selection
   - Capture selection metadata (page URL, offsets)
4. User clicks "Ask about this":
   - Open chat with selectedText populated
   - Prefill input with "Explain this" or similar

ILLUSTRATIVE PSEUDOCODE (NOT FOR PRODUCTION):
```
function handleSelection(event):
  selection = window.getSelection()
  text = selection.toString().trim()

  if 10 < len(text) < 2000:
    showSelectionPopover(
      text: text,
      position: getSelectionBounds()
    )

function onAskAboutSelection(text):
  dispatch(SET_SELECTION, text)
  dispatch(OPEN_CHAT)
  focusInput()
```
```

### Accessibility Implementation

```
ACCESSIBILITY REQUIREMENTS
==========================

1. ARIA Roles and Labels
   - Chat panel: role="dialog", aria-label="Textbook Assistant"
   - Input: aria-label="Ask a question about the textbook"
   - Send button: aria-label="Send message"
   - Close button: aria-label="Close chat"
   - Messages: role="log", aria-live="polite"

2. Keyboard Navigation
   - Tab: Move through interactive elements
   - Escape: Close chat panel
   - Enter: Submit query
   - Arrow keys: Navigate message history (optional)

3. Focus Management
   - On open: Focus moves to input field
   - On close: Focus returns to chat toggle button
   - New message: Announce via aria-live region

4. Color Contrast
   - All text: Minimum 4.5:1 contrast ratio
   - Interactive elements: Visible focus indicators
   - Error states: Not conveyed by color alone

ILLUSTRATIVE FOCUS TRAP:
```
function ChatPanel({ isOpen }):
  if not isOpen:
    return null

  useEffect:
    # Save previously focused element
    previousFocus = document.activeElement

    # Focus input on mount
    inputRef.focus()

    # Trap focus within panel
    panel.addEventListener('keydown', handleKeyDown)

    return:
      # Restore focus on unmount
      previousFocus.focus()
```
```

---

## Module D: Database Schemas

### Neon Postgres Schema

```
DATABASE SCHEMA
===============

Table: conversations
────────────────────
id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
session_id      VARCHAR(255) NOT NULL
created_at      TIMESTAMP DEFAULT NOW()
updated_at      TIMESTAMP DEFAULT NOW()

Index: idx_conversations_session_id ON session_id

Table: messages
───────────────
id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE
role            VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant'))
content         TEXT NOT NULL
citations       JSONB DEFAULT '[]'
created_at      TIMESTAMP DEFAULT NOW()

Index: idx_messages_conversation_id ON conversation_id
Index: idx_messages_created_at ON created_at

Table: analytics (optional)
───────────────────────────
id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
session_id      VARCHAR(255) NOT NULL
query           TEXT
response_time   INTEGER  -- milliseconds
chunk_count     INTEGER
is_off_topic    BOOLEAN
created_at      TIMESTAMP DEFAULT NOW()
```

### Qdrant Collection Schema

```
QDRANT COLLECTION: textbook_chunks
==================================

Vector Configuration:
  - Size: 1536
  - Distance: Cosine

Payload Schema:
  - chunk_id: string (unique identifier)
  - chapter_id: string (e.g., "ch01", "ch19")
  - section_id: string (e.g., "introduction", "zmp-theory")
  - title: string (section heading)
  - url: string (full path with anchor)
  - content: string (chunk text)
  - page_number: integer (optional, approximate)

Indexes:
  - chapter_id: Keyword index (for filtering)
  - section_id: Keyword index (for filtering)
```

---

## Error Handling Strategy

```
ERROR HANDLING MATRIX
=====================

| Error Type           | Detection               | Response                           |
|---------------------|-------------------------|-----------------------------------|
| OpenAI rate limit   | 429 status code         | Retry with backoff, fallback msg  |
| OpenAI unavailable  | 5xx or timeout          | "Service temporarily unavailable" |
| Qdrant unavailable  | Connection error        | Return cached response or error   |
| Neon unavailable    | Connection error        | Chat works, no history saved      |
| Invalid input       | Pydantic validation     | 400 with specific error message   |
| Query too long      | Length check            | Truncate with warning             |
| Selection too long  | Length check            | Reject with message               |
| Off-topic query     | Retrieval + LLM check   | Polite refusal response           |
| No results found    | Empty retrieval         | "Couldn't find information"       |

Graceful Degradation Priority:
1. Chat must always respond (even if degraded)
2. Citations optional if retrieval fails
3. History optional if Neon fails
4. User should never see raw errors
```

---

## Security Considerations

```
SECURITY MEASURES
=================

1. Prompt Injection Prevention
   - User input placed in dedicated section of prompt
   - System instructions clearly separated
   - Output validation against expected format

2. Input Sanitization
   - HTML entities escaped
   - Maximum length enforced
   - Rate limiting per session

3. API Security
   - CORS restricted to textbook domain
   - No authentication (anonymous sessions)
   - API keys stored in environment variables
   - HTTPS only

4. Data Privacy
   - No PII collected
   - Sessions identified by random UUID
   - Conversation pruning after 30 days
   - No analytics on query content (only metadata)
```

---

## Performance Optimization

```
PERFORMANCE TARGETS AND STRATEGIES
==================================

Target: p95 response latency < 5 seconds

Latency Breakdown:
  - Embedding: ~100ms
  - Retrieval: ~200ms
  - Generation: ~2-3s
  - Overhead: ~200ms
  Total: ~3-4s typical

Optimization Strategies:

1. Parallel Operations
   - Load conversation history while embedding query
   - Start retrieval as soon as embedding completes

2. Caching (if needed)
   - Cache embeddings for common queries
   - Cache retrieval results for short TTL
   - Not implemented in v1 (premature optimization)

3. Streaming (future enhancement)
   - Stream GPT-4 response tokens
   - Display partial response as it generates
   - Reduces perceived latency
```

---

## Testing Strategy

```
TESTING APPROACH
================

Unit Tests (pytest):
  - EmbeddingService: Mock OpenAI, test batching
  - QdrantService: Mock Qdrant client, test search
  - RAGService: Mock dependencies, test pipeline
  - ConversationService: Test with test database

Integration Tests:
  - Full chat flow with real services (staging env)
  - Rate limiting behavior
  - Error handling paths

E2E Tests (Playwright):
  - Chat widget interaction
  - Text selection flow
  - Accessibility checks
  - Mobile responsiveness

Quality Tests:
  - Sample query evaluation (human review)
  - Citation accuracy verification
  - Off-topic detection effectiveness
```

---

## Deployment Considerations

```
DEPLOYMENT ARCHITECTURE
=======================

                     ┌─────────────────────────────┐
                     │        CDN / Vercel         │
                     │   (Docusaurus Static Site)  │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      Internet                                │
└─────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │    Railway / Render / Fly   │
                     │      (FastAPI Backend)      │
                     └──────────────┬──────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Qdrant Cloud  │      │   Neon Postgres │      │   OpenAI API    │
│  (Vector Store) │      │   (Database)    │      │  (LLM/Embed)    │
└─────────────────┘      └─────────────────┘      └─────────────────┘

Environment Variables Required:
  - QDRANT_URL
  - QDRANT_API_KEY
  - DATABASE_URL (Neon connection string)
  - OPENAI_API_KEY
  - CORS_ORIGINS (textbook domain)
```

---

**Implementation Narrative Version**: 1.0.0 | **Author**: Claude Code Agent | **Status**: Conceptual Only
