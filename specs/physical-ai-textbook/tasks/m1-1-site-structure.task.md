# Task: M1.1 Site Structure

**Task ID**: M1.1
**Milestone**: Phase 1 - Module 1 (Docusaurus Documentation)
**Status**: Not Started
**Created**: 2025-12-12
**Branch**: `feature/physical-ai-textbook-tasks`

---

## Task Summary

Set up the foundational Docusaurus site structure including navigation, sidebars, and the complete part/chapter hierarchy for the 28-chapter Physical AI & Humanoid Robotics textbook.

## Purpose

Establish the information architecture that enables learners to navigate the textbook intuitively. This task creates the skeleton structure that all subsequent content tasks (M1.2-M1.9) will populate.

## Inputs

- `specs/physical-ai-textbook/spec.md` - Textbook structure overview (28 chapters in 6 parts)
- `specs/physical-ai-textbook/plan.md` - Project structure and file conventions
- Docusaurus v3.x documentation for sidebar and navigation configuration
- Existing `my-project/` Docusaurus scaffold

## Outputs

- Configured `docusaurus.config.ts` with site metadata and theme settings
- Configured `sidebars.ts` with 6-part hierarchical structure
- Directory structure under `my-project/docs/` for all 28 chapters
- Placeholder MDX files for each chapter with frontmatter
- Navigation header with part-level access
- Breadcrumb configuration for chapter context

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| M0.1 Project Scaffolding | Predecessor | Must be complete |
| Docusaurus v3.x installed | Technical | Required |
| Node.js 18+ environment | Technical | Required |

**Blocked By**: M0.1 (Project Scaffolding must be complete first)
**Blocks**: M1.2 (Core Components), M1.3-M1.8 (All content milestones)

---

## Step-by-Step Checklist

> **Instructions**: Complete each step in order. Check the box when done. Do not skip steps.

### Phase A: Configuration Setup

- [ ] **A1** Open `my-project/docusaurus.config.ts`
- [ ] **A2** Update site metadata:
  - [ ] Set `title` to "Physical AI & Humanoid Robotics"
  - [ ] Set `tagline` to "From Foundations to Advanced Humanoid Control"
  - [ ] Configure `url` and `baseUrl` for deployment target
  - [ ] Add `organizationName` and `projectName`
- [ ] **A3** Configure theme settings:
  - [ ] Enable dark mode toggle
  - [ ] Configure navbar with logo and title
  - [ ] Add search placeholder (Algolia or local search)
- [ ] **A4** Save configuration and verify dev server starts without errors

### Phase B: Directory Structure Creation

- [ ] **B1** Navigate to `my-project/docs/`
- [ ] **B2** Remove default tutorial content (if present)
- [ ] **B3** Create Part I directory structure:
  ```
  docs/part-i-foundations/
  ├── _category_.json
  ├── ch01-embodied-intelligence.mdx
  ├── ch02-physical-ai-principles.mdx
  ├── ch03-robotics-mathematics.mdx
  └── ch04-safety-foundations.mdx
  ```
- [ ] **B4** Create Part II directory structure:
  ```
  docs/part-ii-humanoid-fundamentals/
  ├── _category_.json
  ├── ch05-humanoid-kinematics.mdx
  ├── ch06-dynamics-actuation.mdx
  ├── ch07-sensing-perception.mdx
  └── ch08-human-robot-interaction.mdx
  ```
- [ ] **B5** Create Part III directory structure:
  ```
  docs/part-iii-ros2/
  ├── _category_.json
  ├── ch09-ros2-architecture.mdx
  ├── ch10-lifecycle-management.mdx
  ├── ch11-qos-reliability.mdx
  ├── ch12-component-composition.mdx
  └── ch13-debugging-observability.mdx
  ```
- [ ] **B6** Create Part IV directory structure:
  ```
  docs/part-iv-simulation/
  ├── _category_.json
  ├── ch14-gazebo-harmonic.mdx
  ├── ch15-unity-robotics.mdx
  ├── ch16-nvidia-isaac.mdx
  ├── ch17-sim-to-real.mdx
  └── ch18-platform-selection.mdx
  ```
- [ ] **B7** Create Part V directory structure:
  ```
  docs/part-v-control/
  ├── _category_.json
  ├── ch19-bipedal-locomotion.mdx
  ├── ch20-whole-body-control.mdx
  ├── ch21-manipulation-grasping.mdx
  ├── ch22-perception-integration.mdx
  └── ch23-sensor-fusion.mdx
  ```
- [ ] **B8** Create Part VI directory structure:
  ```
  docs/part-vi-vla/
  ├── _category_.json
  ├── ch24-vla-architecture.mdx
  ├── ch25-training-vla.mdx
  ├── ch26-deployment-inference.mdx
  ├── ch27-safety-learned-systems.mdx
  └── ch28-future-directions.mdx
  ```

### Phase C: Category Configuration

- [ ] **C1** Create `docs/part-i-foundations/_category_.json`:
  ```json
  {
    "label": "Part I: Foundations of Physical AI",
    "position": 1,
    "collapsible": true,
    "collapsed": false
  }
  ```
- [ ] **C2** Create `_category_.json` for Part II (position: 2)
- [ ] **C3** Create `_category_.json` for Part III (position: 3)
- [ ] **C4** Create `_category_.json` for Part IV (position: 4)
- [ ] **C5** Create `_category_.json` for Part V (position: 5)
- [ ] **C6** Create `_category_.json` for Part VI (position: 6)

