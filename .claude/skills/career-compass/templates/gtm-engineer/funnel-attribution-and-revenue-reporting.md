---
title: "Funnel, Attribution, and Revenue Reporting"
track: "gtm-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["marketing-attribution", "sql", "data-visualization", "business-intelligence-tools", "data-modeling"]
skill_prerequisites: ["sql"]
project_prerequisites: ["crm-data-model-and-hygiene.md"]
prerequisite_learning_hours: 3
---

# Funnel, Attribution, and Revenue Reporting

## Production Workflow Mirrored
1. Modeling the funnel from first touch to closed revenue across systems
2. Joining marketing, product, and CRM data on consistent identities
3. Implementing attribution models and explaining their differences
4. Building the dashboards revenue leaders run their week on
5. Reconciling reported pipeline and revenue with the source of truth

## What You'll Build
A revenue analytics layer over your CRM and a marketing or product event
source: SQL models producing a unified touchpoint and opportunity
timeline, funnel conversion by stage and segment with velocity, three
attribution models (first touch, last touch, and a multi-touch
variant) with a comparison, a pipeline and forecast view, and a
dashboard reconciled to CRM totals.

## Student-Scope Notes
- Use DuckDB or Postgres with dbt or plain SQL models, and any BI tool
  with a free tier.
- Marketing and product events can be synthetic but must be generated
  with realistic identity gaps (anonymous to known transitions) so
  identity resolution is a real problem.
- Three attribution models compared honestly is worth more than a
  sophisticated one presented alone.

## Steps
1. Document the funnel definition with stage criteria and the systems
   each stage lives in.
2. Extract CRM objects and event data into the warehouse and build
   staging models with consistent keys.
3. Build identity resolution: link anonymous events to known contacts
   and contacts to accounts, and measure the match rate.
4. Build the touchpoint timeline per opportunity and the funnel model
   with stage conversion rates, velocity, and segment breakdowns.
5. Implement the three attribution models over the timeline and produce
   a comparison of channel credit under each.
6. Build the pipeline view (open pipeline by stage and close date) and
   a simple forecast (weighted by stage probability).
7. Build the dashboard and reconcile every headline number to the CRM's
   own reports, documenting discrepancies and causes.
8. Write the reporting guide: definitions, model differences, known
   gaps, and how to read the dashboard.

## Extension Ideas
- Add cohort retention and expansion revenue.
- Add a data-driven attribution model and compare.
- Add alerting on funnel metric anomalies.
- Add a self-serve semantic layer for the team.

## Skills Demonstrated
- Funnel and revenue data modeling across systems
- Identity resolution and touchpoint timelines
- Attribution modeling and honest comparison
- Executive-grade dashboards reconciled to source

## Industry Relevance

B2B SaaS, E-commerce, Fintech. Revenue operations in these sectors depends on trustworthy funnel and attribution reporting, and the go-to-market engineer is usually the person who makes the systems agree. A reconciled dashboard with a transparent attribution comparison is precisely the deliverable those teams hire for.
