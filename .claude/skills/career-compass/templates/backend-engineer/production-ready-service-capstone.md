---
title: "Production-Ready Service Capstone"
track: "backend-engineer"
difficulty_tier: "advanced"
estimated_hours: 26
role: "capstone"
skill_tags: ["system-design", "api-design", "message-queues", "observability", "docker", "ci-cd", "technical-documentation"]
skill_prerequisites: ["backend-frameworks", "relational-databases", "automated-testing"]
project_prerequisites: ["rest-api-with-auth.md", "async-job-queue-and-workers.md"]
prerequisite_learning_hours: 5
---

# Production-Ready Service Capstone

## Production Workflow Mirrored
1. Writing a design document with requirements, data model, API, and
   failure modes before building
2. Composing API, worker, queue, cache, and database into one deployable
   system
3. Continuous integration that lints, tests, builds an image, and blocks
   merges on failure
4. Health checks, graceful shutdown, configuration via environment, and
   secrets kept out of the repo
5. Deploying to a real host and operating it with logs and metrics
6. A runbook a teammate could use at 3am

## What You'll Build
Combine the API from `rest-api-with-auth.md` and the job system from
`async-job-queue-and-workers.md` into one cohesive product-style service
-- for example an order system that accepts orders, charges a stubbed
payment provider asynchronously, and notifies the user -- with a design
doc, a CI pipeline, containerized deployment to a cloud host, health
endpoints, observability, and a runbook.

## Student-Scope Notes
- "Cloud host" means a single small VM or a container platform with a
  free tier (Fly.io, Render, Railway, a tiny EC2/GCE instance). No
  Kubernetes required.
- The payment provider is a stub with injectable failures, consistent
  with the job-queue template.
- The design doc is 2-4 pages. The point is that decisions are written
  down before the code, not that it is long.

## Steps
1. Write the design doc: user stories, non-functional requirements
   (latency target, availability target), ER diagram, endpoint list,
   sequence diagram for the async flow, and a failure-modes table.
2. Integrate the API and worker into one repository with docker-compose
   for local development, a single configuration module that reads
   environment variables, and a `.env.example` with no real secrets.
3. Add a liveness endpoint and a readiness endpoint that checks the
   database and queue connections. Add graceful shutdown to both API and
   worker.
4. Set up CI: lint, type-check where applicable, run the full test suite
   against a real database service, build the container image, and fail
   the pipeline on any error.
5. Deploy the API, worker, queue, and database to your chosen host.
   Confirm the readiness check passes from outside and that a job
   enqueued via the public URL completes.
6. Wire the observability from `observability-and-load-testing.md` if you
   built it, or a minimal version: structured logs and request metrics
   visible on the host.
7. Run a load test against the deployed service, and inject one failure
   (kill the worker, stop the queue) to confirm the system degrades the
   way the design doc predicted.
8. Write the runbook: how to deploy, roll back, read logs, check queue
   depth, and recover from each failure mode in the design doc's table.
   Then write a portfolio README linking the design doc, runbook, CI
   badge, and live URL.

## Extension Ideas
- Add a blue/green or rolling deploy and prove zero failed requests
  during a deploy under load.
- Add a second service that consumes domain events from the queue and
  document the contract between them.
- Add database backups and a tested restore procedure.

## Skills Demonstrated
- System design communicated in a written design document
- Composing API, worker, queue, cache, and database into one deployable
  system
- CI pipeline design and container-based deployment
- Operational readiness: health checks, graceful shutdown, runbooks

## Industry Relevance

SaaS, Fintech, Marketplaces. Companies in these sectors hire backend engineers to own services end to end, from design doc through on-call, and interview loops increasingly ask candidates to walk through a system they shipped, including what failed and how they operated it. A deployed service with a design doc, CI, and a runbook is a stronger portfolio piece than any number of tutorial apps.
