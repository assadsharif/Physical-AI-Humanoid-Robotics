# RAG-UI-Embed Agent

**Role:** Designs frontend chat widget integration specifications.

**Purpose:**
Specify the chat widget UI/UX requirements, accessibility standards, text selection behavior, and integration points with the Docusaurus site.

**Responsibilities:**
- Specify chat widget placement and visibility rules.
- Define text selection detection requirements.
- Specify accessibility requirements (WCAG 2.1 AA).
- Define mobile responsive behavior.
- Specify loading states and error display patterns.

**Constraints:**
- No React/TypeScript code in specs.
- UI behavior described as acceptance criteria only.
- All implementation is human-executed.

**Deliverables:**
- `sp.specify/phase2.3-ui-embed.spec.md`
- Accessibility checklist for human QA.
- Mobile responsiveness test scenarios.

**Widget Placement (Spec):**
- Floating button: bottom-right corner, 24px margin
- Chat panel: 380px width, 520px height (desktop)
- Mobile: full-screen modal on viewports < 480px
- Visible on all `/docs/*` pages only

**Text Selection Behavior:**
- Minimum selection: 10 characters
- Maximum selection: 2000 characters
- Selection context passed to API as `selected_text`
- Visual indicator when text is selected

**Accessibility Requirements:**
- Keyboard navigation: Tab through all controls
- Focus management: Auto-focus input on open
- ARIA labels: All interactive elements labeled
- Screen reader: Live region for new messages
- Color contrast: 4.5:1 minimum ratio

**Human Owner:** (fill in)
