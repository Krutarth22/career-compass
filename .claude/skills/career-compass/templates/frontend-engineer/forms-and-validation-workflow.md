---
title: "Multi-Step Form with Validation and Autosave"
track: "frontend-engineer"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["frontend-frameworks", "state-management", "web-accessibility", "frontend-testing", "responsive-design"]
skill_prerequisites: ["javascript", "html-css"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Multi-Step Form with Validation and Autosave

## Production Workflow Mirrored
1. Modelling a complex form as a schema with per-field and cross-field rules
2. Validating on the client with clear, accessible error messaging
3. Persisting drafts so a refresh or crash does not lose work
4. Submitting to an API and handling server-side validation errors
5. Making the whole flow work on a phone and with a keyboard only

## What You'll Build
A multi-step form (an application, checkout, or onboarding flow) with at
least four steps and fifteen fields, schema-based validation including a
cross-field rule, async validation against an API (for example a username
availability check), autosaved drafts, a review step, and a responsive
layout. Server errors returned on submit map back to the right fields.

## Student-Scope Notes
- The backend is a mock server (MSW, json-server, or a tiny Express app)
  that returns realistic validation errors; you are not building the API.
- Use a form library appropriate to your framework and a schema library
  (zod, yup, valibot). Be able to explain what the library does for you.
- Draft persistence goes to localStorage. A synced server-side draft is
  an extension.

## Steps
1. Write the form schema first: every field, its type, its validation
   rules, and one cross-field rule (end date after start date, password
   confirmation, etc.).
2. Build the step navigation with progress indication, guarding forward
   navigation on invalid steps while always allowing backward.
3. Wire validation so errors appear on blur and on submit, are announced
   to screen readers, and are associated with their inputs via
   aria-describedby.
4. Add an async validator with debouncing, a pending indicator, and
   correct handling if the user changes the field while a check is in
   flight.
5. Add autosave: persist the draft on change with debouncing, restore it
   on load, and offer to discard it.
6. Add the review step and submit. Map server validation errors back to
   the correct fields and step, and jump the user there.
7. Make the layout responsive and confirm every step is completable by
   keyboard only and on a 360px-wide viewport.
8. Write tests for the validation rules, the async validator race, and
   the draft restore. Write up the state model: what lives in form
   state, what in the draft, and how server errors flow back.

## Extension Ideas
- Add conditional steps that appear based on earlier answers.
- Add file upload with progress and client-side size/type checks.
- Add internationalized error messages.
- Sync drafts to the server for cross-device resume.

## Skills Demonstrated
- Schema-driven form validation including async and cross-field rules
- Accessible error messaging and keyboard-complete flows
- Draft persistence and recovery
- Responsive layout for complex interactive UI

## Industry Relevance

Insurance, Banking, Government Services, Healthcare Intake. These sectors run on long forms, and abandonment, accessibility complaints, and data-quality problems all trace back to form UX. Frontend engineers who can build a form that validates clearly, never loses work, and passes accessibility review are in constant demand there.
