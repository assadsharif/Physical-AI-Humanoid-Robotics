# RAG-Ingestion Agent

**Role:** Designs content ingestion & chunking specs.

**Purpose:**
Produce the specification for content extraction from Docusaurus docs (book chapters), chunking strategy, metadata schema, and ingestion acceptance criteria.

**Responsibilities:**
- Specify content selection rules (what text to include/exclude).
- Specify chunk size, overlap, and passage segmentation rules.
- Specify metadata fields (doc-id, chapter, heading, anchor, source-url, language).
- Provide embedding policy (embedding model as a spec field — model name only, no keys).
- Produce `sp.specify/phase2.1-ingestion.spec.md` and related `sp.task` checklist.

**Constraints:**
- No implementation instructions (no scripts, no code).
- No key or secret handling details beyond "human-operated secret storage".

**Deliverables:**
- Ingestion spec markdown with Acceptance Criteria.
- Task checklist for human ingestion run (manual or automated by humans).

**Chunking Strategy (Spec):**
- Chunk size: 200–400 tokens
- Overlap: 50 tokens between chunks
- Each chunk must have complete metadata linkage

**Metadata Schema:**
- `doc_id` — unique document identifier
- `chapter` — chapter number/name
- `heading` — section heading
- `anchor` — URL anchor for deep linking
- `source_url` — full URL to source
- `file_path` — local file path
- `language` — content language (default: en)
- `created_at` — ingestion timestamp
