---
title: "Frontend Test Suite and CI Pipeline"
track: "frontend-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["frontend-testing", "end-to-end-testing", "ci-cd", "automated-testing"]
skill_prerequisites: ["javascript", "frontend-frameworks"]
project_prerequisites: ["forms-and-validation-workflow.md"]
prerequisite_learning_hours: 3
---

# Frontend Test Suite and CI Pipeline

## Production Workflow Mirrored
1. Choosing what to test at each level: unit, component, end-to-end
2. Mocking the network at the boundary rather than mocking modules
3. Writing end-to-end tests that survive UI refactors
4. Running lint, type-check, tests, and a build on every pull request
5. Keeping the suite fast and flake-free enough that people trust it

## What You'll Build
A layered test suite for the form from `forms-and-validation-workflow.md`
(or another app you built in this track): unit tests for pure logic,
component tests with network mocking, and a small end-to-end suite in
Playwright or Cypress covering the critical path, all wired into a CI
pipeline that runs on every push with a coverage report and an artifact
of the built app.

## Student-Scope Notes
- Aim for a handful of end-to-end tests over the critical path, not
  hundreds. E2E tests are expensive; the exercise is choosing well.
- Use a network mocking layer (MSW or the framework equivalent) so
  component tests never hit a real server.
- CI is GitHub Actions or the equivalent free tier. Cross-browser cloud
  grids are out of scope.

## Steps
1. Write a short test strategy: which behaviors are covered at which
   level and why. Identify the three to five critical-path user journeys.
2. Write unit tests for pure logic (validation rules, formatting,
   reducers) and reach high coverage on those modules.
3. Write component tests that render real components, mock the network
   at the request level, and assert on what the user sees, not on
   implementation details.
4. Write end-to-end tests for the critical paths using resilient
   selectors (roles and labels, not CSS classes), including one test that
   proves a server validation error surfaces correctly.
5. Set up CI: install, lint, type-check, unit and component tests with
   coverage, then the E2E suite against a production build, then upload
   the build and the Playwright report as artifacts.
6. Deliberately introduce a regression on a branch and confirm CI blocks
   it with a readable failure.
7. Measure suite runtime and parallelize or shard the E2E stage if it
   exceeds a few minutes.
8. Write up the strategy, the runtime numbers, and how you would keep
   flakiness out of the suite as it grows.

## Extension Ideas
- Add visual regression snapshots for key screens.
- Add accessibility assertions to the E2E suite.
- Add preview deployments per pull request and run E2E against them.
- Add a flaky-test quarantine and retry policy.

## Skills Demonstrated
- Test strategy across unit, component, and end-to-end levels
- Network mocking at the boundary
- Resilient end-to-end test authoring
- CI pipeline design for frontend applications

## Industry Relevance

SaaS, E-commerce, Fintech. Frontend teams in these sectors ship many times a day and rely on automated suites to do it safely, so hiring loops ask candidates how they decide what to test and how they keep pipelines fast. A repository with a layered suite and a green CI history is direct evidence.
