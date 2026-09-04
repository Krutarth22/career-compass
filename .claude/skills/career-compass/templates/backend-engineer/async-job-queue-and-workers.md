---
title: "Background Job Queue with Workers and Retries"
track: "backend-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["background-jobs", "message-queues", "concurrency", "observability"]
skill_prerequisites: ["backend-frameworks", "docker"]
project_prerequisites: ["rest-api-with-auth.md"]
prerequisite_learning_hours: 4
---

# Background Job Queue with Workers and Retries

## Production Workflow Mirrored
1. Moving slow or failure-prone work (emails, exports, third-party calls)
   out of the request path
2. Enqueuing jobs durably so they survive a process crash
3. Running worker processes that consume, execute, and acknowledge jobs
4. Retrying with backoff, dead-lettering poison messages, and making jobs
   idempotent
5. Exposing job status to the client and metrics to operators

## What You'll Build
An asynchronous processing system attached to the API from
`rest-api-with-auth.md`: an endpoint that enqueues a long-running task
(for example, generating a report or calling a slow external service),
one or more worker processes that consume from a durable queue (Redis,
RabbitMQ, or a database-backed queue), retries with exponential backoff, a
dead-letter queue, and a status endpoint the client polls.

## Student-Scope Notes
- Use a library appropriate to your stack (Celery, RQ, BullMQ, Sidekiq)
  or a hand-rolled queue on Postgres with SKIP LOCKED. A hand-rolled
  queue teaches more; a library ships faster. Either is acceptable.
- "Slow external service" can be a stub that sleeps and randomly fails.
  The failure injection is the point.
- Run everything with docker-compose: API, worker, queue, database.

## Steps
1. Identify one operation in your API that should not run inline and
   define the job payload as a small, serializable schema.
2. Add the queue infrastructure to docker-compose and an enqueue call in
   the API that returns 202 with a job id.
3. Write a worker that consumes jobs, executes them, and acknowledges only
   on success. Kill the worker mid-job and confirm the job is redelivered.
4. Add retries with exponential backoff and jitter, capped at a maximum
   attempt count, then route exhausted jobs to a dead-letter queue.
5. Make the job idempotent: running it twice must not produce two side
   effects. Write a test that delivers the same job twice and checks.
6. Add a status endpoint (queued, running, succeeded, failed, attempts)
   backed by a job-state table.
7. Add structured logs with the job id on every line and a metrics
   counter for succeeded, failed, and retried jobs. Run two workers
   concurrently and confirm no job is processed twice.
8. Write up: the delivery guarantee you actually provide (at-least-once),
   how idempotency makes that safe, and what the dead-letter queue is for.

## Extension Ideas
- Add scheduled (delayed) jobs and a periodic job.
- Add a priority queue and prove high-priority jobs jump the line.
- Add graceful shutdown so a worker finishes its current job on SIGTERM.
- Replace polling with a webhook or server-sent event on completion.

## Skills Demonstrated
- Asynchronous job processing with durable queues
- Retry, backoff, and dead-letter design
- Idempotency and at-least-once delivery reasoning
- Concurrent workers with structured logging and metrics

## Industry Relevance

Fintech, Logistics, Marketing Technology. Payment reconciliation, shipment updates, and bulk email all run as background jobs, and the difference between a reliable system and a support nightmare is whether retries are safe and poison messages are isolated. This project demonstrates the exact at-least-once plus idempotency reasoning that backend interviews in these sectors test for.
