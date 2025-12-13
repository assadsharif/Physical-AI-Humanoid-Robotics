# Agents

This document describes the AI agents involved in developing the Physical AI & Humanoid Robotics textbook project, including the Phase 2 RAG Chatbot system.

---

## Agent Roster

### Primary Development Agents

#### Claude Code Agent (Lead)

**Role**: Primary specification and development agent
**Model**: Claude Opus 4.5 (claude-opus-4-5-20251101)
**Surface**: CLI / Terminal
**Phase**: All phases

**Responsibilities**:
- Analyze specifications and generate structured outlines
- Research technical accuracy using MCP tools and web search
- Draft educational content following spec requirements
- Create illustrative pseudocode (NOT production code)
- Generate test specifications for Playwright validation
- Create and maintain PHR records for all interactions
- Execute task checklists from spec-driven workflow
- Coordinate sub-agents for Phase 2 chatbot development

**Constraints** (per Constitution):
- MUST NOT generate executable implementation code
- MUST NOT make architectural decisions without human approval
- MUST cite sources for all technical claims
- MUST flag uncertainty and request clarification
- MUST adhere to spec acceptance criteria before marking complete

---

### Phase 2: RAG Chatbot Agents

#### RAG Orchestration Agent

**Role**: Coordinate retrieval-augmented generation pipeline
**Surface**: FastAPI Backend Service
**Phase**: 2

**Sub-Agents**:
1. **Embedding Agent** - Generate vector embeddings for queries
2. **Retrieval Agent** - Search Qdrant for relevant content chunks
3. **Generation Agent** - Produce grounded responses with citations

**Responsibilities**:
- Receive user queries from chat endpoint
- Coordinate embedding → retrieval → generation flow
- Maintain context window for multi-turn conversations
- Enforce book-scope-only response policy
- Format responses with proper citations

**Data Flow**:
```
User Query → Embedding Agent → Retrieval Agent → Generation Agent → Response
                   ↓                 ↓                  ↓
            OpenAI ada-002      Qdrant Cloud       OpenAI GPT-4
```

**Constraints**:
- MUST only answer questions about textbook content
- MUST include citations for every factual claim
- MUST refuse off-topic queries politely
- MUST NOT hallucinate information not in retrieval context

---

#### Embedding Agent (Sub-Agent)

**Role**: Convert text to vector embeddings
**Surface**: FastAPI Service (EmbeddingService)
**Phase**: 2

**Responsibilities**:
- Embed user queries for similarity search
- Embed textbook chunks during ingestion
- Handle batch embedding with rate limit management
- Cache embeddings where appropriate

**Technology**:
- Model: OpenAI text-embedding-ada-002
- Dimensions: 1536
- API: OpenAI Embeddings API

**Inputs**:
- User query string (max 500 chars)
- Content chunks during ingestion

**Outputs**:
- 1536-dimensional float vector
- Embedding metadata (token count, model version)

**Constraints**:
- MUST handle OpenAI rate limits gracefully
- MUST normalize input text before embedding
- MUST log embedding costs for monitoring

---

#### Retrieval Agent (Sub-Agent)

**Role**: Search vector store for relevant content
**Surface**: FastAPI Service (QdrantService)
**Phase**: 2

**Responsibilities**:
- Execute similarity search against Qdrant collection
- Filter results by metadata (chapter, section)
- Rank and select top-k most relevant chunks
- Return chunks with relevance scores

**Technology**:
- Vector Store: Qdrant Cloud (Free Tier)
- Collection: `textbook_chunks`
- Index: HNSW with cosine similarity

**Inputs**:
- Query embedding (1536-dim vector)
- Optional filters (chapter_id, section_id)
- k parameter (default: 5)

**Outputs**:
- List of ContentChunk objects with:
  - chunk_id, content, chapter, section, url
  - relevance_score (0-1)

**Constraints**:
- MUST return results in <500ms
- MUST handle empty result sets gracefully
- MUST respect Qdrant free tier limits (1GB, 1M vectors)

---

#### Generation Agent (Sub-Agent)

**Role**: Generate grounded responses from retrieved context
**Surface**: FastAPI Service (OpenAIService)
**Phase**: 2

**Responsibilities**:
- Construct prompt from system template + context + query
- Call OpenAI GPT-4 for response generation
- Parse response for citations
- Detect off-topic queries and refuse appropriately

