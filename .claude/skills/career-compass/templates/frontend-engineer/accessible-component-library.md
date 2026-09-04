---
title: "Accessible Component Library with Storybook"
track: "frontend-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["html-css", "frontend-frameworks", "web-accessibility", "design-systems", "frontend-testing"]
skill_prerequisites: ["javascript", "git-version-control"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# Accessible Component Library with Storybook

## Production Workflow Mirrored
1. Building reusable UI primitives (button, input, select, modal, tabs)
   with a consistent API
2. Documenting each component in isolation with its states and variants
3. Meeting keyboard, screen-reader, and contrast requirements from the start
4. Testing components for behavior and accessibility automatically
5. Versioning and publishing a shared package other teams consume

## What You'll Build
A small design-system package in React, Vue, or Svelte containing at
least six components (button, text input, select, checkbox, modal dialog,
tabs) with design tokens for color, spacing, and typography, a Storybook
showing every state, automated accessibility checks, and component tests
for keyboard interaction.

## Student-Scope Notes
- Six components is the floor. Depth (correct focus management in the
  modal, arrow-key navigation in tabs) matters more than breadth.
- Use the framework's mainstream testing library plus axe for
  accessibility assertions. No visual-regression service required.
- "Publishing" means a local package build that a second sample app
  installs from a file path or a private registry, not a public npm
  release.

## Steps
1. Define design tokens (color scale with documented contrast ratios,
   spacing scale, type scale) as CSS custom properties or a theme object.
2. Build the button and text input with all states (default, hover,
   focus-visible, disabled, error, loading) and write Storybook stories
   for each.
3. Build the modal dialog with focus trap, return-focus-on-close, Escape
   to close, and the correct dialog role and labelling.
4. Build tabs with roving tabindex, arrow-key navigation, and correct
   tab/tabpanel roles. Build select and checkbox with proper labels.
5. Add axe checks to every story and fix every violation it finds.
6. Write component tests that drive each component purely by keyboard and
   assert the resulting state.
7. Run a manual screen-reader pass (VoiceOver or NVDA) over the modal and
   tabs and record what you fixed.
8. Build the package, install it in a tiny sample app, and write the
   README with usage examples and the accessibility guarantees each
   component makes.

## Extension Ideas
- Add a dark theme via token swapping and prove contrast still passes.
- Add a combobox with typeahead, the hardest common accessible widget.
- Add visual regression tests with Storybook's test runner.
- Add a changelog and semantic versioning workflow.

## Skills Demonstrated
- Component API design and design-token architecture
- Keyboard and screen-reader accessibility implemented, not just claimed
- Storybook-driven documentation and component testing
- Building and consuming a shared UI package

## Industry Relevance

Enterprise Software, Government Digital Services, Healthcare Portals. Accessibility is a legal requirement in these sectors and a core hiring filter for frontend roles; teams maintain shared component libraries precisely so accessibility is solved once and reused. A candidate who can show a modal with correct focus management and tests for it stands out immediately.