### Phase D: Chapter Placeholder Files

- [ ] **D1** Create placeholder MDX template with required frontmatter:
  ```mdx
  ---
  sidebar_position: [N]
  title: "[Chapter Title]"
  description: "[Brief description]"
  keywords: ["physical-ai", "humanoid", "[topic]"]
  ---

  # [Chapter Title]

  :::info Learning Objectives
  - [Objective 1]
  - [Objective 2]
  - [Objective 3]
  :::

  :::note Prerequisites
  - [Prerequisite 1]
  - [Prerequisite 2]
  :::

  **Estimated Time**: [X] minutes

  ---

  ## Content Placeholder

  *This chapter is under development.*

  ---

  ## Self-Assessment

  *Quiz coming soon.*
  ```
- [ ] **D2** Apply template to all 28 chapter files with appropriate metadata
- [ ] **D3** Verify each chapter has unique `sidebar_position` within its part
- [ ] **D4** Add appropriate keywords to each chapter frontmatter

### Phase E: Sidebar Configuration

- [ ] **E1** Open `my-project/sidebars.ts`
- [ ] **E2** Configure autogenerated sidebar:
  ```typescript
  const sidebars = {
    textbookSidebar: [
      {
        type: 'autogenerated',
        dirName: '.',
      },
    ],
  };
  ```
- [ ] **E3** Alternatively, configure explicit sidebar if more control needed
- [ ] **E4** Verify sidebar renders all 6 parts with correct hierarchy
- [ ] **E5** Test collapsible behavior works correctly

### Phase F: Navigation Header

- [ ] **F1** Configure navbar items in `docusaurus.config.ts`:
  - [ ] Add "Textbook" link pointing to Part I Chapter 1
  - [ ] Add "Glossary" placeholder link
  - [ ] Add "About" link
  - [ ] Add GitHub repository link (if public)
- [ ] **F2** Verify navbar renders correctly on desktop
- [ ] **F3** Verify mobile hamburger menu works

### Phase G: Verification

- [ ] **G1** Run `npm run build` and verify no errors
- [ ] **G2** Run `npm run serve` and test navigation:
  - [ ] Homepage loads correctly
  - [ ] All 6 parts visible in sidebar
  - [ ] All 28 chapters accessible
  - [ ] Breadcrumbs show correct hierarchy
  - [ ] Part collapse/expand works
- [ ] **G3** Test on mobile viewport (375px)
- [ ] **G4** Verify all internal links resolve (no 404s)
- [ ] **G5** Document any deviations or issues encountered

---

## Acceptance Criteria

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| AC-01 | Docusaurus dev server starts without errors | `npm run start` succeeds |
| AC-02 | All 6 parts visible in sidebar navigation | Visual inspection |
| AC-03 | All 28 chapters accessible via sidebar | Click each chapter link |
| AC-04 | Breadcrumb navigation shows Part > Chapter | Visual inspection on any chapter |
| AC-05 | Part sections are collapsible | Click collapse toggle |
| AC-06 | Mobile navigation menu functions | Test on 375px viewport |
| AC-07 | `npm run build` completes without errors | Build command succeeds |
| AC-08 | Each chapter has valid frontmatter | No build warnings about frontmatter |
| AC-09 | Sidebar position ordering is correct | Chapters appear in numerical order |
| AC-10 | Navigation reaches any chapter in ≤3 clicks | Manual navigation test |

---

## Related Specifications

| Document | Relevance |
|----------|-----------|
| `specs/physical-ai-textbook/spec.md` | Textbook structure overview (Section: Textbook Structure Overview) |
| `specs/physical-ai-textbook/plan.md` | Project structure (Section: Source Code) |
| `.specify/memory/constitution.md` | Principle I (Spec-Driven), Principle VII (Testability) |

---

## QA Notes

### Playwright Test-Spec References

| Test ID | Description | Relates To |
|---------|-------------|------------|
| NAV-001 | Homepage loads and displays part navigation | AC-02 |
| NAV-002 | Click Part I → Chapter 1 | AC-03, AC-10 |
| NAV-003 | Breadcrumb navigation works | AC-04 |
| NAV-005 | Mobile menu toggles correctly | AC-06 |

### Manual QA Checklist

- [ ] Verify dark mode toggle works
- [ ] Verify search placeholder appears (functional search comes later)
- [ ] Verify consistent styling across all placeholder pages
- [ ] Verify no console errors in browser developer tools
- [ ] Verify responsive layout at 375px, 768px, 1024px, 1440px viewports

---

## Human Review Checkpoint

**Reviewer Role**: UX Designer / Information Architect
**Review Focus**:
- Navigation hierarchy intuitive for learners
- Part/chapter naming clear and descriptive
- Mobile experience acceptable
- Consistent with Docusaurus best practices

**Approval Required Before**: M1.2 (Core Components) can begin

---

## Notes

- Do NOT add actual chapter content in this task (that's M1.3-M1.8)
- Do NOT create custom components in this task (that's M1.2)
- Placeholder content should clearly indicate "under development" status
- All file names use kebab-case convention
- Chapter numbers are zero-padded for consistent sorting (ch01, ch02, etc.)

---

**Task Version**: 1.0.0 | **Author**: Claude Code Agent | **Reviewed**: Pending
