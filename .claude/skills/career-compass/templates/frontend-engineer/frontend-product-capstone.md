---
title: "Frontend Product Capstone: Ship a Polished App"
track: "frontend-engineer"
difficulty_tier: "advanced"
estimated_hours: 24
role: "capstone"
skill_tags: ["frontend-frameworks", "typescript", "state-management", "web-accessibility", "web-performance", "frontend-testing", "cloud-deployment"]
skill_prerequisites: ["javascript", "html-css", "git-version-control"]
project_prerequisites: ["accessible-component-library.md", "data-driven-dashboard-ui.md"]
prerequisite_learning_hours: 4
---

# Frontend Product Capstone: Ship a Polished App

## Production Workflow Mirrored
1. Turning a product brief into screens, flows, and a component inventory
2. Building on a shared component library rather than one-off UI
3. Managing server state, client state, and URL state coherently
4. Meeting accessibility and performance bars before launch
5. Deploying with CI, previews, and monitoring for errors

## What You'll Build
A complete, deployed web application of your own design (a habit tracker
with analytics, a recipe planner, a small marketplace front end) built on
the component library from `accessible-component-library.md`, using the
state patterns from `data-driven-dashboard-ui.md`, with authentication
against a backend or a backend-as-a-service, a test suite, a Lighthouse
score you are proud of, and a public URL with error monitoring.

## Student-Scope Notes
- The backend may be a hosted service (Supabase, Firebase, PocketBase) or
  a simple API you or a teammate built. Backend engineering is not graded
  here.
- Scope to three to five screens done well. A polished small app beats a
  sprawling half-finished one.
- Error monitoring can be a free-tier hosted tool or a minimal
  window.onerror reporter to your backend.

## Steps
1. Write a one-page product brief and low-fidelity wireframes for every
   screen. List the components you need and which come from your library.
2. Set up the project with TypeScript, the component library, routing,
   and a server-state library. Add lint, type-check, and tests to CI from
   day one.
3. Implement authentication (sign up, sign in, protected routes, sign
   out) with a proper loading state while the session resolves.
4. Build the core screens with explicit loading, error, and empty states
   and URL-synced filters where relevant.
5. Run an accessibility pass: automated checks on every screen plus a
   manual keyboard and screen-reader walkthrough of the main flow. Fix
   what you find.
6. Run the performance audit from `web-performance-audit-and-fix.md` if
   you built it, or a minimal version: production build, Lighthouse,
   bundle analysis, and at least three fixes.
7. Add end-to-end tests for the critical path and deploy with preview
   builds per pull request and a production deploy on merge.
8. Add error monitoring, use the app for a week, fix what the monitoring
   surfaces, and write the portfolio README: brief, architecture, state
   model, accessibility and performance results, and live URL.

## Extension Ideas
- Add offline support with a service worker and background sync.
- Add internationalization for a second language.
- Add analytics events and a small funnel report.
- Add a public component playground built from your library.

## Skills Demonstrated
- End-to-end frontend product delivery from brief to deployed app
- Coherent state architecture across server, client, and URL
- Accessibility and performance as launch criteria
- CI with preview deployments and production monitoring

## Industry Relevance

Consumer Apps, SaaS, Digital Agencies. These employers hire frontend engineers to own features from design handoff to production, and a deployed app with real users, monitoring, and measured accessibility and performance results demonstrates that ownership more convincingly than any coding exercise.
