---
title: "LLM App Observability, Cost & Guardrails"
track: "ai-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["llm-observability", "eval-harnesses", "python", "api-design"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# LLM App Observability, Cost & Guardrails

## Production Workflow Mirrored
1. Instrumenting every LLM call with request/response logging
2. Tracking token usage and cost per request and per session
3. Tracking latency (including time-to-first-token for streaming)
4. Input/output guardrails (blocking disallowed input, filtering unsafe or
   off-policy output)
5. Aggregating logs into a dashboard for cost, latency, and guardrail-trip
   trends over time
6. Alerting when cost, latency, or guardrail-trip rate crosses a threshold

## What You'll Build
An observability layer wrapped around an existing LLM-powered app (yours
from an earlier template, or a small new one) that logs every call with
cost/latency/token counts, enforces input and output guardrails, and
surfaces the aggregated trends in a small dashboard you can point at when
asked "how much is this costing us and is it behaving?"

## Student-Scope Notes
- Logging goes to a local structured log file or lightweight database, not
  a production observability platform.
- Guardrails are a small set of concrete rules (a disallowed-topics list,
  a max-output-length check, a basic PII pattern filter), not a full
  content-safety model.
- The dashboard can be a script that reads the logs and prints/plots
  summary stats, not a hosted monitoring product.

## Steps
1. Pick an existing (or minimal new) LLM-powered app to instrument.
2. Wrap every LLM call with logging: timestamp, prompt/response (or a
   redacted summary), token counts, latency, and estimated cost.
3. Add an input guardrail that rejects or flags requests violating a
   defined policy (disallowed topics, injection attempts, malformed
   input).
4. Add an output guardrail that checks responses before they're returned
   (length limits, a basic PII pattern check, a disallowed-content check).
5. Aggregate logs into per-day/per-session summaries: total cost, average
   latency, guardrail-trip rate.
6. Build a small script or dashboard visualizing these trends over a
   period of simulated traffic.
7. Add a threshold-based alert (e.g. print/log a warning) when cost,
   latency, or guardrail-trip rate exceeds a configured limit.
8. Write up: what a real incident would have looked like in your logs, and
   how quickly your dashboard would have surfaced it.

## Extension Ideas
- Add per-user or per-feature cost attribution instead of just app-wide
  totals.
- Add a canary/shadow-eval hook that scores a sample of live traffic
  against your eval harness (pairs with the RAG template's eval suite).
- Add rate limiting tied to the same guardrail infrastructure.
- Send alerts to a real channel (email, Slack webhook) instead of just
  logging them.

## Skills Demonstrated
- LLM application observability: cost, latency, and usage tracking
- Guardrail design for input and output safety
- Operational dashboarding and threshold-based alerting
- Production-readiness instincts specific to LLM-powered applications
