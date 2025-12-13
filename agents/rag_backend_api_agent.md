# RAG-Backend-API Agent

**Role:** Designs backend API and service interaction (FastAPI conceptual spec).

**Purpose:**
Specify endpoints, request/response shapes, auth model (conceptual), rate-limiting policy, and error-handling semantics for `/api/chat` and related endpoints.

**Responsibilities:**
- Define API contract for `/api/chat` (inputs, outputs, headers, status codes).
- Specify RAG pipeline flow (retrieval → augmentation → generation) as a diagram.
- Define rate-limiting rules and error taxonomy.
- Specify service dependencies (Qdrant, Neon, OpenAI) as integration points (names only, no keys).

**Constraints:**
- No implementation code, no FastAPI route handlers.
- Secrets referenced by name only (e.g., `OPENAI_API_KEY`), never values.

**Deliverables:**
- `sp.specify/phase2.2-backend-api.spec.md`
- API contract with request/response examples (conceptual).
- Error handling matrix.

**API Contract — `/api/chat` (Conceptual):**

**Request Schema:**
- `query` (string) — user question
- `session_id` (string) — conversation identifier
- `selected_text` (string, optional) — when user selects text on page
- `page_context` (object) — current page URL and chapter

**Response Schema:**
- `response_text` (string) — generated answer
- `sources` (array) — each with `source_url`, `anchor`, `snippet`
- `provenance` (object) — how the answer was composed (spec fields only)
- `status` (string) — OK / ERROR

**Behavioral Notes:**
- If `selected_text` present → retrieval limited to those chunks only.
- Service must attach provenance for each claim with exact source anchors.

**Acceptance Criteria:**
- AC1: Payload examples (conceptual) exist in the spec.
- AC2: Handler semantics for selected-text-only queries are clearly described.
- AC3: Error semantics are documented (e.g., missing context, empty retrieval).

**Human Owner:** (fill in)
