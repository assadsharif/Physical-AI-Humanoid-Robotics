# Constitution Amendment Proposal: Phase 2 RAG Chatbot

**Proposal ID**: CAP-2025-001
**Date**: 2025-12-12
**Status**: Pending Human Approval
**Affects**: `.specify/memory/constitution.md`

---

## Summary

This proposal suggests amendments to the project constitution to accommodate Phase 2 RAG chatbot functionality. Per Constitution Governance (Amendment Process), these changes require content architect sign-off.

---

## Proposed Changes

### 1. New Section: RAG Chatbot Principles (VIII)

**Rationale**: Phase 2 introduces LLM-generated responses that require explicit governance to ensure quality and safety.

**Proposed Text**:

```markdown
### VIII. RAG Chatbot Governance

Content MUST ensure the RAG chatbot operates within strict boundaries:

- **Book-Scope Only**: Chatbot MUST only answer questions about textbook content
- **Grounded Responses**: All responses MUST be based on retrieved context, never fabricated
- **Citation Required**: Every factual claim MUST cite the source chapter/section
- **Off-Topic Refusal**: Non-textbook questions MUST be politely declined
- **No PII Collection**: Conversation storage MUST NOT include user identifying information
- **Prompt Hardening**: System prompts MUST be designed to resist prompt injection attacks
```

---

### 2. Update: Tooling Standards Section

**Rationale**: Phase 2 introduces new external service dependencies that should be documented in constitution.

**Proposed Addition** (under Tooling Standards):

```markdown
### RAG Infrastructure (Phase 2)

- **Vector Store**: Qdrant Cloud for semantic search
  - Free tier constraints: 1GB storage, 1M vectors
  - Collection: `textbook_chunks` with 1536-dim embeddings
- **Database**: Neon Serverless Postgres for conversation history
  - Free tier constraints: 512MB storage, 3GB transfer/month
  - Tables: conversations, messages
- **LLM Provider**: OpenAI API for embeddings and generation
  - Embedding model: text-embedding-ada-002
  - Generation model: GPT-4 / GPT-4-turbo
  - Rate limits: Must be handled gracefully
```

---

### 3. Update: Agent Responsibilities Section

**Rationale**: Phase 2 introduces new agents that should be formally acknowledged in constitution.

**Proposed Addition** (under Agent Responsibilities):

```markdown
### RAG Chatbot Agents (Phase 2)

- **RAG Orchestration Agent**: Coordinate retrieval-augmented generation
- **Embedding Agent**: Convert queries to vector embeddings
- **Retrieval Agent**: Search Qdrant for relevant content
- **Generation Agent**: Produce grounded responses with citations
- **Conversation Agent**: Manage chat history in Neon Postgres

### RAG Agent Constraints

- MUST NOT generate content outside retrieved context
- MUST NOT store or process user PII
- MUST handle external API failures gracefully
- MUST log usage for cost monitoring
```

---

### 4. Update: Security & Safety Standards Section

**Rationale**: Chatbot introduces new security considerations not covered in original constitution.

**Proposed Addition** (under Security & Safety Standards):

```markdown
### Chatbot Security Requirements

- **Prompt Injection Prevention**: System prompts must be hardened against injection attacks
- **Input Validation**: All user input must be validated and sanitized
- **Rate Limiting**: Per-session rate limits must prevent abuse
- **Response Filtering**: Responses must not leak system prompts or internal context
- **Data Retention**: Conversation data must be automatically pruned after 30 days

### Chatbot Safety Content

- Chatbot must not provide advice that could lead to physical harm
- Safety warnings from textbook content must be preserved in chatbot responses
- Chatbot must include disclaimers when discussing simulation vs. real-world behavior
```

---

### 5. New Section: Data Retention Policy (IX)

**Rationale**: Phase 2 stores conversation data, requiring explicit retention policy.

**Proposed Text**:

```markdown
### IX. Data Retention Policy

Data handling MUST follow these retention guidelines:

- **Conversation History**: Retained for 30 days, then automatically deleted
- **Analytics Data**: Aggregated metrics only, no raw query content after 7 days
- **Vector Embeddings**: Retained indefinitely (textbook content, not user data)
- **Session Identifiers**: Anonymous UUIDs only, no correlation to user identity

### Data Subject Rights

- No PII is collected, therefore GDPR subject access rights are N/A
- Users cannot request conversation deletion (no user accounts)
- Analytics data is anonymized and aggregated
```

---

## Impact Assessment

| Area | Impact | Migration Required |
|------|--------|-------------------|
| Constitution | MINOR version increment | No |
| Existing specs | No change | No |
| Templates | No change | No |
| Agents | Acknowledge new agents | No |
| Workflows | Add chatbot workflow | No |

---

## Version Change

**Current Version**: 1.0.0
**Proposed Version**: 1.1.0 (MINOR: New section added)

---

## Approval Requirements

Per Constitution Governance (Amendment Process):

1. [ ] Propose amendment via ADR with rationale (this document)
2. [ ] Review period: minimum 48 hours
3. [ ] Approval requires content architect sign-off
4. [ ] Update constitution with version increment
5. [ ] Propagate changes to dependent templates

---

## Architectural Decision Suggestion

**Architectural decision detected**: Constitution amendment for Phase 2 chatbot governance

Document reasoning and tradeoffs? Run `/sp.adr constitution-phase2-amendment`

---

**Proposal Author**: Claude Code Agent | **Review Status**: Pending Human Approval
