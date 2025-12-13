# Feature Specification: RAG Chatbot for Physical AI Textbook

**Feature Branch**: `feature/rag-chatbot`
**Created**: 2025-12-12
**Status**: Draft
**Phase**: 2 (Follows Phase 1: Docusaurus Site Structure)
**Input**: User description: "Embedded RAG chatbot visible on site using OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres DB, and Qdrant Cloud Free Tier. Must answer general book questions and user-selected text questions only."

---

## Problem Statement

The Physical AI & Humanoid Robotics textbook requires an intelligent assistant that can answer reader questions contextually. Currently, readers must manually search through 28 chapters and 200+ glossary terms. An embedded RAG chatbot would provide:
1. Instant answers to questions about textbook content
2. Ability to explain user-selected/highlighted text passages
3. Guided learning paths based on reader context
4. No hallucination through strict retrieval-augmented generation

---

## Goals

1. **Embedded Chatbot**: Visible, accessible chat widget on all textbook pages
2. **RAG-Powered Responses**: All answers grounded in actual textbook content
3. **Text Selection Q&A**: Users can highlight text and ask questions about it
4. **Book-Scoped Answers**: Chatbot ONLY answers questions about textbook content
5. **Citation Transparency**: Every response cites source chapter/section
6. **Low Latency**: Responses within 5 seconds for standard queries

---

## Non-Goals

- General-purpose AI assistant (must stay book-scoped)
- User authentication or personalized learning history
- Multi-language support (English only for v1)
- Voice input/output
- Integration with external knowledge bases
- Real-time content updates (batch ingestion only)

---

## Inputs

- **Textbook Content**: 28 chapters in MDX format from `/my-project/docs/`
- **Glossary Terms**: 200+ terms with definitions
- **User Queries**: Natural language questions about book content
- **Selected Text**: User-highlighted passages for contextual Q&A

---

## Outputs

- **Chat Responses**: Grounded answers with chapter/section citations
- **Source References**: Links to relevant textbook sections
- **Clarification Prompts**: When query is ambiguous or off-topic
- **Out-of-Scope Responses**: Polite refusal for non-book questions

---

## Dependencies

### Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Vector Store** | Qdrant Cloud Free Tier | Managed vector DB, 1GB free storage, REST API |
| **Backend API** | FastAPI (Python 3.11+) | Async, OpenAPI spec, Pydantic validation |
| **Database** | Neon Serverless Postgres | Conversation history, usage analytics, serverless scaling |
| **AI/LLM** | OpenAI Agents SDK + ChatKit | GPT-4 for generation, ada-002 for embeddings |
| **Frontend** | React component in Docusaurus | MDX-compatible, TypeScript |
| **Orchestration** | LangChain | RAG pipeline, prompt templates, chain composition |

### External Services

- **OpenAI API**: GPT-4/GPT-4-turbo for response generation
- **OpenAI Embeddings API**: text-embedding-ada-002 for vector embeddings
- **Qdrant Cloud**: Vector similarity search (free tier: 1GB, 1M vectors)
- **Neon Database**: Serverless Postgres (free tier: 512MB storage)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - General Book Question (Priority: P1)

A reader wants to understand a concept mentioned in the textbook and asks a general question like "What is Zero Moment Point in bipedal locomotion?"

**Why this priority**: Core chatbot functionality. Without general Q&A, the chatbot has no value.

**Independent Test**: Can be fully tested by asking 10 representative questions covering each Part and verifying accurate, cited responses.

**Acceptance Scenarios**:

1. **Given** a reader on any textbook page, **When** they type "What is ZMP?" in the chatbot, **Then** they receive a response citing Chapter 19 (Bipedal Locomotion) with accurate definition
2. **Given** a reader asking about ROS2 lifecycle states, **When** response is generated, **Then** it includes specific state names and cites Chapter 10
3. **Given** a reader asking "How do I make pizza?", **When** chatbot detects off-topic query, **Then** it politely responds "I can only answer questions about the Physical AI & Humanoid Robotics textbook content."

---

### User Story 2 - Selected Text Explanation (Priority: P1)

A reader highlights a complex passage in the textbook and asks "Explain this to me" or "What does this mean?"

**Why this priority**: Differentiating feature. Enables contextual, targeted assistance at point of confusion.

**Independent Test**: Can be fully tested by selecting 5 technical passages across different Parts and requesting explanations.

