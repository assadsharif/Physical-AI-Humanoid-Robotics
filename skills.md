# Skills

This document describes the skills and capabilities available in the Physical AI & Humanoid Robotics textbook project.

## Spec-Kit Plus Skills

### Specification Skills

| Skill | Command | Description |
|-------|---------|-------------|
| Constitution | `/sp.constitution` | Define project principles and constraints |
| Specification | `/sp.specify` | Create feature requirements and acceptance criteria |
| Planning | `/sp.plan` | Create architectural plans and milestone breakdowns |
| Task Creation | `/sp.task` | Create atomic, executable task checklists |
| Implementation | `/sp.implement` | Create conceptual implementation narratives |

### Documentation Skills

| Skill | Command | Description |
|-------|---------|-------------|
| ADR Creation | `/sp.adr` | Document architectural decisions |
| PHR Creation | `/sp.phr` | Record prompt history for traceability |
| Checklist | `/sp.checklist` | Generate verification checklists |

### Analysis Skills

| Skill | Command | Description |
|-------|---------|-------------|
| Clarification | `/sp.clarify` | Ask clarifying questions |
| Analysis | `/sp.analyze` | Analyze code or specifications |

## Technical Skills

### Content Development

- **MDX Authoring**: Create educational content in MDX format
- **Diagram Creation**: Generate Mermaid diagrams for visualizations
- **Pseudocode Writing**: Create illustrative (non-production) code examples
- **Quiz Design**: Develop self-assessment questions

### Research & Validation

- **Documentation Research**: Access and cite official documentation
- **Technical Verification**: Validate claims against authoritative sources
- **Safety Review**: Identify safety considerations and hazards

### Project Management

- **Task Tracking**: Maintain todo lists and progress tracking
- **Dependency Analysis**: Identify and document dependencies
- **Risk Assessment**: Identify risks and mitigation strategies

## Platform Skills

### Docusaurus

- Site configuration (docusaurus.config.ts)
- Sidebar management (sidebars.ts)
- MDX component integration
- Navigation structure
- Theme customization

### Git Workflow

- Feature branch creation
- Commit message formatting
- Change staging and status checking

### File Management

- Directory structure creation
- File reading and writing
- Pattern-based file searching

## Skill Constraints

Per the project constitution, the following skills are **NOT** available:

| Unavailable Skill | Reason |
|-------------------|--------|
| Production Code Generation | Constitution Principle II: No Vibe Coding |
| Autonomous ADR Creation | Requires human consent |
| Safety Certification | Educational content only |
| Deployment Automation | Out of scope |

## Skill Development Roadmap

### Current (M1.1 Complete)

- [x] Site structure setup
- [x] Chapter placeholder creation
- [x] Navigation configuration
- [x] Glossary scaffolding

### Planned (M1.2)

- [ ] Quiz component integration
- [ ] GlossaryTerm component
- [ ] SafetyCallout component
- [ ] PseudocodeBlock component

### Future (M2-M4)

- [ ] RAG pipeline integration (Qdrant)
- [ ] Search API integration (FastAPI)
- [ ] Chat interface integration (ChatKit)

## Skill Invocation

Skills are invoked through:

1. **Slash Commands**: `/sp.<skill>` format
2. **Natural Language**: Describe the task and the agent selects appropriate skills
3. **Task Checklists**: Execute predefined task files

## Skill Dependencies

```
Constitution
    │
    ▼
Specification ──► Planning ──► Task Creation
    │                              │
    ▼                              ▼
Implementation Narrative      Task Execution
    │                              │
    ▼                              ▼
ADR (if needed)              PHR Record
```

## Adding New Skills

New skills can be added by:

1. Creating a command file in `.claude/commands/`
2. Updating the constitution if principles change
3. Documenting in this skills.md file
