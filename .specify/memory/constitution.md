<!--
Sync Impact Report
==================
Version change: N/A → 1.0.0 (initial ratification)
Added sections:
  - Core Principles (I–VII)
  - Agent Responsibilities
  - Human Responsibilities
  - Tooling Standards
  - Security & Safety Standards
  - Governance
Templates requiring updates:
  - plan-template.md ⚠ pending (review for robotics-specific constraints)
  - spec-template.md ⚠ pending (review for simulation workflow sections)
  - tasks-template.md ⚠ pending (review for safety checkpoint tasks)
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Course Book Constitution

## Mission

Produce a high-quality, pedagogically rigorous course book on Physical AI and Humanoid Robotics. The book MUST enable learners to understand embodied intelligence theory, design safe humanoid control systems, operate high-fidelity simulation workflows, and deploy reliable ROS2-based robotics applications.

## Scope

### In Scope

- Embodied intelligence fundamentals and cognitive architectures
- Humanoid kinematic and dynamic modeling
- High-fidelity simulation environments (Isaac Sim, MuJoCo, Gazebo)
- Sim-to-real transfer methodologies
- ROS2 architecture, lifecycle management, and reliability patterns
- Humanoid locomotion, manipulation, and perception systems
- Safety standards compliance (ISO 13482, ISO 10218, IEC 62443)
- Testing strategies for robotic systems

### Out of Scope

- Production deployment of physical robots (book is educational)
- Vendor-specific proprietary systems without open alternatives
- Real-time kernel tuning and low-level driver development
- Commercial licensing of simulation content

## Non-Goals

- This project does NOT produce deployable robot firmware or control code
- This project does NOT certify readers for safety compliance
- This project does NOT replace hands-on laboratory training

## Core Principles

### I. Spec-Driven Development

All content MUST originate from approved specifications. No chapter, section, or code example proceeds without a documented spec reviewed by stakeholders. Specs define acceptance criteria before any authoring begins.

### II. No Vibe Coding

Agents MUST NOT use vibe coding or produce any implementation code. All code artifacts are illustrative pseudocode or reference snippets for educational purposes only. Production-quality implementation is explicitly forbidden within this project's scope.

### III. Embodied Intelligence First

Content MUST ground abstract AI concepts in physical embodiment. Every theoretical discussion connects to sensor-motor loops, environmental interaction, and real-world constraints. Pure algorithmic treatment without embodiment context is prohibited.

### IV. High-Fidelity Simulation Rigor

Simulation workflows MUST prioritize physical accuracy over computational convenience. Content covers:
- Physics engine selection criteria (contact dynamics, friction models)
- Sensor simulation fidelity (noise models, latency)
- Domain randomization for sim-to-real transfer
- Validation against real-world benchmarks

### V. ROS2 Reliability Standards

All ROS2 content MUST emphasize reliability patterns:
- Lifecycle node management (managed nodes, state transitions)
- Quality of Service (QoS) configuration for deterministic communication
- Component composition and intra-process communication
- Failure detection, recovery, and graceful degradation

### VI. Safety-Critical Mindset

Content MUST instill safety-first thinking:
- Hazard identification and risk assessment frameworks
- Functional safety concepts (SIL, PL ratings)
- Human-robot interaction safety zones
- Emergency stop systems and watchdog architectures
- Compliance pathways for ISO 13482 (personal care robots)

### VII. Testability and Verification

Every concept MUST include verification strategies:
- Unit testing for ROS2 nodes (launch_testing, pytest)
- Integration testing for subsystem interactions
- Hardware-in-the-loop (HIL) simulation validation
- Acceptance criteria tied to measurable outcomes

## Agent Responsibilities

### Claude Code Agent

- Analyze specifications and generate structured outlines
- Research technical accuracy using MCP tools and web search
- Draft educational content following spec requirements
- Create illustrative pseudocode (NOT production code)
- Generate test specifications for Playwright validation
- Create and maintain PHR records for all interactions

### Claude Code Constraints

- MUST NOT generate executable implementation code
- MUST NOT make architectural decisions without human approval
- MUST cite sources for all technical claims
- MUST flag uncertainty and request clarification
- MUST adhere to spec acceptance criteria before marking complete

### Context7 Agent (if applicable)

- Provide up-to-date documentation references
- Validate API compatibility claims
- Surface deprecation warnings for ROS2/simulation APIs

## Human Responsibilities

### Content Architects

- Define and approve all specifications
- Make architectural decisions (ADRs)
- Review agent-generated content for technical accuracy
- Validate pedagogical effectiveness
- Approve simulation workflow designs

### Domain Experts

- Verify safety standard interpretations
- Review embodied intelligence theory accuracy
- Validate ROS2 best practices
- Confirm simulation fidelity claims

### Quality Reviewers

- Execute Playwright test specifications
- Verify acceptance criteria completion
- Flag content gaps or inconsistencies

## Tooling Standards

### Spec-Kit Plus

- All features tracked via `specs/<feature>/` structure
- Mandatory artifacts: `spec.md`, `plan.md`, `tasks.md`
- PHR records stored in `history/prompts/`
- ADRs stored in `history/adr/`

### Claude Code

- Primary agent for content generation
- Operates under this constitution's constraints
- Creates PHR for every significant interaction
- Suggests ADRs for architectural decisions (never auto-creates)

### Playwright Test Specifications

- Define acceptance tests for rendered content
- Validate navigation, search, and cross-references
- Test code block rendering and syntax highlighting
- Verify accessibility compliance (WCAG 2.1 AA)

### Docusaurus

- Static site generator for course book output
- MDX format for interactive content
- Versioning for curriculum iterations
- Search integration for discoverability

## Security & Safety Standards

### Content Security

- No secrets, credentials, or API keys in content
- Example configurations use placeholder values
- External links validated and archived

### Safety Content Requirements

- All safety-related content peer-reviewed by domain expert
- Warning callouts for hazardous operations
- Clear disclaimers on simulation vs. real-world behavior
- Emergency procedure documentation in relevant sections

### Compliance References

- ISO 13482: Robots and robotic devices — Safety requirements for personal care robots
- ISO 10218-1/2: Robots and robotic devices — Safety requirements for industrial robots
- IEC 62443: Industrial communication networks — IT security for networks and systems
- ROS2 REP-2004: Package quality categories

## Governance

### Constitution Authority

This constitution supersedes all other project practices. Conflicts resolve in favor of constitution principles.

### Amendment Process

1. Propose amendment via ADR with rationale
2. Review period: minimum 48 hours
3. Approval requires content architect sign-off
4. Update constitution with version increment
5. Propagate changes to dependent templates

### Version Policy

- MAJOR: Principle removal or fundamental scope change
- MINOR: New principle, section, or significant expansion
- PATCH: Clarification, typo, or non-semantic refinement

### Compliance Verification

- All PRs MUST reference compliance with relevant principles
- Code reviews verify no vibe coding violations
- Specs reviewed against constitution before approval
- Quarterly constitution review for relevance

**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12