**Acceptance Scenarios**:

1. **Given** a reader highlights "DCM trajectory generation ensures smooth transitions between support phases", **When** they ask "Explain this", **Then** chatbot explains Divergent Component of Motion with simplified language and cites source
2. **Given** a reader selects a pseudocode block, **When** they ask "What does this do?", **Then** chatbot explains the algorithm step-by-step
3. **Given** a reader selects text and asks an unrelated question, **When** chatbot detects mismatch, **Then** it asks "Did you want me to explain the selected text, or answer your question about [topic]?"

---

### User Story 3 - Conversation Context Retention (Priority: P2)

A reader has a multi-turn conversation, asking follow-up questions that reference previous exchanges.

**Why this priority**: Improves learning experience by enabling deeper exploration without repetition.

**Independent Test**: Can be tested with 3-turn conversation threads verifying context retention.

**Acceptance Scenarios**:

1. **Given** reader asks "What is whole-body control?" followed by "How does it handle redundancy?", **When** second question is processed, **Then** response understands "it" refers to whole-body control
2. **Given** a conversation about simulation platforms, **When** reader asks "Which one supports reinforcement learning?", **Then** chatbot references previously discussed platforms
3. **Given** conversation exceeds 10 turns, **When** context window limits approach, **Then** chatbot summarizes earlier context and continues coherently

---

### User Story 4 - Source Navigation (Priority: P2)

A reader wants to dive deeper into a topic mentioned in a chatbot response by navigating directly to the source.

**Why this priority**: Bridges chat assistance to deep reading, completing the learning loop.

**Independent Test**: Can be tested by verifying all cited sources in responses contain clickable links that resolve correctly.

**Acceptance Scenarios**:

1. **Given** chatbot responds about VLA architecture, **When** response cites "Chapter 24, Section 2", **Then** citation is a clickable link to that location
2. **Given** chatbot cites multiple sources, **When** response includes "[1], [2], [3]" style citations, **Then** each citation links to the correct chapter
3. **Given** a response with glossary term references, **When** term is mentioned, **Then** it links to glossary entry

---

### User Story 5 - Chat Widget Accessibility (Priority: P2)

A reader using assistive technology (screen reader, keyboard navigation) can fully interact with the chatbot.

**Why this priority**: Accessibility is required by constitution (WCAG 2.1 AA compliance).

**Independent Test**: Can be tested with screen reader (NVDA/VoiceOver) and keyboard-only navigation.

**Acceptance Scenarios**:

1. **Given** a screen reader user, **When** chatbot opens, **Then** focus announces "Physical AI Textbook Assistant, chat input field"
2. **Given** keyboard-only navigation, **When** user tabs through interface, **Then** all controls (input, send, close, links) are focusable in logical order
3. **Given** new chatbot response arrives, **When** screen reader is active, **Then** response is announced via ARIA live region

---

### User Story 6 - Mobile Responsive Chat (Priority: P3)

A reader on mobile device (375px+ viewport) can use the chatbot without UI issues.

**Why this priority**: Mobile readership expected; responsive design per spec requirements.

**Independent Test**: Can be tested on 375px, 768px, and 1024px viewports.

**Acceptance Scenarios**:

1. **Given** 375px viewport, **When** chat widget opens, **Then** it expands to near-full-screen modal with visible input
2. **Given** mobile keyboard opens, **When** user types, **Then** input field remains visible above keyboard
3. **Given** long response on mobile, **When** content overflows, **Then** response area scrolls independently

---

### Edge Cases

- **Empty Query**: Display "Please enter a question about the textbook"
- **Very Long Query (>500 chars)**: Truncate with warning "Query shortened to 500 characters"
- **API Rate Limit**: Display "The assistant is busy. Please try again in a few seconds."
- **Network Failure**: Display "Unable to connect. Please check your connection."
- **No Relevant Results**: "I couldn't find information about that in the textbook. Try rephrasing or browse the glossary."
- **Malicious Input (prompt injection)**: System prompt hardened; response limited to book content only
- **Selected Text Too Long (>2000 chars)**: "Please select a shorter passage (max 2000 characters)"

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Chatbot MUST be embedded as a floating widget visible on all `/docs/*` pages
- **FR-002**: Chatbot MUST accept natural language queries up to 500 characters
- **FR-003**: Chatbot MUST use RAG to retrieve relevant textbook chunks before generating responses
- **FR-004**: Chatbot MUST cite source chapter/section for every factual claim
- **FR-005**: Chatbot MUST detect and handle user-selected text as query context
- **FR-006**: Chatbot MUST politely refuse questions outside textbook scope
- **FR-007**: Chatbot MUST maintain conversation history within session (up to 20 turns)
- **FR-008**: Chatbot MUST store conversation logs in Neon Postgres for analytics
- **FR-009**: Chatbot MUST respond within 5 seconds for 95% of queries (p95 latency)
- **FR-010**: Chatbot MUST work without JavaScript disabled (graceful degradation: show link to search)

