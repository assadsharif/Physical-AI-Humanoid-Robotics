# Skills Registry

This document catalogs the technical skills required for the Physical AI & Humanoid Robotics textbook project across all phases.

---

## Overview

| Phase | Focus Area | Primary Skills |
|-------|------------|----------------|
| 1 | Docusaurus Site | React, TypeScript, MDX, CSS |
| 2 | RAG Chatbot | Python, FastAPI, LangChain, OpenAI, Vector DBs |

---

## Phase 1: Docusaurus Site Skills

### Frontend Development

#### SK-F001: React Component Development
**Level**: Intermediate
**Required For**: Custom components (Quiz, Glossary, SafetyCallout)

**Competencies**:
- Functional components with hooks (useState, useEffect)
- Props and TypeScript interfaces
- Component composition patterns
- CSS Modules for scoped styling

**Verification**: Can create a reusable component with props, state, and styling

---

#### SK-F002: TypeScript Proficiency
**Level**: Intermediate
**Required For**: All frontend code

**Competencies**:
- Type annotations and interfaces
- Generic types
- Union and intersection types
- Type guards and assertions

**Verification**: Can type a complex React component with proper generics

---

#### SK-F003: MDX Authoring
**Level**: Basic
**Required For**: Textbook content creation

**Competencies**:
- Markdown syntax (headings, lists, links, code blocks)
- JSX component embedding in markdown
- Frontmatter configuration
- Import statements in MDX

**Verification**: Can create an MDX file with custom components and frontmatter

---

#### SK-F004: Docusaurus Configuration
**Level**: Intermediate
**Required For**: Site setup and customization

**Competencies**:
- docusaurus.config.ts structure
- Sidebars configuration
- Theme customization
- Plugin configuration

**Verification**: Can configure navigation, add plugins, and customize theme

---

#### SK-F005: CSS/Styling
**Level**: Intermediate
**Required For**: Custom component styling

**Competencies**:
- CSS Modules syntax
- Flexbox and Grid layouts
- Responsive design (media queries)
- CSS variables for theming

**Verification**: Can create responsive layouts that work 375px-1440px

---

### Testing

#### SK-T001: Playwright E2E Testing
**Level**: Intermediate
**Required For**: Acceptance test execution

**Competencies**:
- Test file structure and assertions
- Selectors and locators
- Page object patterns
- Accessibility testing with axe

**Verification**: Can write and run E2E tests for navigation and content

---

### Content

#### SK-C001: Technical Writing
**Level**: Advanced
**Required For**: Textbook content creation

**Competencies**:
- Educational content structure
- Technical accuracy verification
- Citation and reference management
- Accessibility in documentation

**Verification**: Can write a technically accurate chapter with proper structure

---

## Phase 2: RAG Chatbot Skills

### Backend Development

#### SK-B001: Python Proficiency
**Level**: Intermediate
**Required For**: All backend code

**Competencies**:
- Python 3.11+ syntax and features
- Async/await patterns
- Type hints (PEP 484, 585)
- Virtual environments and dependency management

**Verification**: Can write async Python code with proper typing

---

#### SK-B002: FastAPI Development
**Level**: Intermediate
**Required For**: API endpoint implementation

**Competencies**:
- Route handlers with path/query parameters
- Pydantic models for request/response validation
- Dependency injection
- Middleware and CORS configuration
- OpenAPI documentation

**Verification**: Can create a REST API with validation, docs, and error handling

---

#### SK-B003: LangChain RAG Patterns
**Level**: Intermediate
**Required For**: RAG pipeline implementation

**Competencies**:
- Chain composition
- Document loaders and text splitters
- Embedding models integration
- Retriever patterns
- Prompt templates

**Verification**: Can build a RAG pipeline that retrieves and generates responses

---

#### SK-B004: OpenAI API Integration
**Level**: Basic
**Required For**: Embedding and generation

**Competencies**:
- Chat completions API
- Embeddings API
- Rate limit handling
- Token counting and management

**Verification**: Can call OpenAI APIs with proper error handling

---

### Data Engineering

#### SK-D001: Vector Database Operations
**Level**: Intermediate
**Required For**: Qdrant integration

**Competencies**:
- Vector similarity concepts (cosine, dot product)
- Collection and index management
- Metadata filtering
- Batch upsert operations

**Verification**: Can create, populate, and query a vector collection

---

#### SK-D002: PostgreSQL Proficiency
**Level**: Basic
**Required For**: Conversation storage

**Competencies**:
- SQL fundamentals (CRUD operations)
- Schema design
- Migrations with Alembic
- Connection pooling (Neon specifics)

**Verification**: Can design schema and write migrations for conversation storage

---

