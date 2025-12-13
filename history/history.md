# Project History

This document tracks the development history of the Physical AI & Humanoid Robotics textbook project.

---

## Project Timeline

```
2025-12-12 ─────────────────────────────────────────────────────────────────►
    │
    ├── Phase 1: Docusaurus Site Structure
    │   ├── Constitution ratified (v1.0.0)
    │   ├── Textbook specification created
    │   ├── Implementation plan approved
    │   └── Site structure milestone (M1.1) executed
    │
    └── Phase 2: RAG Chatbot Specification (CURRENT)
        ├── RAG chatbot spec created
        ├── Phase 2 plan created
        ├── Task checklist created
        ├── Agents updated for chatbot system
        └── Skills registry created
```

---

## Phase 1: Docusaurus Site (2025-12-12)

### Milestones Completed

| Milestone | Status | Date | Notes |
|-----------|--------|------|-------|
| Constitution Ratification | Complete | 2025-12-12 | v1.0.0 ratified |
| Feature Specification | Complete | 2025-12-12 | 28-chapter textbook structure |
| Implementation Plan | Complete | 2025-12-12 | 4-module architecture defined |
| M1.1 Site Structure | Complete | 2025-12-12 | Docusaurus initialized, navigation configured |

### Key Decisions (Phase 1)

| Decision | Outcome | Rationale |
|----------|---------|-----------|
| Static Site Generator | Docusaurus v3 | MDX support, React components, search built-in |
| Content Format | MDX | Allows interactive components in markdown |
| Testing Framework | Playwright | E2E testing with accessibility support |

### Artifacts Created

| Artifact | Path | Description |
|----------|------|-------------|
| Constitution | `.specify/memory/constitution.md` | Project principles and constraints |
| Textbook Spec | `specs/physical-ai-textbook/spec.md` | Feature specification |
| Textbook Plan | `specs/physical-ai-textbook/plan.md` | Implementation plan |
| Site Structure Task | `specs/physical-ai-textbook/tasks/m1-1-site-structure.task.md` | Task checklist |
| Implementation Narrative | `specs/physical-ai-textbook/implement/m1-docusaurus-site.implement.md` | Conceptual narrative |

### PHR Records (Phase 1)

| ID | Title | Stage | Path |
|----|-------|-------|------|
| 001 | Physical AI Robotics Constitution | constitution | `history/prompts/constitution/` |
| 001 | Textbook Specification Draft | spec | `history/prompts/physical-ai-textbook/` |
| 002 | Project Plan Architecture | plan | `history/prompts/physical-ai-textbook/` |
| 003 | Site Structure Task | tasks | `history/prompts/physical-ai-textbook/` |
| 004 | Docusaurus Implementation Narrative | misc | `history/prompts/physical-ai-textbook/` |
| 005 | M1-1 Site Structure Execution | green | `history/prompts/physical-ai-textbook/` |

---

## Phase 2: RAG Chatbot (2025-12-12 - Present)

### Overview

Phase 2 adds an embedded RAG chatbot to the Docusaurus textbook, enabling readers to ask questions about content and get contextual explanations of selected text.

### Milestones Defined

| Milestone | Status | Target | Description |
|-----------|--------|--------|-------------|
| M2.0.1 Qdrant Setup | Pending | TBD | Provision Qdrant Cloud free tier |
| M2.0.2 Neon Setup | Pending | TBD | Provision Neon Postgres free tier |
| M2.0.3 OpenAI Config | Pending | TBD | Configure API keys |
| M2.0.4 Backend Scaffold | Pending | TBD | FastAPI application structure |
| M2.1.1 MDX Parser | Pending | TBD | Parse textbook content |
| M2.1.2 Chunking | Pending | TBD | Implement content chunking |
| M2.1.3 Embedding | Pending | TBD | Generate vector embeddings |
| M2.1.4 Qdrant Upload | Pending | TBD | Index all content |
| M2.2.1 Search Endpoint | Pending | TBD | GET /api/search |
| M2.2.2 RAG Pipeline | Pending | TBD | LangChain orchestration |
| M2.2.3 Chat Endpoint | Pending | TBD | POST /api/chat |
| M2.2.4 Conversation DB | Pending | TBD | Neon persistence |
| M2.3.1 ChatWidget | Pending | TBD | React component |
| M2.3.4 Accessibility | Pending | TBD | WCAG compliance |
| M2.4.4 E2E Tests | Pending | TBD | Playwright tests |
| M2.5.5 Launch | Pending | TBD | Production deployment |

