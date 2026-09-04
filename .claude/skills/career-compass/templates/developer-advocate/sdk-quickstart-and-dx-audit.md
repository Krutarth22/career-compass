---
title: "SDK Quickstart and Developer Experience Audit"
track: "developer-advocate"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["developer-experience", "api-design", "technical-documentation", "user-research"]
skill_prerequisites: ["python", "javascript"]
project_prerequisites: []
prerequisite_learning_hours: 2
---

# SDK Quickstart and Developer Experience Audit

## Production Workflow Mirrored
1. Measuring time-to-first-success for a new developer on a product
2. Observing real developers onboarding and cataloguing friction
3. Prioritizing fixes across docs, SDK, errors, and dashboard
4. Shipping a quickstart that gets developers to success fast
5. Feeding the friction log to product and engineering with evidence

## What You'll Build
A developer experience audit of a real API or SDK: a measured baseline
of time-to-first-successful-call from a clean machine, recorded
onboarding sessions with at least three developers, a prioritized
friction log with evidence, a rewritten quickstart in two languages
that measurably reduces time-to-first-success, and a report to the
product team with specific SDK and error-message recommendations.

## Student-Scope Notes
- Choose a product with a public API and SDK; open-source projects and
  free-tier APIs are both fine.
- Onboarding sessions are think-aloud sessions you observe without
  helping, recorded with consent.
- The quickstart must be tested from a clean environment (a fresh
  container or VM) before and after.

## Steps
1. Run the existing quickstart yourself from a clean environment, timing
   each step and logging every friction point and confusing error.
2. Recruit three developers matching the target audience and run
   think-aloud onboarding sessions, timing to first successful call.
3. Build the friction log: each issue, where it occurred, how many
   participants hit it, severity, and evidence (quotes, screenshots).
4. Prioritize by frequency and severity and categorize by owner: docs,
   SDK, API errors, dashboard, or auth flow.
5. Rewrite the quickstart in two languages: minimal prerequisites,
   copy-paste steps, expected output at each step, and the top three
   errors with fixes.
6. Test the new quickstart from a clean environment and with two new
   developers, measuring time-to-first-success again.
7. Write the recommendations for product and engineering: SDK
   ergonomics, error messages with suggested text, and dashboard
   changes, each tied to friction-log evidence.
8. Publish the quickstart (or submit it upstream) and write up the
   before-and-after metrics and the report.

## Extension Ideas
- Contribute an SDK improvement (better error, helper method) upstream.
- Build a CLI that automates the quickstart's setup steps.
- Run the audit quarterly and track the metric over time.
- Add an onboarding funnel analysis from product analytics.

## Skills Demonstrated
- Developer onboarding research and measurement
- Friction analysis with evidence and prioritization
- Quickstart writing validated by time-to-first-success
- Product feedback grounded in observed developer behavior

## Industry Relevance

API Platforms, Developer Tools, Cloud Providers. Time-to-first-success is a tracked metric in these sectors, and developer advocates are expected to own it with research and writing rather than opinion. An audit with recorded sessions and a measured improvement is the kind of work sample DevRel hiring managers ask to see.
