# Agent Strategy

**Created**: 2025-12-12
**Status**: Active Rule

## Core Principle

**Create different agents for each phase of development.**

## Phase-to-Agent Mapping

| Phase | Agent Name | Responsibility |
|-------|------------|----------------|
| Phase 0: Foundation | **Setup Agent** | Project scaffolding, infrastructure, CI/CD |
| Phase 1: Documentation | **Content Agent** | Docusaurus site, MDX chapters, components |
| Phase 2: RAG Store | **RAG Agent** | Qdrant ingestion, embeddings, vector search |
| Phase 3: Backend | **API Agent** | FastAPI endpoints, RAG pipeline, chat API |
| Phase 4: Chat Interface | **Chat Agent** | ChatKit integration, agentic behaviors |
| Phase 5: QA & Launch | **QA Agent** | Playwright tests, accessibility, deployment |

## Agent Design Guidelines

1. **Single Responsibility**: Each agent handles ONE phase
2. **Clear Boundaries**: Agents don't overlap in scope
3. **Handoff Protocol**: Define inputs/outputs between agents
4. **Specialized Tools**: Each agent has phase-specific tools
5. **Independent Testing**: Each agent's work is independently verifiable

## Agent Template

For each phase, create an agent file with:
- Agent name and ID
- Phase assignment
- Specific responsibilities
- Tools available
- Constraints
- Inputs (from previous agent)
- Outputs (to next agent)
- Success criteria

## Implementation Notes

- Agents should be defined in `agents/` directory
- Each agent gets its own configuration
- Agents can be run in parallel where phases don't depend on each other
- Human review checkpoints between agent handoffs

## Future Agents to Create

- [ ] Setup Agent (Phase 0)
- [ ] Content Agent (Phase 1)
- [ ] RAG Agent (Phase 2)
- [ ] API Agent (Phase 3)
- [ ] Chat Agent (Phase 4)
- [ ] QA Agent (Phase 5)

## Reference

This strategy supersedes single-agent approach. All future development must assign work to phase-specific agents.
