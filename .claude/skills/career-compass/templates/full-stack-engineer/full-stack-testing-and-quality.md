---
title: "Full-Stack Test Suite and Quality Gates"
track: "full-stack-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["automated-testing", "end-to-end-testing", "ci-cd", "test-strategy"]
skill_prerequisites: ["javascript", "backend-frameworks"]
project_prerequisites: ["crud-app-end-to-end.md"]
prerequisite_learning_hours: 2
---

# Full-Stack Test Suite and Quality Gates

## Production Workflow Mirrored
1. Deciding what to test at the unit, API, component, and end-to-end levels
2. Running API tests against a real database in CI
3. Running browser tests against the full stack, not a mocked client
4. Enforcing quality gates: lint, types, coverage thresholds, and E2E on
   every pull request
5. Keeping the suite fast with parallelism and sharding

## What You'll Build
A layered test suite for the app from `crud-app-end-to-end.md`: unit
tests for domain logic on both sides, API tests that hit a real test
database, component tests with the network mocked, and a Playwright or
Cypress suite that drives the real client against the real server, all
enforced as CI gates with coverage thresholds and a readable report.

## Student-Scope Notes
- A small number of end-to-end tests over the critical journeys is the
  target. The exercise is choosing the right level for each behavior.
- Use a throwaway database per CI run (a service container) and seed it
  with fixtures.
- Cross-browser grids and visual regression are extensions.

## Steps
1. Write a one-page test strategy mapping each behavior to a level and
   listing the critical user journeys for end-to-end coverage.
2. Write unit tests for pure logic on the server (validation, business
   rules) and the client (formatters, reducers).
3. Write API tests that start the server against a real test database,
   seed fixtures, and cover auth failures, ownership, validation, and the
   happy paths.
4. Write component tests with the network mocked at the request level.
5. Write end-to-end tests that sign up, create, edit, and delete a record
   through the browser against the full stack, using role and label
   selectors.
6. Configure CI: lint, type-check, unit and API tests with a database
   service container, coverage thresholds that fail the build, then the
   E2E suite against a production build with the report uploaded as an
   artifact.
7. Introduce a deliberate bug on a branch at each level and confirm the
   right test catches it with a clear failure message.
8. Measure total pipeline time, shard or parallelize the slowest stage,
   and write up the strategy, the numbers, and your flakiness policy.

## Extension Ideas
- Add contract tests that verify the client's expectations against the
  server's OpenAPI spec.
- Add mutation testing to check the suite's strength.
- Add visual regression snapshots for key screens.
- Add a nightly job that runs the E2E suite against staging.

## Skills Demonstrated
- Test strategy across the full stack
- API testing against real databases in CI
- End-to-end testing of a complete application
- Quality gates and pipeline performance

## Industry Relevance

SaaS, Fintech, Healthcare Software. Teams in these sectors deploy continuously and cannot do so without trustworthy automated suites, and full-stack hires are expected to test across the boundary rather than only on their preferred side. A repository with layered tests and enforced gates answers the question directly.
