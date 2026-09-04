---
title: "Data-Driven Dashboard with Async State"
track: "frontend-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["frontend-frameworks", "state-management", "browser-apis", "typescript", "data-visualization"]
skill_prerequisites: ["javascript", "html-css"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# Data-Driven Dashboard with Async State

## Production Workflow Mirrored
1. Fetching, caching, and refreshing server data in the client
2. Handling loading, error, empty, and stale states for every view
3. Filtering, sorting, and paginating large lists without freezing the UI
4. Rendering charts from live data with correct labelling
5. Persisting user preferences and deep-linkable filter state in the URL

## What You'll Build
A single-page dashboard in TypeScript and your chosen framework that
reads from a public or mock API (weather, GitHub, a JSON server you run),
shows a filterable and sortable table of at least a thousand rows, two
charts that respond to the same filters, and URL-synced filter state so a
link reproduces the exact view. Every async view handles loading, error,
and empty states explicitly.

## Student-Scope Notes
- Use a server-state library (TanStack Query, SWR, RTK Query, or the
  framework equivalent) rather than hand-rolled fetch-in-effect code, and
  be able to explain why.
- A thousand rows is enough to make naive rendering visibly slow; use
  windowing or pagination and measure the difference.
- Charts can use any mainstream library. Accessibility of the charts
  (labels, a data table alternative) counts.

## Steps
1. Define TypeScript types for the API responses and a typed client
   module with error handling for network and non-2xx responses.
2. Build the table with server-state fetching, a skeleton loading state,
   an error state with retry, and an empty state.
3. Add filtering and sorting driven from URL query parameters so the
   back button and shared links work.
4. Measure render time with the browser profiler at a thousand rows, then
   add virtualization or pagination and record the improvement.
5. Add two charts that share the filter state, with axis labels, a
   legend, and a visually hidden data table for screen readers.
6. Add background refetching and a stale indicator so the user knows when
   data is old, plus a manual refresh control.
7. Persist non-URL preferences (column visibility, theme) in localStorage
   with graceful fallback if storage is unavailable.
8. Write tests for the filter/sort logic and a component test for the
   loading, error, and empty states. Write up the state architecture:
   what lives in the URL, in server-state cache, and in local storage,
   and why.

## Extension Ideas
- Add optimistic updates for an editable cell with rollback on failure.
- Add request cancellation when filters change quickly.
- Add an export-to-CSV of the current filtered view.
- Add keyboard navigation for the table.

## Skills Demonstrated
- Server-state management with caching, refetching, and stale handling
- URL-driven application state and deep linking
- Rendering performance measurement and virtualization
- Typed API clients and explicit async UI states

## Industry Relevance

Analytics Products, Fintech, Operations Software. Internal tools and customer dashboards in these sectors are mostly tables, filters, and charts over slow APIs, and the frontend engineers who thrive are the ones who handle every async state and keep large lists responsive. This project mirrors the day-to-day work of those teams almost exactly.
