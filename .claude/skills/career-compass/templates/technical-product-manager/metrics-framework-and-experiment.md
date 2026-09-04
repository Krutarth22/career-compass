---
title: "Metrics Framework and a Product Experiment"
track: "technical-product-manager"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["product-analytics", "ab-testing", "sql", "statistics", "data-storytelling"]
skill_prerequisites: ["sql", "statistics"]
project_prerequisites: ["user-research-and-problem-definition.md"]
prerequisite_learning_hours: 4
---

# Metrics Framework and a Product Experiment

## Production Workflow Mirrored
1. Defining a north-star metric and the input metrics that drive it
2. Instrumenting events so the metrics can actually be computed
3. Designing an experiment with a hypothesis, power, and guardrails
4. Analyzing results correctly and deciding what to ship
5. Communicating the decision and its confidence

## What You'll Build
A metrics framework for a product you can instrument (a small app you
or a peer built, or an open-source product you can deploy with users):
a metric tree from north star to inputs, event instrumentation and SQL
definitions for each metric, a dashboard, and a designed and executed
experiment (or a rigorous quasi-experiment if randomization is not
possible) with a pre-registered hypothesis, sample-size calculation,
analysis, and a decision memo.

## Student-Scope Notes
- A small real user base is enough if you design for it honestly; if
  the sample is too small for significance, say so and use the
  experiment to practice the method.
- Use a product analytics tool's free tier or your own event tables
  with SQL.
- Pre-register the hypothesis and analysis plan before looking at data.

## Steps
1. Define the north-star metric and build the metric tree of input
   metrics with the causal logic connecting them.
2. Specify the events needed for each metric with properties, and
   instrument them (or generate a realistic stream and label it so).
3. Write SQL definitions for every metric and build the dashboard with
   segment breakdowns.
4. Choose a change to test that plausibly moves an input metric, and
   write the hypothesis, the primary and guardrail metrics, and the
   minimum detectable effect.
5. Calculate the sample size and duration, and pre-register the analysis
   plan.
6. Run the experiment with proper randomization (or design the best
   quasi-experiment available and document its limitations).
7. Analyze: effect size with confidence intervals, guardrail checks,
   segment sanity checks, and known pitfalls (peeking, novelty).
8. Write the decision memo: result, confidence, recommendation, risks,
   and what to test next, and present it.

## Extension Ideas
- Add a sequential testing or Bayesian analysis and compare.
- Build an experiment registry and a results archive.
- Add a metric-anomaly alert on the dashboard.
- Run a second experiment on a different input metric.

## Skills Demonstrated
- Metric tree design and instrumentation specification
- SQL metric definitions and dashboards
- Experiment design with power and guardrails
- Correct analysis and decision communication

## Industry Relevance

Consumer Apps, Marketplaces, SaaS. Product managers in these sectors are expected to define metrics, run experiments, and read results without leaning entirely on analysts, and interviews test exactly that. A metric tree with SQL definitions and a pre-registered experiment memo demonstrates the analytical half of the role.
