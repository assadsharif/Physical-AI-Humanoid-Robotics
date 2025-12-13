# Tasks: RAG Chatbot for Physical AI Textbook

**Input**: Design documents from `/specs/rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required)
**Phase**: 2 (Follows Phase 1: Docusaurus Site Structure)

**IMPORTANT**: All tasks are HUMAN-EXECUTABLE only. No autonomous agent execution.
Each task includes verification steps for human reviewers.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions
- Each task must be completable in <4 hours

---

## Phase 2.0: Infrastructure Setup (Blocking Prerequisites)

**Purpose**: Provision external services and configure environment before any development.

**CRITICAL**: No Phase 2.1+ work can begin until this phase is complete.

### Service Provisioning

- [ ] T2001 [P] Create Qdrant Cloud account and provision free tier cluster
  - **Verify**: Cluster URL accessible, API key generated
  - **Output**: `QDRANT_URL` and `QDRANT_API_KEY` values

- [ ] T2002 [P] Create Neon Postgres database on free tier
  - **Verify**: Connection string works with psql
  - **Output**: `DATABASE_URL` connection string

- [ ] T2003 [P] Obtain OpenAI API key with GPT-4 and embedding access
  - **Verify**: Test embedding call succeeds
  - **Output**: `OPENAI_API_KEY` value

### Backend Scaffolding

- [ ] T2004 Create backend directory structure per plan.md
  - **Path**: `/backend/`
  - **Verify**: Structure matches plan.md source code section

- [ ] T2005 Initialize Python project with FastAPI dependencies
  - **Path**: `/backend/requirements.txt`
  - **Verify**: `pip install -r requirements.txt` succeeds

- [ ] T2006 Create FastAPI application factory
  - **Path**: `/backend/src/main.py`
  - **Verify**: `uvicorn src.main:app --reload` starts server

- [ ] T2007 Create environment configuration module
  - **Path**: `/backend/src/core/config.py`
  - **Verify**: Config loads from `.env` file correctly

- [ ] T2008 Implement health check endpoint
  - **Path**: `/backend/src/api/routes/health.py`
  - **Verify**: `GET /api/health` returns service status JSON

### Database Setup

- [ ] T2009 Create SQLAlchemy models for conversations
  - **Path**: `/backend/src/models/database.py`
  - **Models**: Conversation, Message, Analytics

- [ ] T2010 Create Alembic migration for initial schema
  - **Path**: `/backend/alembic/versions/`
  - **Verify**: `alembic upgrade head` creates tables in Neon

### Qdrant Setup

- [ ] T2011 Create Qdrant collection initialization script
  - **Path**: `/backend/scripts/setup_qdrant.py`
  - **Collection**: `textbook_chunks` with 1536 dimensions

- [ ] T2012 Run Qdrant setup script and verify collection exists
  - **Verify**: Collection visible in Qdrant Cloud dashboard

**Checkpoint**: All infrastructure ready. Services connected. Health endpoint returns all green.

---

## Phase 2.1: Content Ingestion (US1 Foundation)

**Purpose**: Transform textbook MDX content into searchable vector embeddings.

**Goal**: All 28 chapters indexed in Qdrant with metadata for retrieval.

### MDX Parsing

- [ ] T2101 Create MDX parser module to extract text content
  - **Path**: `/backend/scripts/ingest_content.py`
  - **Input**: `/my-project/docs/**/*.mdx`
  - **Output**: List of (chapter_id, section_id, text, url) tuples

- [ ] T2102 Test MDX parser on Part I chapters (1-4)
  - **Verify**: Text extraction includes headers, paragraphs, excludes JSX components

### Chunking Strategy

- [ ] T2103 Implement text chunking with overlap
  - **Path**: `/backend/scripts/ingest_content.py`
  - **Config**: 500 tokens max, 100 token overlap
  - **Verify**: Chunks maintain semantic coherence

- [ ] T2104 [P] Review chunk quality on sample chapters
  - **Human Review**: Check 20 random chunks for readability and context
  - **Output**: Approved/needs adjustment

### Embedding Generation

- [ ] T2105 Create embedding service wrapper for OpenAI
  - **Path**: `/backend/src/services/embedding_service.py`
  - **Verify**: `embed_text("test")` returns 1536-dim vector

- [ ] T2106 Implement batch embedding with progress tracking
  - **Path**: `/backend/scripts/ingest_content.py`
  - **Verify**: Handles rate limits, shows progress bar

### Vector Upload

- [ ] T2107 Create Qdrant service for vector operations
  - **Path**: `/backend/src/services/qdrant_service.py`
  - **Methods**: `upsert_chunks()`, `search_similar()`

- [ ] T2108 Upload all chapters to Qdrant collection
  - **Verify**: `~500` vectors in collection (check Qdrant dashboard)
  - **Metadata**: chapter_id, section_id, title, url, page_number

- [ ] T2109 Test semantic search with sample queries
  - **Queries**: "What is ZMP?", "ROS2 lifecycle states", "Isaac Sim GPU requirements"
  - **Verify**: Top-5 results are relevant to each query

**Checkpoint**: All content indexed. Search returns relevant results. Human-verified chunk quality.

---

## Phase 2.2: Backend API Development

**Purpose**: Implement RAG-powered chat and search API endpoints.

### User Story 1 - General Book Questions

#### Search Endpoint (US1)

- [ ] T2201 [US1] Create Pydantic schemas for search request/response
  - **Path**: `/backend/src/models/schemas.py`
  - **Verify**: Schema validation works for valid/invalid inputs

- [ ] T2202 [US1] Implement search route handler
  - **Path**: `/backend/src/api/routes/search.py`
  - **Endpoint**: `GET /api/search?q={query}&limit={10}`
  - **Verify**: Returns ranked results with scores

- [ ] T2203 [US1] Add search endpoint tests
  - **Path**: `/backend/tests/integration/test_search_endpoint.py`
  - **Verify**: Tests pass for valid queries, empty queries, no results

#### RAG Pipeline (US1)

- [ ] T2204 [US1] Create system prompt templates
  - **Path**: `/backend/src/core/prompts.py`
  - **Prompts**: SYSTEM_PROMPT, OFF_TOPIC_RESPONSE, NO_RESULTS_RESPONSE
  - **Verify**: Prompts enforce book-scope-only responses

- [ ] T2205 [US1] Create OpenAI service wrapper
  - **Path**: `/backend/src/services/openai_service.py`
  - **Methods**: `generate_response(context, query, history)`
  - **Verify**: API calls succeed, responses are coherent

- [ ] T2206 [US1] Implement RAG service with LangChain
  - **Path**: `/backend/src/services/rag_service.py`
  - **Flow**: Query → Embed → Retrieve → Generate → Format
  - **Verify**: End-to-end RAG produces cited responses

- [ ] T2207 [US1] Create Pydantic schemas for chat request/response
  - **Path**: `/backend/src/models/schemas.py`
  - **Fields**: query, session_id, selected_text, page_context, citations

- [ ] T2208 [US1] Implement chat route handler
  - **Path**: `/backend/src/api/routes/chat.py`
  - **Endpoint**: `POST /api/chat`
  - **Verify**: Returns response with citations array

- [ ] T2209 [US1] Test off-topic query detection
  - **Queries**: "How do I make pizza?", "What's the weather?"
  - **Verify**: Returns polite refusal, `is_off_topic: true`

### User Story 2 - Selected Text Explanation

- [ ] T2210 [US2] Update chat endpoint to handle selected_text context
  - **Path**: `/backend/src/api/routes/chat.py`
  - **Verify**: Selected text included in RAG context

- [ ] T2211 [US2] Create prompt template for text explanation
  - **Path**: `/backend/src/core/prompts.py`
  - **Template**: EXPLAIN_SELECTION_PROMPT
  - **Verify**: Explanations are clear and reference source

- [ ] T2212 [US2] Test selected text explanation flow
  - **Input**: Technical passage + "Explain this"
  - **Verify**: Response explains passage in simpler terms

### User Story 3 - Conversation Context

- [ ] T2213 [US3] Create conversation service for history management
  - **Path**: `/backend/src/services/conversation_service.py`
  - **Methods**: `load_history()`, `save_message()`, `prune_old()`

- [ ] T2214 [US3] Implement conversation persistence to Neon
  - **Verify**: Messages stored with session_id, role, content, timestamp

- [ ] T2215 [US3] Update RAG service to include conversation history
  - **Verify**: Multi-turn conversations maintain context

- [ ] T2216 [US3] Test multi-turn conversation flow
  - **Scenario**: Q1 about topic → Q2 with "it" reference
  - **Verify**: Second response understands context

### Security & Rate Limiting

- [ ] T2217 Implement per-session rate limiting (30 req/min)
  - **Path**: `/backend/src/api/deps.py`
  - **Verify**: 31st request returns 429 status

- [ ] T2218 Add input sanitization for prompt injection prevention
  - **Path**: `/backend/src/api/routes/chat.py`
  - **Verify**: Malicious inputs don't affect system prompt

- [ ] T2219 Configure CORS for textbook domain only
  - **Path**: `/backend/src/main.py`
  - **Verify**: Cross-origin requests from other domains rejected

**Checkpoint**: All API endpoints functional. RAG generates accurate responses. Security measures in place.

---

## Phase 2.3: Frontend Chat Widget

**Purpose**: Build React component for chat interactions embedded in Docusaurus.

### User Story 1 & 2 - Core Chat UI

- [ ] T2301 [P] [US1] Create ChatWidget directory structure
  - **Path**: `/my-project/src/components/ChatWidget/`
  - **Files**: ChatWidget.tsx, index.ts, ChatWidget.module.css

- [ ] T2302 [US1] Implement ChatWidget container component
  - **Path**: `/my-project/src/components/ChatWidget/ChatWidget.tsx`
  - **State**: isOpen, messages[], inputValue, isLoading
  - **Verify**: Widget opens/closes, input accepts text

- [ ] T2303 [US1] Implement MessageList component
  - **Path**: `/my-project/src/components/ChatWidget/MessageList.tsx`
  - **Verify**: User and assistant messages render distinctly

- [ ] T2304 [US1] Implement ChatInput component
  - **Path**: `/my-project/src/components/ChatWidget/ChatInput.tsx`
  - **Verify**: Submit via button and Enter key

- [ ] T2305 [US1] Implement Citation component
  - **Path**: `/my-project/src/components/ChatWidget/Citation.tsx`
  - **Verify**: Citations render as clickable links to chapters

- [ ] T2306 [US1] Connect ChatWidget to backend API
  - **Verify**: Queries sent, responses displayed with citations

- [ ] T2307 [US2] Implement SelectionHandler component
  - **Path**: `/my-project/src/components/ChatWidget/SelectionHandler.tsx`
  - **Verify**: Text selection triggers contextual chat icon

- [ ] T2308 [US2] Integrate selection context into chat flow
  - **Verify**: Selected text appears as context in chat

### User Story 4 - Source Navigation

- [ ] T2309 [US4] Ensure all citations are clickable links
  - **Verify**: Clicking citation navigates to correct chapter/section

- [ ] T2310 [US4] Add visual distinction for cited sources
  - **Verify**: Citations have consistent styling across responses

### User Story 5 - Accessibility

- [ ] T2311 [US5] Add ARIA labels to all interactive elements
  - **Elements**: Chat button, input, send button, close button
  - **Verify**: Screen reader announces all elements correctly

- [ ] T2312 [US5] Implement keyboard navigation
  - **Keys**: Escape closes, Tab moves focus, Enter submits
  - **Verify**: Full interaction possible without mouse

- [ ] T2313 [US5] Add ARIA live region for new messages
  - **Verify**: Screen reader announces new responses automatically

- [ ] T2314 [US5] Implement focus management
  - **Verify**: Focus moves to input on open, returns to trigger on close

- [ ] T2315 [US5] Verify color contrast meets WCAG AA
  - **Tool**: axe DevTools or Lighthouse
  - **Verify**: All text passes 4.5:1 contrast ratio

### User Story 6 - Mobile Responsive

- [ ] T2316 [US6] Create mobile-specific styles (375px breakpoint)
  - **Path**: `/my-project/src/components/ChatWidget/ChatWidget.module.css`
  - **Verify**: Full-screen modal on mobile viewport

- [ ] T2317 [US6] Test keyboard interaction on mobile
  - **Verify**: Input remains visible when virtual keyboard opens

- [ ] T2318 [US6] Test response scrolling on mobile
  - **Verify**: Long responses scroll within container

### Docusaurus Integration

- [ ] T2319 Create Root wrapper to provide ChatWidget globally
  - **Path**: `/my-project/src/theme/Root.tsx`
  - **Verify**: ChatWidget appears on all /docs/* pages

- [ ] T2320 Add environment variables to Docusaurus config
  - **Path**: `/my-project/docusaurus.config.ts`
  - **Variables**: REACT_APP_API_URL
  - **Verify**: Frontend can call backend API

- [ ] T2321 Build and verify production bundle
  - **Command**: `npm run build`
  - **Verify**: ChatWidget included in production build

**Checkpoint**: Chat widget fully functional. Accessibility audit passed. Mobile responsive.

---

## Phase 2.4: Testing & QA

**Purpose**: Comprehensive testing to verify all acceptance criteria.

### Backend Tests

- [ ] T2401 [P] Write unit tests for embedding service
  - **Path**: `/backend/tests/unit/test_embedding_service.py`
  - **Coverage**: embed_text(), batch_embed()

- [ ] T2402 [P] Write unit tests for RAG service
  - **Path**: `/backend/tests/unit/test_rag_service.py`
  - **Coverage**: retrieve(), generate(), format_response()

- [ ] T2403 [P] Write unit tests for conversation service
  - **Path**: `/backend/tests/unit/test_conversation_service.py`
  - **Coverage**: load_history(), save_message(), prune_old()

- [ ] T2404 Write integration tests for chat endpoint
  - **Path**: `/backend/tests/integration/test_chat_endpoint.py`
  - **Scenarios**: Valid query, empty query, off-topic, rate limit

- [ ] T2405 Run pytest and verify >80% coverage
  - **Command**: `pytest --cov=src`
  - **Verify**: Coverage report shows >80%

### Frontend Tests

- [ ] T2406 [P] Write Vitest tests for ChatWidget
  - **Path**: `/my-project/src/components/ChatWidget/__tests__/`
  - **Coverage**: Open/close, submit, render messages

- [ ] T2407 [P] Write Vitest tests for SelectionHandler
  - **Coverage**: Selection detection, context capture

### E2E Playwright Tests

- [ ] T2408 Create Playwright test for basic chat flow
  - **Path**: `/e2e/chatbot/chat-basic.spec.ts`
  - **Tests**: CHAT-001 through CHAT-008 from spec

- [ ] T2409 Create Playwright test for selected text flow
  - **Path**: `/e2e/chatbot/chat-selection.spec.ts`
  - **Tests**: SEL-001 through SEL-004 from spec

- [ ] T2410 Create Playwright test for accessibility
  - **Path**: `/e2e/chatbot/chat-accessibility.spec.ts`
  - **Tests**: A11Y-CHAT-001 through A11Y-CHAT-004 from spec

- [ ] T2411 Create Playwright test for mobile responsiveness
  - **Path**: `/e2e/chatbot/chat-mobile.spec.ts`
  - **Tests**: MOB-001 through MOB-003 from spec

- [ ] T2412 Run full Playwright test suite
  - **Command**: `npx playwright test`
  - **Verify**: All tests pass

### Quality Audits

- [ ] T2413 Run Lighthouse accessibility audit
  - **Target**: >90 accessibility score
  - **Verify**: 0 critical issues

- [ ] T2414 Run Lighthouse performance audit
  - **Target**: >90 performance score
  - **Verify**: Chat widget doesn't impact page load significantly

- [ ] T2415 Manual RAG quality review (10 sample queries)
  - **Human Review**: Evaluate accuracy, relevance, citation correctness
  - **Output**: Quality report with pass/fail per query

**Checkpoint**: All tests pass. Coverage >80%. Quality audits pass.

---

## Phase 2.5: Deployment & Launch

**Purpose**: Deploy chatbot to production and enable for all users.

### Backend Deployment

- [ ] T2501 Create Dockerfile for FastAPI backend
  - **Path**: `/backend/Dockerfile`
  - **Verify**: `docker build` succeeds

- [ ] T2502 Deploy backend to hosting platform (Railway/Render/Fly.io)
  - **Verify**: Health endpoint accessible at production URL

- [ ] T2503 Configure production environment variables
  - **Variables**: QDRANT_URL, DATABASE_URL, OPENAI_API_KEY
  - **Verify**: All services connected in production

### Frontend Deployment

- [ ] T2504 Update frontend to use production API URL
  - **Path**: `/my-project/docusaurus.config.ts`
  - **Verify**: API calls route to production backend

- [ ] T2505 Build and deploy Docusaurus with ChatWidget
  - **Command**: `npm run build && npm run deploy`
  - **Verify**: Chat widget visible on production site

### Monitoring & Observability

- [ ] T2506 Configure error tracking (Sentry or similar)
  - **Verify**: Test error captured and reported

- [ ] T2507 Create latency monitoring dashboard
  - **Metrics**: p50, p95, p99 response times
  - **Verify**: Dashboard shows real-time metrics

- [ ] T2508 Set up alerting for service degradation
  - **Alerts**: Error rate >5%, latency p95 >10s
  - **Verify**: Test alert fires correctly

### Documentation

- [ ] T2509 Document API endpoints in OpenAPI spec
  - **Path**: `/backend/docs/openapi.yaml` or auto-generated
  - **Verify**: Swagger UI accessible

- [ ] T2510 Create operational runbook
  - **Path**: `/docs/runbook-chatbot.md`
  - **Contents**: Common issues, troubleshooting, scaling

- [ ] T2511 Update project README with chatbot information
  - **Verify**: Setup instructions accurate

### Launch

- [ ] T2512 Conduct final pre-launch checklist review
  - **Checklist**: All tests pass, monitoring active, docs complete
  - **Verify**: Human sign-off from project lead

- [ ] T2513 Enable chatbot for all users (feature flag or full deploy)
  - **Verify**: Chat widget functional for external users

- [ ] T2514 Create PHR for Phase 2 completion
  - **Path**: `/history/prompts/rag-chatbot/`

**Checkpoint**: Chatbot live in production. Monitoring active. Launch complete.

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 2.0 (Infrastructure) ─────► BLOCKS all other phases
        │
        ▼
Phase 2.1 (Ingestion) ──────────► Required for search/chat
        │
        ▼
Phase 2.2 (Backend API) ────────► Required for frontend
        │
        ▼
Phase 2.3 (Frontend) ───────────► Required for E2E tests
        │
        ▼
Phase 2.4 (Testing) ────────────► Required for deployment
        │
        ▼
Phase 2.5 (Deployment)
```