#### SK-D003: Content Chunking Strategies
**Level**: Intermediate
**Required For**: Content ingestion pipeline

**Competencies**:
- Token counting for LLMs
- Semantic vs fixed-size chunking
- Overlap strategies
- Metadata preservation

**Verification**: Can chunk MDX content while preserving semantic meaning

---

### Frontend (Phase 2 Additions)

#### SK-F006: React State Management for Chat
**Level**: Intermediate
**Required For**: ChatWidget implementation

**Competencies**:
- Complex state with useReducer
- Optimistic updates
- WebSocket or polling patterns
- Session management

**Verification**: Can build a chat interface with conversation state

---

#### SK-F007: Accessibility Implementation
**Level**: Intermediate
**Required For**: WCAG compliance

**Competencies**:
- ARIA attributes and roles
- Focus management
- Keyboard navigation
- Screen reader compatibility
- Color contrast compliance

**Verification**: Chat widget passes axe accessibility audit

---

### DevOps

#### SK-O001: Docker Containerization
**Level**: Basic
**Required For**: Backend deployment

**Competencies**:
- Dockerfile creation
- Multi-stage builds
- Environment variable management
- Container networking basics

**Verification**: Can containerize FastAPI app with proper configuration

---

#### SK-O002: Cloud Service Configuration
**Level**: Basic
**Required For**: External service setup

**Competencies**:
- Qdrant Cloud dashboard navigation
- Neon database provisioning
- Environment variable management
- API key security

**Verification**: Can provision and configure all required cloud services

---

## Skill Matrix by Role

### Content Developer
| Skill | Required Level |
|-------|----------------|
| SK-C001 Technical Writing | Advanced |
| SK-F003 MDX Authoring | Basic |
| Domain Knowledge | Advanced |

### Frontend Developer
| Skill | Required Level |
|-------|----------------|
| SK-F001 React | Intermediate |
| SK-F002 TypeScript | Intermediate |
| SK-F004 Docusaurus | Intermediate |
| SK-F005 CSS | Intermediate |
| SK-F006 Chat State | Intermediate |
| SK-F007 Accessibility | Intermediate |
| SK-T001 Playwright | Intermediate |

### Backend Developer
| Skill | Required Level |
|-------|----------------|
| SK-B001 Python | Intermediate |
| SK-B002 FastAPI | Intermediate |
| SK-B003 LangChain | Intermediate |
| SK-B004 OpenAI API | Basic |
| SK-D001 Vector DB | Intermediate |
| SK-D002 PostgreSQL | Basic |
| SK-D003 Chunking | Intermediate |

### DevOps/Infrastructure
| Skill | Required Level |
|-------|----------------|
| SK-O001 Docker | Basic |
| SK-O002 Cloud Services | Basic |
| CI/CD Configuration | Basic |

---

## Skill Development Resources

### Phase 1 Resources

| Skill | Resource |
|-------|----------|
| React | [React Documentation](https://react.dev) |
| Docusaurus | [Docusaurus Docs](https://docusaurus.io/docs) |
| Playwright | [Playwright Docs](https://playwright.dev/docs/intro) |
| MDX | [MDX Documentation](https://mdxjs.com/docs/) |

### Phase 2 Resources

| Skill | Resource |
|-------|----------|
| FastAPI | [FastAPI Documentation](https://fastapi.tiangolo.com) |
| LangChain | [LangChain Docs](https://python.langchain.com/docs/) |
| OpenAI API | [OpenAI Documentation](https://platform.openai.com/docs) |
| Qdrant | [Qdrant Documentation](https://qdrant.tech/documentation/) |
| Neon | [Neon Documentation](https://neon.tech/docs) |

---

## Skill Verification Checklist

### Before Phase 2 Development

- [ ] Python 3.11+ environment configured
- [ ] FastAPI "Hello World" endpoint running
- [ ] OpenAI API key tested with embedding call
- [ ] Qdrant Cloud account provisioned
- [ ] Neon database connection established
- [ ] React ChatWidget scaffold created
- [ ] Playwright test suite executing

### Quality Gates

| Milestone | Skill Verification |
|-----------|-------------------|
| M2.0.4 Backend Scaffold | SK-B002 FastAPI |
| M2.1.3 Embedding Pipeline | SK-B004 OpenAI, SK-D003 Chunking |
| M2.1.4 Qdrant Upload | SK-D001 Vector DB |
| M2.2.2 RAG Pipeline | SK-B003 LangChain |
| M2.3.1 ChatWidget | SK-F006 Chat State |
| M2.3.4 Accessibility | SK-F007 A11y |

---

**Skills Version**: 1.0.0 | **Last Updated**: 2025-12-12