### Key Decisions (Phase 2)

| Decision | Outcome | Status |
|----------|---------|--------|
| Vector Database | Qdrant Cloud Free Tier | Pending ADR |
| Relational Database | Neon Serverless Postgres | Pending ADR |
| Embedding Model | OpenAI ada-002 | Pending ADR |
| LLM | OpenAI GPT-4 | Pending ADR |
| Chunking Strategy | 500 tokens, 100 overlap | Pending ADR |
| Rate Limiting | 30 req/min/session | Pending ADR |

### Artifacts Created (Phase 2 Specification)

| Artifact | Path | Description |
|----------|------|-------------|
| RAG Chatbot Spec | `specs/rag-chatbot/spec.md` | Feature specification |
| RAG Chatbot Plan | `specs/rag-chatbot/plan.md` | Implementation plan |
| RAG Chatbot Tasks | `specs/rag-chatbot/tasks.md` | Task checklist |
| Agents (v2.0.0) | `agents.md` | Updated with chatbot agents |
| Skills Registry | `history/skills.md` | Required skills catalog |

### Technology Stack (Phase 2)

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React (Docusaurus) | ChatWidget component |
| Backend | FastAPI | API endpoints |
| Orchestration | LangChain | RAG pipeline |
| Vector Store | Qdrant Cloud | Similarity search |
| Database | Neon Postgres | Conversation history |
| LLM | OpenAI GPT-4 | Response generation |
| Embeddings | OpenAI ada-002 | Vector embeddings |

### Agent Roster (Phase 2)

| Agent | Role | Surface |
|-------|------|---------|
| RAG Orchestration Agent | Coordinate RAG pipeline | FastAPI |
| Embedding Agent | Generate embeddings | EmbeddingService |
| Retrieval Agent | Search vectors | QdrantService |
| Generation Agent | Generate responses | OpenAIService |
| Conversation Agent | Manage history | ConversationService |
| Content Ingestion Agent | Index content | Python script |

---

## Upcoming Milestones

### Next Actions (Blocking)

1. **Human Approval**: Phase 2 spec, plan, and tasks require human review
2. **ADR Creation**: Architectural decisions need documentation
3. **Infrastructure Setup**: Cloud services must be provisioned

### Phase 2 Critical Path

```
Spec Review → Infrastructure Setup → Content Ingestion → Backend API → Frontend Widget → Testing → Launch
```

---

## Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2025-12-12 | 1.0.0 | Initial Phase 1 setup | Claude Code Agent |
| 2025-12-12 | 2.0.0 | Phase 2 RAG chatbot specification | Claude Code Agent |

---

## Open Items

### Pending ADRs

1. `embedding-model-selection` - OpenAI ada-002 vs alternatives
2. `chunking-strategy` - Fixed vs semantic chunking
3. `conversation-retention` - 30-day vs indefinite storage
4. `rate-limiting-strategy` - Per-session vs per-IP

### Open Questions

1. OpenAI API budget allocation for Phase 2
2. Qdrant free tier sufficiency for ~500 vectors
3. Neon free tier sufficiency for conversation storage
4. Mobile-first vs desktop-first chat widget design
5. Fallback behavior when OpenAI API unavailable

---

## Project Metrics

### Phase 1 Metrics

| Metric | Value |
|--------|-------|
| Specification documents | 4 |
| PHR records created | 5 |
| Chapters planned | 28 |
| Glossary terms planned | 200+ |

### Phase 2 Metrics (Planned)

| Metric | Target |
|--------|--------|
| API endpoints | 3 |
| Vector embeddings | ~500 |
| Frontend components | 6 |
| Playwright tests | 20+ |
| p95 response latency | <5s |

---

**History Version**: 1.0.0 | **Last Updated**: 2025-12-12
