---
title: "End-to-End Business Analytics Capstone"
track: "data-analyst"
difficulty_tier: "advanced"
estimated_hours: 25
role: "capstone"
skill_tags: ["sql", "business-intelligence-tools", "stakeholder-communication", "data-storytelling", "database-design", "data-visualization"]
skill_prerequisites: ["sql", "business-intelligence-tools"]
project_prerequisites: ["sql-analytics-deep-dive.md", "bi-dashboard-build.md"]
prerequisite_learning_hours: 5
---

# End-to-End Business Analytics Capstone

## Production Workflow Mirrored
1. SQL-driven data preparation feeding a live, reusable data model (not
   one-off queries)
2. That model powering an interactive BI dashboard directly, with no manual
   copy-paste step between analysis and presentation layer
3. A defined refresh path so the dashboard reflects new data without being
   rebuilt from scratch
4. Operational readiness: documented schema, query performance sanity
   checks, and a data-quality check layer before numbers reach the
   dashboard
5. A stakeholder presentation that ties the underlying analysis to the live
   dashboard and to a concrete recommendation

## What You'll Build
An integrated, end-to-end analytics deliverable that takes the SQL query
library and schema understanding you built in `sql-analytics-deep-dive.md`
and turns it into the data layer for a live dashboard built with the same
practices as `bi-dashboard-build.md` — one connected system, not two
side-by-side projects. You'll build a small set of SQL views that answer
the business's core questions, connect those views directly to a BI tool as
the dashboard's data source, and deliver the whole thing with a stakeholder
presentation that walks from the business question through the SQL logic to
the dashboard and lands on a recommendation.

## Student-Scope Notes
- This capstone assumes you completed both prerequisite projects; it does
  not re-teach SQL fundamentals or BI-tool basics — it's about wiring a
  query layer and a presentation layer together into one coherent pipeline,
  and about the data-quality and refresh discipline that gap requires.
- "Refresh path" means a documented, re-runnable process (re-run the SQL
  views against a new data extract, re-point or refresh the BI tool's
  connection) — not a scheduled production ETL job with orchestration
  tooling; that operational maturity is out of scope here.
- Data-quality checks are a focused set (row-count sanity, null checks on
  key join columns, duplicate-key checks) run before the dashboard is
  trusted, not a full data-quality framework.
- One business domain, one integrated dashboard-plus-query-layer — the
  point is depth and coherence of the full pipeline, not breadth across
  multiple business areas.

## Steps
1. Pick one business domain and write the 3-5 core questions this capstone
   needs to answer end-to-end (draw on the kinds of questions from the SQL
   deep-dive, but this time they must all serve one coherent dashboard, not
   be independent exercises).
2. Design a small set of SQL views (not one-off queries) that each answer
   one core question or one KPI, written so a BI tool can query them
   directly without further transformation. Reuse and refine query patterns
   (CTEs, window functions) from your SQL deep-dive project.
3. Add a data-quality check layer: queries that verify row counts look
   reasonable, key join columns aren't unexpectedly null, and no primary
   key is duplicated in the views feeding the dashboard. Run these before
   trusting any downstream number.
4. Connect your BI tool directly to these SQL views (live database
   connection or a scheduled extract) rather than a hand-exported CSV — the
   dashboard's data source should be the query layer itself.
5. Build the dashboard on top of this connected data layer, reusing the
   design discipline from your BI dashboard project: top-level KPI view,
   at least one drill-down path, and consistent visual encoding across
   views.
6. Simulate a data refresh: get a second extract/snapshot of the source
   data (later date range, or regenerate simulated data forward one
   period), re-run your SQL views and data-quality checks against it, and
   confirm the dashboard updates correctly without being rebuilt.
7. Document the full pipeline: schema/ER diagram, what each SQL view
   computes and why, the data-quality checks in place, and the refresh
   procedure — written so another analyst could pick this up and run it.
8. Build the stakeholder presentation: start from the business questions,
   show the SQL logic behind the key numbers (briefly, for credibility),
   walk through the live dashboard, and end on a concrete, numbers-backed
   recommendation.
9. Do a final end-to-end dry run: from a cold start, can you re-run the SQL
   views, pass the data-quality checks, refresh the dashboard, and deliver
   the presentation without any manual patching of numbers? Fix anything
   that breaks this chain.

## Extension Ideas
- Extend the dashboard with an A/B-test results panel, pulling in the
  significance-testing approach from `ab-test-analysis.md` to show a live
  experiment's status alongside the core business metrics.
- Add a cohort-retention or funnel view to the dashboard using the SQL and
  visualization patterns from `cohort-and-funnel-analysis.md`, for readers
  who want to push the capstone into behavioral analytics as well as
  business reporting.
- Add basic query-performance notes (execution plan review, an index you'd
  add) for the views under real production data volume.
- Add a lightweight alerting rule (e.g. flag in the write-up what dashboard
  value would trigger stakeholder outreach) to show operational thinking
  beyond the one-time analysis.

## Skills Demonstrated
- End-to-end integration of a SQL data layer with a live BI dashboard
- Data-quality and refresh discipline connecting analysis to presentation
- Schema design and documentation for a reusable query layer
- Portfolio-level stakeholder communication connecting query logic,
  dashboard, and business recommendation into one narrative

## Industry Relevance

Retail Operations, SaaS, Financial Reporting. Any business that reports metrics on a recurring cadence needs the query layer and the dashboard connected end to end, with data-quality checks in between, so leadership isn't looking at numbers a human manually patched before every meeting. This capstone's focus on a live SQL-to-dashboard pipeline with a documented refresh path mirrors the analytics-engineering responsibility many analyst roles in these industries actually own, not just the one-off analysis.