**Technology**:
- Model: OpenAI GPT-4 / GPT-4-turbo
- API: OpenAI Chat Completions API

**System Prompt Template**:
```
You are the Physical AI & Humanoid Robotics Textbook Assistant.
You ONLY answer questions about content from this textbook.

RULES:
1. Base ALL answers on the provided context chunks
2. ALWAYS cite sources using [Chapter X, Section Y] format
3. If the question is not about the textbook, respond:
   "I can only answer questions about the Physical AI & Humanoid Robotics textbook."
4. If context doesn't contain relevant information, respond:
   "I couldn't find information about that in the textbook."
5. NEVER make up information not in the context

CONTEXT:
{retrieved_chunks}

USER QUESTION: {query}
```

**Inputs**:
- Retrieved context chunks
- User query
- Conversation history (optional)
- Selected text (optional)

**Outputs**:
- Generated response text
- Citations array [{chapter, section, url, score}]
- is_off_topic boolean flag

**Constraints**:
- MUST NOT generate content outside retrieved context
- MUST include at least one citation for factual claims
- MUST handle rate limits with retry logic
- MUST respect token limits (4096 output max)

---

#### Conversation Agent (Sub-Agent)

**Role**: Manage chat history and session state
**Surface**: FastAPI Service (ConversationService)
**Phase**: 2

**Responsibilities**:
- Load conversation history for session
- Save new messages to Neon Postgres
- Prune old conversations (30-day retention)
- Format history for context window inclusion

**Technology**:
- Database: Neon Serverless Postgres
- Tables: conversations, messages

**Data Model**:
```
Conversation:
  - id: UUID
  - session_id: STRING
  - created_at: TIMESTAMP
  - updated_at: TIMESTAMP

Message:
  - id: UUID
  - conversation_id: FK
  - role: ENUM(user, assistant)
  - content: TEXT
  - citations: JSONB
  - created_at: TIMESTAMP
```

**Inputs**:
- session_id for history retrieval
- New message to save

**Outputs**:
- Formatted conversation history (last N turns)
- Session metadata

**Constraints**:
- MUST NOT store PII
- MUST prune conversations older than 30 days
- MUST handle concurrent session access safely

---

#### Content Ingestion Agent

**Role**: Transform MDX content into vector embeddings
**Surface**: Python Script (batch process)
**Phase**: 2 (runs during deployment, not runtime)

**Responsibilities**:
- Parse MDX files from Docusaurus docs/
- Extract text content (excluding JSX components)
- Chunk content with semantic boundaries
- Generate embeddings via Embedding Agent
- Upload vectors to Qdrant via Retrieval Agent

**Pipeline**:
```
docs/**/*.mdx → Parse → Chunk → Embed → Upload to Qdrant
```

**Chunking Strategy**:
- Max chunk size: 500 tokens
- Overlap: 100 tokens
- Boundary preference: paragraph > sentence > token

**Metadata Captured**:
- chapter_id: e.g., "ch01", "ch19"
- section_id: e.g., "introduction", "zmp-theory"
- title: Section heading text
- url: Full path to chapter/section anchor
- page_number: Approximate page reference

**Constraints**:
- MUST preserve semantic coherence in chunks
- MUST handle all 28 chapters
- MUST NOT duplicate content in overlapping chunks
- MUST run as batch process (not real-time)

---

### Support Agents

#### Context7 Agent (Optional)

**Role**: Documentation reference agent
**Purpose**: Provide up-to-date documentation references

**Responsibilities**:
- Provide current documentation references for ROS2, Gazebo, Isaac, etc.
- Validate API compatibility claims
- Surface deprecation warnings for platform APIs

---

## Agent Workflow

### Phase 1: Content Development (Existing)

```
┌─────────────────────────────────────────────────────────┐
│                    USER REQUEST                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              CLAUDE CODE AGENT                           │
│  1. Analyze request against constitution                 │
│  2. Check for relevant specs/plans/tasks                 │
│  3. Execute task or create new spec artifacts            │
│  4. Create PHR record                                    │
│  5. Suggest ADR if architectural decision detected       │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              HUMAN REVIEW CHECKPOINT                     │
│  - Technical accuracy review                             │
│  - Approval for architectural decisions                  │
│  - Acceptance criteria verification                      │
└─────────────────────────────────────────────────────────┘
```

