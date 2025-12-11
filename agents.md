# Agents

This document describes the AI agents involved in developing the Physical AI & Humanoid Robotics textbook project.

## Agent Roster

### Claude Code Agent

**Role**: Primary development agent
**Model**: Claude Opus 4.5 (claude-opus-4-5-20251101)
**Surface**: CLI / Terminal

**Responsibilities**:
- Analyze specifications and generate structured outlines
- Research technical accuracy using MCP tools and web search
- Draft educational content following spec requirements
- Create illustrative pseudocode (NOT production code)
- Generate test specifications for Playwright validation
- Create and maintain PHR records for all interactions
- Execute task checklists from spec-driven workflow

**Constraints** (per Constitution):
- MUST NOT generate executable implementation code
- MUST NOT make architectural decisions without human approval
- MUST cite sources for all technical claims
- MUST flag uncertainty and request clarification
- MUST adhere to spec acceptance criteria before marking complete

### Context7 Agent (Optional)

**Role**: Documentation reference agent
**Purpose**: Provide up-to-date documentation references

**Responsibilities**:
- Provide current documentation references for ROS2, Gazebo, Isaac, etc.
- Validate API compatibility claims
- Surface deprecation warnings for platform APIs

## Agent Workflow

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

## Agent Commands

| Command | Purpose |
|---------|---------|
| `/sp.constitution` | Create or update project constitution |
| `/sp.specify` | Create feature specification |
| `/sp.plan` | Create implementation plan |
| `/sp.task` | Create atomic task file |
| `/sp.implement` | Create implementation narrative |
| `/sp.adr` | Create architectural decision record |
| `/sp.phr` | Create prompt history record |

## Agent Principles

1. **Spec-Driven**: All work originates from approved specifications
2. **No Vibe Coding**: No implementation code; pseudocode only for illustration
3. **Human-in-the-Loop**: Architectural decisions require human approval
4. **Traceability**: PHR records for every significant interaction
5. **Safety-First**: Safety considerations in all content and recommendations

## Agent Configuration

The agent operates under the constraints defined in:
- `.specify/memory/constitution.md` - Project principles
- `CLAUDE.md` - Agent instructions and rules
- `specs/physical-ai-textbook/` - Feature specifications

## Agent Outputs

| Output Type | Location |
|-------------|----------|
| Specifications | `specs/<feature>/spec.md` |
| Plans | `specs/<feature>/plan.md` |
| Tasks | `specs/<feature>/tasks/` |
| Implementation Narratives | `specs/<feature>/implement/` |
| PHR Records | `history/prompts/` |
| ADR Records | `history/adr/` |
| Content | `my-project/docs/` |
