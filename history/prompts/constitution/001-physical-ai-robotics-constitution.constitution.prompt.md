---
id: 001
title: Physical AI Robotics Constitution
stage: constitution
date: 2025-12-12
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: main
user: assad
command: /sp.constitution
labels: ["constitution", "physical-ai", "humanoid-robotics", "embodied-intelligence", "ros2", "safety"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

/sp.constitution create principles for Physical AI & Humanoid Robotics course book. Focus on embodied intelligenece, high-fidelity simulation workflows, humanoid control systems, ROS2 reliability, and safety standards.
You are an AI Spec Agent working inside the Docusaurus-based
"Physical AI & Humanoid Robotics" book project.

Task:
Generate the file: /spec/sp.constitution.md

Requirements:
- Define the project mission, scope, non-goals, and constraints.
- Explicitly include: "Agents must not use vibe coding or produce
  any implementation code."
- Define responsibilities of agents vs humans.
- Include rules for Claude Code, Context7, Spec-Kit Plus, and
  Playwright test-spec usage.
- Keep language: clear, concise, spec-style.
- Output only the full markdown content of sp.constitution.md.

## Response snapshot

Created constitution at `.specify/memory/constitution.md` with version 1.0.0. Key sections include:

- **Mission**: Produce pedagogically rigorous course book on Physical AI and Humanoid Robotics
- **Core Principles (I-VII)**: Spec-Driven Development, No Vibe Coding, Embodied Intelligence First, High-Fidelity Simulation Rigor, ROS2 Reliability Standards, Safety-Critical Mindset, Testability and Verification
- **Agent Responsibilities**: Claude Code constraints (no executable code, cite sources, flag uncertainty)
- **Human Responsibilities**: Content Architects, Domain Experts, Quality Reviewers
- **Tooling Standards**: Spec-Kit Plus, Claude Code, Playwright, Docusaurus
- **Security & Safety Standards**: Content security, safety content requirements, compliance references (ISO 13482, ISO 10218, IEC 62443, ROS2 REP-2004)
- **Governance**: Amendment process, version policy, compliance verification

## Outcome

- Impact: Initial constitution established for Physical AI & Humanoid Robotics course book project
- Tests: N/A (constitution document)
- Files: 1 created (.specify/memory/constitution.md)
- Next prompts: Create feature specs for individual chapters, set up Docusaurus content structure
- Reflection: Constitution covers all requested focus areas with clear agent/human boundaries

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution against actual content authoring workflow
