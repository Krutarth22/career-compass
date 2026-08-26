---
title: "Interactive BI Dashboard with Stakeholder Narrative"
track: "data-analyst"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["business-intelligence-tools", "data-visualization", "stakeholder-communication"]
skill_prerequisites: ["sql", "data-visualization"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# Interactive BI Dashboard with Stakeholder Narrative

## Production Workflow Mirrored
1. Gather requirements from a (simulated) stakeholder: what decisions the
   dashboard needs to support
2. Design a data model the BI tool can query efficiently
3. Build the dashboard: top-level KPIs, drill-down views, filters
4. Apply visual design principles so the dashboard is scannable, not just
   accurate
5. Write a short stakeholder-facing narrative that walks through what the
   dashboard shows and what action it suggests
6. Get (simulated) feedback and iterate on the design

## What You'll Build
An interactive BI dashboard (built in Tableau Public, Power BI, or Looker
Studio — pick whichever is free/available to you) on top of a business
dataset (e.g. e-commerce sales, subscription churn, marketing campaign
performance). The dashboard has a top-level KPI summary view and at least
one drill-down path (e.g. region -> store -> product), plus a one-page
written narrative aimed at a non-technical stakeholder explaining what the
numbers mean and what you'd recommend doing about them.

## Student-Scope Notes
- Built against a static or periodically-refreshed extract, not a live
  streaming data connection — the dashboard-design and storytelling skills
  transfer directly even without a production data pipeline behind it.
- One BI tool, one dataset, one primary stakeholder persona — not a suite of
  dashboards serving multiple teams with row-level security and access
  controls.
- "Stakeholder feedback" is self-generated (you write the questions a real
  stakeholder would ask and answer them), not from an actual user-testing
  session — the point is practicing the anticipation-and-response habit.
- Visual design is judged against BI dashboard conventions (data-ink ratio,
  consistent color encoding, avoiding chart junk), not a full design-system
  exercise.

## Steps
1. Write a one-paragraph requirements brief in the voice of a stakeholder
   (e.g. a VP of Sales) stating the 3 decisions they need this dashboard to
   support. Let this brief drive every design choice that follows.
2. Choose or shape a dataset (500+ transactional/event rows minimum) and
   build a simple star-schema-style data model (one fact table, a couple of
   dimension tables) so the BI tool can aggregate cleanly.
3. Design the top-level view on paper/whiteboard first: which 4-6 KPIs
   answer the stakeholder's questions at a glance, and in what layout.
4. Build the top-level KPI view: scorecards/big numbers for headline
   metrics, a trend chart, and a top-N breakdown (e.g. top products/regions).
5. Add at least one drill-down interaction: clicking a region filters the
   rest of the view down to that region's detail, or a parameter control
   lets the user switch the metric being shown.
6. Add filters/date-range controls a stakeholder would actually use (not
   every possible filter — pick the 2-3 that map to real decisions).
7. Apply visual polish: consistent color encoding across charts (the same
   category is always the same color), remove unnecessary gridlines/legends,
   order categorical axes meaningfully instead of alphabetically.
8. Write the stakeholder narrative: what the dashboard shows, the 2-3
   biggest findings, and a concrete recommendation tied to a number on the
   dashboard.
9. Do a self-critique pass: list 3 questions a skeptical stakeholder would
   ask that the current dashboard can't answer, and either add a view for
   them or note it explicitly as a scoping decision.

## Extension Ideas
- Add a second drill-down path (e.g. by time as well as by category) and
  compare which one stakeholders would find more useful.
- Rebuild the same dashboard in a second BI tool and compare tradeoffs.
- Add a "what changed since last period" view highlighting movers, not just
  current-state numbers.
- Record a 3-minute Loom-style walkthrough as if presenting to leadership.

## Skills Demonstrated
- BI tool proficiency (Tableau/Power BI/Looker Studio)
- Dashboard information design and drill-down interaction design
- Data visualization best practices
- Stakeholder communication: translating numbers into a decision narrative

## Industry Relevance

Retail, Marketing, Financial Services. Leadership teams in these industries make recurring decisions — inventory, campaign spend, portfolio performance — off dashboards that need to surface the right KPIs at a glance and support drill-down when a number looks off. Building a dashboard that a VP-level stakeholder can actually use, paired with a written narrative connecting the numbers to a recommendation, is the day-to-day deliverable that separates a working analyst from someone who can just build charts.
