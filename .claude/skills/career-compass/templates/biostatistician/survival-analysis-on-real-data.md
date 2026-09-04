---
title: "Survival Analysis on Real Clinical Data"
track: "biostatistician"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["survival-analysis", "regression-modeling", "r-programming", "data-visualization", "scientific-writing"]
skill_prerequisites: ["statistics", "r-programming"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Survival Analysis on Real Clinical Data

## Production Workflow Mirrored
1. Preparing time-to-event data with correct censoring
2. Estimating and comparing survival curves
3. Modeling with proportional hazards and checking assumptions
4. Handling competing risks and time-varying effects
5. Reporting to clinical and statistical audiences

## What You'll Build
A survival analysis of a public clinical dataset (a cancer registry
extract, a published trial's shared data, or a well-known teaching
dataset with real provenance): data preparation with censoring
definitions, Kaplan-Meier estimates with confidence bands and log-rank
tests, a Cox model with covariate selection rationale, proportional
hazards diagnostics with a remedy where violated, a competing risks or
time-varying covariate analysis, and a report with clinical
interpretation and a statistical appendix.

## Student-Scope Notes
- Use R with the standard survival packages; implement the
  Kaplan-Meier estimator yourself once to understand it.
- Document every decision about the time origin, event definition,
  and censoring.
- The report should be readable by a clinician, with the statistics in
  an appendix.

## Steps
1. Obtain the dataset, define the time origin, event, and censoring
   rules, and build the analysis dataset with a data flow diagram.
2. Estimate Kaplan-Meier curves overall and by a key group with
   confidence intervals, median survival, and a log-rank test.
3. Implement the Kaplan-Meier estimator by hand for one group and
   confirm it matches the package.
4. Fit a Cox model with clinically motivated covariates, report hazard
   ratios with intervals, and interpret.
5. Check proportional hazards with residual diagnostics; if violated,
   apply a stratified or time-varying approach and compare.
6. Address competing risks (cumulative incidence with a competing
   event) or a time-varying covariate, whichever the data support.
7. Produce publication-quality figures with risk tables and a
   forest plot of the model.
8. Write the report for a clinical audience with a statistical
   appendix and the code.

## Extension Ideas
- Fit a parametric survival model and compare predictions.
- Add a landmark analysis for an immortal-time bias scenario.
- Build a prognostic nomogram with internal validation.
- Analyze recurrent events with an appropriate model.

## Skills Demonstrated
- Time-to-event data preparation and censoring logic
- Non-parametric and semi-parametric survival methods
- Assumption checking and remedies
- Clinical-facing statistical reporting

## Industry Relevance

Oncology Research, Pharmaceutical Development, Medical Device Studies, Health Outcomes Research. Time-to-event endpoints dominate trials and observational studies in these sectors, and biostatisticians are expected to handle censoring, assumptions, and competing risks correctly. A complete survival report with diagnostics is a standard, expected portfolio piece.
