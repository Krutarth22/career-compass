---
title: "End-to-End CRUD App with Auth"
track: "full-stack-engineer"
difficulty_tier: "beginner"
estimated_hours: 16
role: "core"
skill_tags: ["frontend-frameworks", "backend-frameworks", "api-design", "relational-databases", "authentication-authorization"]
skill_prerequisites: ["javascript", "html-css", "http-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# End-to-End CRUD App with Auth

## Production Workflow Mirrored
1. Defining a data model and an API contract shared by client and server
2. Implementing the server with persistence and authentication
3. Implementing the client against the contract with proper async states
4. Running both locally with one command
5. Writing tests on both sides of the contract

## What You'll Build
A complete web application with a browser client and an HTTP API you
both wrote: users sign up and log in, create and manage records for a
domain of your choice (notes, bookmarks, workouts, inventory), and only
see their own data. The client and server share a typed contract, the
whole stack runs with one command, and both sides have tests.

## Student-Scope Notes
- Pick one stack and stay in it: TypeScript end to end (Next.js or
  Express plus React), Python plus a JS client (FastAPI plus React), or a
  batteries-included framework (Rails, Django plus HTMX). Each is
  respected.
- The database is local Postgres or SQLite. Deployment is covered in a
  later template.
- Auth is session or JWT based; skip social login for the core build.

## Steps
1. Design the data model (two related entities) and write the API
   contract: every endpoint with request and response shapes. If your
   stack allows, generate types from it (OpenAPI, tRPC, or shared TS
   types).
2. Implement the server: schema, migrations, CRUD endpoints, registration
   and login with hashed passwords, and ownership checks on every
   resource.
3. Write server tests covering authentication failures, ownership
   violations, and validation errors.
4. Implement the client: auth screens, a protected area, list and detail
   views, create and edit forms, with loading, error, and empty states.
5. Wire the client to the API through a single typed client module so a
   contract change breaks the build, not production.
6. Add a one-command local setup (docker-compose or a dev script) that
   starts the database, server, and client.
7. Write client tests for the forms and a component test with the API
   mocked at the network layer.
8. Write the README: architecture diagram, the contract, how auth works
   across the boundary, and how to run it.

## Extension Ideas
- Add server-side pagination and search with URL-synced state.
- Add optimistic updates on the client with rollback.
- Add a shared validation schema used by both client and server.
- Add role-based access with an admin view.

## Skills Demonstrated
- Full-stack data modelling and API contract design
- Authentication that spans client and server
- Typed client-server integration
- Testing on both sides of the HTTP boundary

## Industry Relevance

Startups, SaaS, Digital Agencies. Small product teams hire full-stack engineers to take a feature from database to screen without handoffs, and this project is the canonical proof: an authenticated CRUD app where you can explain every layer. It is also the base every later template in this track builds on.