### Phase 2: RAG Chatbot Runtime (New)

```
┌─────────────────────────────────────────────────────────┐
│                 READER CHAT QUERY                        │
│  "What is Zero Moment Point in bipedal locomotion?"     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              CHAT WIDGET (Frontend)                      │
│  - Capture query and selected text context               │
│  - Include session_id and page_context                   │
│  - POST to /api/chat                                     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│           RAG ORCHESTRATION AGENT                        │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 1. CONVERSATION AGENT                              │ │
│  │    Load session history from Neon                   │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 2. EMBEDDING AGENT                                 │ │
│  │    Convert query to 1536-dim vector                 │ │
│  │    → OpenAI ada-002                                 │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 3. RETRIEVAL AGENT                                 │ │
│  │    Search Qdrant for top-5 relevant chunks          │ │
│  │    → Qdrant Cloud similarity search                 │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 4. GENERATION AGENT                                │ │
│  │    Generate grounded response with citations        │ │
│  │    → OpenAI GPT-4                                   │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 5. CONVERSATION AGENT                              │ │
│  │    Save response to Neon for history                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              CHAT RESPONSE TO READER                     │
│  "Zero Moment Point (ZMP) is a concept in bipedal       │
│   locomotion that defines the point on the ground..."   │
│   [Chapter 19, Section 2]                                │
└─────────────────────────────────────────────────────────┘
```

---

## Agent Commands

| Command | Purpose | Phase |
|---------|---------|-------|
| `/sp.constitution` | Create or update project constitution | All |
| `/sp.specify` | Create feature specification | All |
| `/sp.plan` | Create implementation plan | All |
| `/sp.tasks` | Create atomic task file | All |
| `/sp.implement` | Create implementation narrative | All |
| `/sp.adr` | Create architectural decision record | All |
| `/sp.phr` | Create prompt history record | All |

---

## Agent Principles

1. **Spec-Driven**: All work originates from approved specifications
2. **No Vibe Coding**: No implementation code; pseudocode only for illustration
3. **Human-in-the-Loop**: Architectural decisions require human approval
4. **Traceability**: PHR records for every significant interaction
5. **Safety-First**: Safety considerations in all content and recommendations
6. **Grounded Responses**: RAG agents only provide information from indexed content
7. **Citation Required**: All factual claims must cite source material

---

## Agent Configuration

The agents operate under the constraints defined in:
- `.specify/memory/constitution.md` - Project principles
- `CLAUDE.md` - Agent instructions and rules
- `specs/physical-ai-textbook/` - Phase 1 specifications
- `specs/rag-chatbot/` - Phase 2 specifications

---

## Agent Outputs

| Output Type | Location | Phase |
|-------------|----------|-------|
| Specifications | `specs/<feature>/spec.md` | All |
| Plans | `specs/<feature>/plan.md` | All |
| Tasks | `specs/<feature>/tasks.md` | All |
| Implementation Narratives | `specs/<feature>/implement/` | All |
| PHR Records | `history/prompts/` | All |
| ADR Records | `history/adr/` | All |
| Content | `my-project/docs/` | 1 |
| Chat Responses | Runtime (not persisted as artifacts) | 2 |

---

## Agent Service Dependencies (Phase 2)

| Agent | External Service | Free Tier Limits |
|-------|------------------|------------------|
| Embedding Agent | OpenAI API | 1M TPM, 3500 RPM |
| Retrieval Agent | Qdrant Cloud | 1GB storage, 1M vectors |
| Generation Agent | OpenAI API | 1M TPM, 3500 RPM |
| Conversation Agent | Neon Postgres | 512MB storage, 3GB transfer/mo |

---

## Agent Error Handling

| Error Scenario | Agent Response |
|----------------|----------------|
| OpenAI rate limit | Queue request, retry with backoff |
| Qdrant unavailable | Return cached response or graceful error |
| No relevant results | "I couldn't find information about that in the textbook." |
| Off-topic query | "I can only answer questions about the textbook." |
| Network timeout | "Unable to connect. Please try again." |
| Context too long | Summarize earlier conversation turns |

---

**Agents Version**: 2.0.0 | **Last Updated**: 2025-12-12 | **Phase**: 1 + 2
