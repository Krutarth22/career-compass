---
title: "REST API with Authentication and Tests"
track: "backend-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["api-design", "backend-frameworks", "authentication-authorization", "relational-databases", "automated-testing"]
skill_prerequisites: ["http-fundamentals", "git-version-control"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# REST API with Authentication and Tests

## Production Workflow Mirrored
1. Designing resource-oriented endpoints and a versioned URL scheme
2. Persisting resources in a relational database behind a data-access layer
3. Registering users, hashing passwords, and issuing session or token credentials
4. Protecting endpoints with authentication and per-resource authorization
5. Writing an automated test suite that runs on every change
6. Documenting the API so another engineer can integrate without reading the code

## What You'll Build
A small but complete HTTP API in the backend framework of your choice
(FastAPI, Django REST, Express, Spring Boot, Rails) for a domain with two
related resources -- for example projects and tasks, or authors and posts.
Users register and log in, receive a token, and can only read or modify
the resources they own. Every endpoint has automated tests, and the API is
documented with an OpenAPI spec or equivalent.

## Student-Scope Notes
- The database is a local Postgres in Docker or SQLite; you are learning
  the data-access and auth patterns, not operating a managed database.
- Token auth is a signed JWT or a server-side session -- either is fine.
  Skip refresh tokens, OAuth providers, and MFA for the core build.
- "Deploy" is not required here; the production-ready-service capstone
  covers that. Run it locally and prove it works with the test suite.

## Steps
1. Sketch the resource model (two related entities with a one-to-many
   relationship) and write out every endpoint with method, path, request
   body, response body, and status codes before writing code.
2. Scaffold the project, connect it to the database, and implement the two
   resources with create, read (list and single), update, and delete.
3. Add user registration and login: hash passwords with bcrypt or argon2,
   issue a token on login, and reject invalid credentials with the correct
   status code.
4. Add an authentication dependency or middleware that resolves the token
   to a user on every protected route.
5. Add authorization: a user can only read or modify their own resources.
   Return 403 rather than 404 when they hit someone else's, and document
   why you chose that.
6. Write tests covering the happy path and at least three failure modes
   per resource (unauthenticated, wrong owner, invalid payload). Run them
   in CI or a pre-commit hook.
7. Generate or hand-write an OpenAPI document and confirm it matches the
   real behavior by exercising every endpoint from the docs UI or curl.
8. Write a README explaining the auth flow with a sequence diagram and how
   to run the tests.

## Extension Ideas
- Add pagination, filtering, and sorting to the list endpoints with a
  consistent query-parameter convention.
- Add refresh tokens and token revocation.
- Add a role (admin) that can read all resources, and tests that prove the
  boundary holds.
- Add request validation error responses that follow RFC 9457 problem
  details.

## Skills Demonstrated
- Resource-oriented REST API design with correct status codes
- Password hashing and token-based authentication
- Ownership-based authorization and the tests that prove it
- A maintainable test suite for an HTTP service

## Industry Relevance

SaaS, Fintech, E-commerce. Nearly every product company runs on authenticated HTTP APIs, and backend interview loops routinely probe whether a candidate can explain auth flows, ownership checks, and why an endpoint returns 403 versus 404. This project produces exactly the artifact hiring managers ask to see: a small service where the auth boundary is designed deliberately and proven by tests.