### Non-Functional Requirements

- **NFR-001**: Qdrant Cloud free tier constraints: 1GB storage, 1M vectors max
- **NFR-002**: Neon Postgres free tier constraints: 512MB storage, 3GB transfer/month
- **NFR-003**: OpenAI API rate limits: 3500 RPM for GPT-4, 1M TPM
- **NFR-004**: WCAG 2.1 AA accessibility compliance
- **NFR-005**: HTTPS-only API communication
- **NFR-006**: No PII storage (conversations stored without user identifiers)

### Key Entities

- **ChatMessage**: User or assistant message with timestamp, role, content, citations[]
- **Conversation**: Session-scoped collection of ChatMessages with session_id
- **TextChunk**: Embedded textbook content with chapter_id, section_id, content, vector_embedding
- **Citation**: Reference to source with chapter, section, url, relevance_score
- **SelectedText**: User-highlighted passage with page_url, start_offset, end_offset, content

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 90% of test queries receive accurate, relevant responses (human evaluation)
- **SC-002**: 100% of responses include at least one valid source citation
- **SC-003**: p95 response latency < 5 seconds
- **SC-004**: 0% of responses answer off-topic questions with fabricated content
- **SC-005**: Chat widget loads within 1 second of page load
- **SC-006**: Mobile usability score > 90 (Lighthouse)
- **SC-007**: Accessibility audit passes with 0 critical issues
- **SC-008**: Conversation history persists correctly for 100% of sessions

---

## API Contract Specifications

### POST /api/chat

**Request**:
```json
{
  "query": "string (max 500 chars)",
  "session_id": "uuid",
  "selected_text": "string | null (max 2000 chars)",
  "page_context": {
    "chapter_id": "string",
    "section_id": "string | null",
    "url": "string"
  }
}
```

**Response**:
```json
{
  "response": "string",
  "citations": [
    {
      "chapter": "string",
      "section": "string",
      "url": "string",
      "relevance_score": "float 0-1"
    }
  ],
  "conversation_id": "uuid",
  "is_off_topic": "boolean"
}
```

**Error Responses**:
- `400`: Invalid request (validation failure)
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: Service unavailable (upstream API failure)

### GET /api/search

**Request**:
```
GET /api/search?q={query}&limit={10}&chapter={chapter_id}
```

**Response**:
```json
{
  "results": [
    {
      "chunk_id": "string",
      "content": "string",
      "chapter": "string",
      "section": "string",
      "score": "float 0-1"
    }
  ],
  "total": "integer"
}
```

### GET /api/health

