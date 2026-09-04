---
title: "Observability and Load Testing for a Service"
track: "backend-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["observability", "performance-testing", "performance-profiling", "docker"]
skill_prerequisites: ["backend-frameworks", "linux-cli"]
project_prerequisites: ["rest-api-with-auth.md"]
prerequisite_learning_hours: 4
---

# Observability and Load Testing for a Service

## Production Workflow Mirrored
1. Instrumenting a service with structured logs, metrics, and traces
2. Standing up a local metrics and dashboard stack
3. Defining a load profile and running a repeatable load test
4. Finding the bottleneck from the telemetry, not from guessing
5. Fixing it and proving the fix with the same load test

## What You'll Build
The API from `rest-api-with-auth.md` instrumented with structured JSON
logs carrying a request id, Prometheus-style metrics (request count,
latency histogram, error rate, database pool usage), and OpenTelemetry
traces, plus a Grafana dashboard and a k6 or locust load test. You will
use the telemetry to locate one real bottleneck, fix it, and show the
before/after.

## Student-Scope Notes
- The observability stack (Prometheus, Grafana, an OTel collector or
  Jaeger) runs in docker-compose on your laptop. No hosted vendor
  required.
- The load test runs from the same machine; absolute numbers are not the
  point, relative before/after under the same conditions is.
- One bottleneck is enough. An N+1 query, a missing index, or a
  synchronous external call are all realistic candidates.

## Steps
1. Add a request-id middleware and switch logging to structured JSON with
   method, path, status, latency, and the request id on every line.
2. Expose a metrics endpoint with a request counter, a latency histogram
   labeled by route and status, and a gauge for database pool usage.
3. Add tracing so each request produces a trace with spans for the
   handler and every database query.
4. Add Prometheus, Grafana, and a trace backend to docker-compose. Build a
   dashboard with request rate, p95 latency, error rate, and pool usage.
5. Write a load test with a realistic mix (mostly reads, some writes,
   some auth failures) and a ramp to a fixed concurrency.
6. Run it, watch the dashboard, and open the slowest traces. Identify one
   concrete bottleneck and document the evidence.
7. Fix the bottleneck and re-run the identical load test. Capture the
   before/after p95 and error rate.
8. Write up: the three signals, how each pointed at (or ruled out) the
   bottleneck, and what alert thresholds you would set from these
   numbers.

## Extension Ideas
- Add an alert rule for p95 latency and error rate and test it by
  injecting a fault.
- Add a service-level objective and compute the error budget from the
  metrics.
- Add log-to-trace correlation so a log line links to its trace.

## Skills Demonstrated
- Structured logging, metrics, and distributed tracing in one service
- Standing up a local observability stack
- Designing and running repeatable load tests
- Evidence-driven performance debugging

## Industry Relevance

Cloud Infrastructure, Fintech, Streaming Media. Any team running a service that people depend on needs engineers who can answer "why is it slow" with a trace rather than a hunch. On-call readiness and load-test discipline are explicit hiring signals for backend roles at scale-focused companies in these sectors.