### Parallel Opportunities

**Within Phase 2.0**:
- T2001, T2002, T2003 can run in parallel (service provisioning)

**Within Phase 2.2**:
- US1 search endpoint can proceed while ingestion completes minimum content

**Within Phase 2.3**:
- Component development (T2301-T2310) can proceed once API is available

**Within Phase 2.4**:
- Backend unit tests (T2401-T2403) can run in parallel
- Frontend tests (T2406-T2407) can run in parallel

---

## Implementation Strategy

### MVP First Approach

1. Complete Phase 2.0: Infrastructure (**blocking**)
2. Complete Phase 2.1: Ingest Part I chapters minimum
3. Complete Phase 2.2: Search + Chat endpoints (US1 only)
4. Complete Phase 2.3: Basic ChatWidget (no selection, basic A11y)
5. **VALIDATE MVP**: Test basic Q&A flow end-to-end
6. Iterate: Add US2-US6 features incrementally

### Risk Mitigation Checkpoints

| After Phase | Validate | Fallback if Fail |
|-------------|----------|------------------|
| 2.0 | All services connected | Debug connectivity, check credentials |
| 2.1 | Search returns relevant results | Adjust chunking, re-index |
| 2.2 | RAG generates accurate responses | Tune prompts, adjust retrieval k |
| 2.3 | Widget works on desktop | Debug React, check API connection |
| 2.4 | All tests pass | Fix failures, adjust acceptance criteria |

---

## Notes

- All tasks are HUMAN-EXECUTABLE - agents do not execute
- Each task should take <4 hours for experienced developer
- Mark tasks complete only after verification steps pass
- Create PHR after each phase completion
- Suggest ADR for any significant deviations from plan

---

**Tasks Version**: 1.0.0 | **Author**: Claude Code Agent | **Reviewed**: Pending
