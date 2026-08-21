---
title: "Cohort Retention and Funnel Drop-Off Analysis"
track: "data-analyst"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["sql", "statistics", "data-visualization"]
skill_prerequisites: ["sql", "statistics"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# Cohort Retention and Funnel Drop-Off Analysis

## Production Workflow Mirrored
1. Define the cohorting logic and the funnel steps that matter for the
   product
2. Query raw event/transaction data into a cohort-by-period retention
   structure
3. Query the same event data into a step-by-step funnel structure
4. Visualize both as a retention curve/heatmap and a funnel chart
5. Diagnose where and for whom the biggest drop-offs happen
6. Turn the diagnosis into a prioritized, actionable recommendation

## What You'll Build
A retention and funnel analysis for a product with an event log (e.g. a
mobile app's signup-to-purchase funnel, a SaaS product's onboarding funnel,
or an e-commerce site's browse-to-checkout funnel). The deliverable is a
cohort retention heatmap (by signup month or week), a step-by-step
conversion funnel with drop-off rates at each stage, and a written diagnosis
of the biggest opportunity for improvement, all built primarily with SQL
against an events table.

## Student-Scope Notes
- One retention definition (e.g. "returned and performed the key action")
  and one primary funnel, not a full metrics-layer covering every possible
  cohort cut or funnel variant a real product team would eventually build.
- Event data can be a public app-events dataset or a plausible simulated
  event log (user_id, event_name, timestamp, plus 1-2 dimensions like
  platform or acquisition channel) — the SQL and analytical patterns are
  identical either way.
- Statistical significance testing on drop-off differences between segments
  is a light touch (a proportion comparison), not a full experiment design
  — that rigor lives in the A/B-test template.
- No causal claims are required about *why* a segment retains worse; the
  deliverable is a well-evidenced diagnosis and hypothesis, not a proven
  causal mechanism.

## Steps
1. Get or simulate an event log with at minimum: user_id, event_name,
   event_timestamp, and a signup/first-seen date per user.
2. Define retention precisely for this product: what event counts as
   "active" or "retained" in a given period, and what period granularity
   (weekly is usually right for apps; monthly for lower-frequency products).
3. Write the cohort SQL: assign each user to a cohort by signup week/month,
   then for each cohort compute the % of users active in period 0, 1, 2,
   3... since signup, using a self-join or window functions against the
   event table.
4. Build a cohort retention heatmap (cohort on one axis, period-since-signup
   on the other, retention % as the color/value) and identify which
   cohorts retain meaningfully better or worse than others.
5. Define the funnel: pick 4-6 sequential steps a user takes toward the key
   outcome (e.g. app_open -> signup -> add_to_cart -> checkout_start ->
   purchase).
6. Write the funnel SQL: for each step, count distinct users who reached it,
   and compute step-over-step conversion rate and overall funnel conversion
   from step 1.
7. Segment the funnel by 1-2 dimensions (e.g. acquisition channel, device
   type) and identify which segment has the worst drop-off at which
   specific step — not just an overall weak step.
8. Cross-reference the two analyses: does the segment with the worst funnel
   conversion also retain worse long-term, or are they different problems?
9. Write the diagnosis: the single biggest drop-off point, who it affects
   most, a plausible reason backed by the data (not speculation alone), and
   a prioritized recommendation for what to test or fix first.

## Extension Ideas
- Add a cohort-by-acquisition-channel retention comparison, not just
  cohort-by-signup-date.
- Build a "time to second purchase/action" distribution alongside the
  binary retention curve for a richer view of engagement.
- Model expected funnel conversion using a simple Markov-chain / transition
  matrix approach and compare it to the observed funnel.
- Automate the cohort/funnel queries into parameterized SQL that could
  regenerate the analysis for any date range.

## Skills Demonstrated
- Advanced SQL for cohort and funnel construction from raw event data
- Retention and funnel analysis frameworks
- Segmentation-driven diagnosis of product/business problems
- Data visualization (heatmaps, funnel charts) for behavioral data

## Industry Relevance

Mobile Apps, SaaS, Consumer Subscriptions. Product and growth teams in these sectors live or die by retention and conversion — a subscription business that doesn't know which cohort churns fastest or where users abandon signup is flying blind on its biggest cost driver. The SQL-driven cohort retention and funnel drop-off analysis this project builds is the exact diagnostic work growth and product analytics teams run every week to find where to invest engineering and marketing effort next.
