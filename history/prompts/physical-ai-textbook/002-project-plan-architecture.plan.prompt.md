---
id: 002
title: Project Plan Architecture
stage: plan
date: 2025-12-12
surface: agent
model: claude-opus-4-5-20251101
feature: physical-ai-textbook
branch: feature/physical-ai-textbook-plan
user: assad
command: /sp.plan
labels: ["plan", "architecture", "docusaurus", "qdrant", "fastapi", "chatkit", "rag"]
links:
  spec: specs/physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/physical-ai-textbook/plan.md
tests:
  - null
---

## Prompt

/sp.plan Use Docusaurus for documentation, Qdrant Cloud for RAG vector store, FastAPI backend for chatbot, and OpenAI ChatKit for agentic AI interface

You are an AI Spec Agent working inside the Docusaurus-based "Physical AI & Humanoid Robotics" book project.

Task: Generate the full project plan file: /spec/sp.plan.md

Requirements:
- Include: High-level timeline, Milestones for all 4 modules, Dependencies between modules, Deliverables for each milestone, Documentation milestones (Docusaurus), QA milestones (Playwright test-spec milestones), Review & approval checkpoints
- Rules: No vibe coding, No implementation code, Only structured planning, Clearly show human review points

Output: Provide the complete markdown for sp.plan.md only.

## Response snapshot

Created comprehensive project plan at `specs/physical-ai-textbook/plan.md` with 4-module architecture:

**Architecture**:
- Module 1: Docusaurus Documentation (28 chapters, MDX, quizzes, glossary)
- Module 2: Qdrant Cloud RAG Store (vector embeddings, semantic search)
- Module 3: FastAPI Backend (search API, chat API, RAG pipeline)
- Module 4: OpenAI ChatKit Interface (agentic assistant, context-aware Q&A)

**Milestones** (5 Phases):
- Phase 0: Foundation Setup (2 milestones)
- Phase 1: Docusaurus Documentation (9 milestones, per-part content)
- Phase 2: Qdrant Cloud RAG (3 milestones)
- Phase 3: FastAPI Backend (5 milestones)
- Phase 4: ChatKit Interface (3 milestones)
- Phase 5: QA & Launch (5 milestones)

**Human Review Points**: 9 blocking checkpoints identified (architecture, security, content accuracy, API contracts, pedagogy, accessibility, launch)

**ADR Suggestions**: 3 architectural decisions flagged for documentation

## Outcome

- Impact: Complete project plan enabling structured development of 4-module system
- Tests: QA milestones defined (5 test categories from spec)
- Files: 1 created (specs/physical-ai-textbook/plan.md)
- Next prompts: `/sp.tasks` to break down into implementable tasks, `/sp.adr` for flagged decisions
- Reflection: Plan follows spec requirements; dependencies clearly mapped between modules

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate milestone sequencing with stakeholders before task breakdown
