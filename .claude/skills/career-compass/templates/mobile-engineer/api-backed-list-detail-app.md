---
title: "API-Backed List and Detail App"
track: "mobile-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["mobile-development", "mobile-ui-patterns", "state-management", "automated-testing"]
skill_prerequisites: ["git-version-control", "http-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# API-Backed List and Detail App

## Production Workflow Mirrored
1. Structuring a mobile app with navigation, screens, and a data layer
2. Fetching from an API with loading, error, and empty states
3. Following the platform's UI conventions so the app feels native
4. Separating view code from state so it can be tested
5. Running unit and UI tests on a simulator or emulator

## What You'll Build
A two-screen mobile app (a list and a detail view) for a public API of
your choice (movies, recipes, transit, weather) on iOS (Swift/SwiftUI),
Android (Kotlin/Compose), or a cross-platform framework (React Native or
Flutter). The list paginates, pull-to-refresh works, tapping an item opens
a detail screen, and every network state is handled. The view model layer
has unit tests and the main flow has a UI test.

## Student-Scope Notes
- Choose one platform and commit for the whole track. The skills
  transfer; switching mid-track does not.
- No backend of your own; the point is consuming an API correctly on a
  device with unreliable connectivity.
- Design fidelity is "follows platform guidelines," not "pixel-perfect
  custom design."

## Steps
1. Sketch both screens and the navigation between them, and note which
   platform components (list, navigation bar, sheet) you will use.
2. Set up the project with a clear layering: networking, models, view
   models or state holders, and views.
3. Build the networking layer with typed models, timeouts, and error
   types the UI can distinguish (offline vs. server error vs. not found).
4. Build the list screen with pagination, pull-to-refresh, a loading
   indicator, an error state with retry, and an empty state.
5. Build the detail screen, pass the item identity through navigation,
   and load any additional detail from the API.
6. Test the app with the simulator's network conditioner or airplane
   mode and make every state look intentional.
7. Write unit tests for the view model (pagination logic, error mapping)
   with the network layer mocked, and one UI test that scrolls the list
   and opens a detail.
8. Write the README with screenshots, the architecture diagram, and a
   note on how each network failure is surfaced to the user.

## Extension Ideas
- Add search with debouncing and request cancellation.
- Add image caching and placeholder handling.
- Add a favorites list persisted locally.
- Add dark mode and dynamic type support.

## Skills Demonstrated
- Mobile app architecture with a testable state layer
- Networking on mobile with explicit failure handling
- Platform-conventional navigation and list UI
- Unit and UI testing on device or simulator

## Industry Relevance

Media, Retail, Travel. Consumer apps in these sectors are dominated by list-and-detail flows over APIs, and hiring managers use exactly this kind of small app as a take-home to see whether a candidate handles loading and failure states and structures code for testing. Building it well once means you have that answer ready.
