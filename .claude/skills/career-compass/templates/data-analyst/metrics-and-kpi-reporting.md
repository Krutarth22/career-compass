---
title: "KPI Framework and Recurring Metrics Report"
track: "data-analyst"
difficulty_tier: "beginner"
estimated_hours: 10
role: "core"
skill_tags: ["spreadsheet-analysis", "data-storytelling", "stakeholder-communication"]
skill_prerequisites: ["spreadsheet-analysis"]
project_prerequisites: []
prerequisite_learning_hours: 6
---

# KPI Framework and Recurring Metrics Report

## Production Workflow Mirrored
1. Work with stakeholders to define what actually counts as a KPI vs. a
   vanity metric for the business
2. Define each metric precisely (formula, data source, owner, cadence)
3. Build a repeatable report/template that can be refreshed each period
   without redesigning it from scratch
4. Populate it with real (or realistic simulated) numbers for several
   periods
5. Present the report with a narrative, not just a wall of numbers

## What You'll Build
A KPI framework and a recurring spreadsheet-based report for a hypothetical
business (pick one you can reason about concretely: a subscription box
company, a two-sided marketplace, or a B2B SaaS product). The deliverable is
a metric definition document plus a spreadsheet report covering at least 6
periods (e.g. 6 months) with trend visuals, and a short presentation
narrative you'd deliver to leadership.

## Student-Scope Notes
- The spreadsheet is built manually against simulated or lightly-sourced
  numbers, not connected to a live data warehouse — the reporting design
  and metric-definition discipline transfer directly even without a live
  feed (a refreshable, tool-connected version of this idea is what the BI
  dashboard and capstone projects build).
- One business, one KPI framework (5-8 metrics), not a full metrics
  catalog covering every team — depth on a focused set beats breadth here.
- The "presentation" is a written narrative plus slides/talking points, not
  a recorded delivery — the skill being practiced is structuring the story,
  not presentation delivery.

## Steps
1. Pick a business model and write one paragraph describing how it makes
   money and what "healthy" looks like for it.
2. Draft a first list of 12-15 candidate metrics, then cut it down to 5-8
   real KPIs by applying a clear filter: does this metric change a decision
   someone would actually make, or is it just a number that's easy to
   compute? Write down why each cut metric was cut.
3. For each surviving KPI, write a precise definition: exact formula,
   what data it needs, the reporting cadence (daily/weekly/monthly), and
   who owns acting on it. Ambiguous metrics (e.g. "active user") need an
   explicit operational definition, not just a name.
4. Design the spreadsheet structure: a raw-data-input tab, a calculations
   tab (formulas, not hardcoded numbers), and a report tab that reads from
   the calculations tab. Never hardcode a computed number directly into the
   report tab.
5. Populate 6+ periods of realistic data (simulate it with a clear,
   documented method — e.g. a base value plus trend plus seasonal
   noise — so the numbers move in a believable way period over period).
6. Build the report tab: current-period scorecards, trend charts for each
   KPI, and period-over-period and year-over-year (or best comparable)
   change indicators.
7. Add at least one derived/composite metric that combines two base KPIs
   (e.g. a health score, or LTV:CAC ratio) and explain its logic.
8. Write the presentation narrative: which KPIs moved and why (as best you
   can infer from the data), which one deserves the most leadership
   attention this period, and what you'd recommend watching next period.
9. Stress-test the framework: pick one KPI and describe a scenario where it
   would mislead a reader if looked at in isolation, and how a guardrail
   metric would catch it.

## Extension Ideas
- Add conditional formatting/alerting logic (e.g. auto-flag any KPI that
  moves more than 2 standard deviations period-over-period).
- Build a lightweight forecast for 1-2 KPIs (simple linear trend or moving
  average) and compare forecast vs. actual in a later period.
- Rebuild the report tab as a one-page executive summary versus a detailed
  appendix, and compare which stakeholders would use which.
- Convert the spreadsheet's calculation logic into SQL as if it were now
  backed by a real warehouse table.

## Skills Demonstrated
- Metric definition discipline and vanity-metric filtering
- Advanced spreadsheet modeling (formulas-driven, not hardcoded)
- Recurring/templated business reporting
- Data storytelling and stakeholder-facing presentation structure

## Industry Relevance

Subscription Businesses, Marketplaces, B2B SaaS. These business models live and die by a small set of core metrics — retention, LTV:CAC, marketplace liquidity — and leadership needs a recurring report that separates the KPIs that drive decisions from vanity metrics that just look good. The metric-definition discipline and formulas-driven reporting structure this project builds is precisely what keeps a growing company's leadership team aligned on what "healthy" actually means period over period.