**Response**:
```json
{
  "status": "healthy | degraded | unhealthy",
  "qdrant": "connected | disconnected",
  "neon": "connected | disconnected",
  "openai": "available | rate_limited | unavailable"
}
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                                  │
│  ┌─────────────┐    ┌──────────────────┐    ┌────────────────────────┐  │
│  │ Type Query  │    │ Select Text      │    │ Click Citation Link    │  │
│  └──────┬──────┘    └────────┬─────────┘    └───────────┬────────────┘  │
│         │                    │                          │               │
└─────────┼────────────────────┼──────────────────────────┼───────────────┘
          │                    │                          │
          ▼                    ▼                          │
┌─────────────────────────────────────────────────────────┼───────────────┐
│                   DOCUSAURUS FRONTEND                   │               │
│  ┌─────────────────────────────────────────────────┐   │               │
│  │              ChatWidget Component                │   │               │
│  │  - Captures query and selected text              │   │               │
│  │  - Manages conversation state                    │   │               │
│  │  - Renders responses with citations              │◄──┘               │
│  │  - Accessibility (ARIA, keyboard nav)            │                   │
│  └───────────────────────┬─────────────────────────┘                   │
│                          │                                              │
└──────────────────────────┼──────────────────────────────────────────────┘
                           │ POST /api/chat
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                      Chat Route Handler                              ││
│  │  1. Validate request                                                 ││
│  │  2. Load conversation history from Neon                              ││
│  │  3. Call RAG pipeline                                                ││
│  │  4. Store response in Neon                                           ││
│  │  5. Return response with citations                                   ││
│  └───────────────────────┬─────────────────────────────────────────────┘│
│                          │                                               │
│  ┌───────────────────────▼─────────────────────────────────────────────┐│
│  │                    RAG Pipeline (LangChain)                          ││
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐ ││
│  │  │ Query Embedding│  │ Context        │  │ Response Generation    │ ││
│  │  │ (OpenAI ada)   │─►│ Retrieval      │─►│ (GPT-4 + System Prompt)│ ││
│  │  └────────────────┘  │ (Qdrant)       │  └────────────────────────┘ ││
│  │                      └────────────────┘                              ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐
│   NEON POSTGRES  │  │   QDRANT CLOUD   │  │      OPENAI API          │
│ - Conversations  │  │ - Text embeddings│  │ - GPT-4 generation       │
│ - Chat history   │  │ - Similarity     │  │ - ada-002 embeddings     │
│ - Usage analytics│  │   search         │  │ - Rate limit management  │
└──────────────────┘  └──────────────────┘  └──────────────────────────┘
```

---

## Security Considerations

### Prompt Injection Prevention

- System prompt hardened with explicit scope constraints
- User input sanitized before RAG pipeline
- Response validation against off-topic content

### API Security

- CORS restricted to textbook domain only
- Rate limiting: 30 requests/minute per session
- Input validation with Pydantic schemas
- No sensitive data in error messages

### Data Privacy

- No user PII collected or stored
- Conversations keyed by anonymous session ID
- Automatic conversation deletion after 30 days
- HTTPS-only communication

---

## Playwright Test-Spec Summary

> **Note**: Test specifications only. No runnable code per constitution.

### Chatbot Core Tests

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| CHAT-001 | Widget visible on /docs/* pages | Floating chat icon present |
| CHAT-002 | Widget opens on click | Chat panel expands with input field |
| CHAT-003 | Submit query via button | Response appears within 5 seconds |
| CHAT-004 | Submit query via Enter key | Response appears within 5 seconds |
| CHAT-005 | Response includes citation | At least one [Chapter X] link present |
| CHAT-006 | Off-topic query handling | Polite refusal message displayed |
| CHAT-007 | Empty query validation | Error message shown, no API call |
| CHAT-008 | Network error handling | Retry message displayed |

### Selected Text Tests

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| SEL-001 | Select text, chat icon appears | Contextual chat trigger visible near selection |
| SEL-002 | Click contextual trigger | Chat opens with selected text as context |
| SEL-003 | "Explain this" with selection | Response explains selected passage |
| SEL-004 | Long selection truncation | Warning displayed, text truncated to 2000 chars |

### Accessibility Tests

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| A11Y-CHAT-001 | Keyboard open/close chat | Escape closes, Enter on icon opens |
| A11Y-CHAT-002 | Screen reader announces responses | ARIA live region triggers announcement |
| A11Y-CHAT-003 | Focus management | Focus moves to input on open, returns on close |
| A11Y-CHAT-004 | Color contrast | All chat UI meets 4.5:1 ratio |

### Mobile Tests

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| MOB-001 | Chat on 375px viewport | Full-screen modal, visible input |
| MOB-002 | Keyboard interaction | Input remains visible above keyboard |
| MOB-003 | Response scrolling | Long responses scroll within container |

---

## Open Questions for Clarification

1. **Rate Limits**: What per-user rate limit is acceptable? (Proposed: 30 requests/minute)
2. **Conversation Retention**: How long should conversations be stored? (Proposed: 30 days)
3. **Fallback Behavior**: If OpenAI API is unavailable, show cached FAQ or disable chat?
4. **Analytics Scope**: What usage metrics should be tracked? (Proposed: query count, topics, latency)
5. **Embedding Model**: OpenAI ada-002 or consider open-source alternatives for cost?

---

**Spec Version**: 1.0.0 | **Author**: Claude Code Agent | **Reviewed**: Pending
