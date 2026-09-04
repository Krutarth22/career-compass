---
title: "Clinical Trial Design and Sample Size Justification"
track: "biostatistician"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["clinical-trial-design", "statistics", "r-programming", "technical-documentation"]
skill_prerequisites: ["statistics"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Clinical Trial Design and Sample Size Justification

## Production Workflow Mirrored
1. Translating a clinical question into estimands and endpoints
2. Choosing the design: parallel, crossover, non-inferiority, adaptive
3. Justifying sample size with assumptions from prior data
4. Planning randomization, blinding, and interim analyses
5. Writing the statistical sections of a protocol

## What You'll Build
The statistical design for a hypothetical but realistic phase II or
III trial based on a published trial's disease area: primary and
secondary endpoints with estimands, a design choice with rationale,
sample size calculations with assumptions sourced from literature and
sensitivity analyses in R, a randomization scheme, an interim analysis
plan with stopping boundaries where appropriate, and the statistical
sections of a protocol written to regulatory expectations.

## Student-Scope Notes
- Base assumptions on a real published trial and cite it.
- Implement sample size calculations in R (and check with a second
  method) rather than only using a calculator.
- Follow the ICH E9 and E9(R1) guidance for terminology.

## Steps
1. Choose the disease area and clinical question, and read the source
   trial's design and results.
2. Define the estimand: population, treatment, endpoint, intercurrent
   events and strategies, and population-level summary.
3. Choose the design and justify it against alternatives, including
   the comparator and the hypothesis type.
4. Compute the sample size for the primary endpoint with sourced
   assumptions, and run sensitivity analyses across plausible values
   with a table and plot.
5. Design the randomization (stratification factors, block or
   minimization) and simulate it to check balance.
6. Plan interim analyses with a group-sequential boundary if
   appropriate, and compute the operating characteristics by
   simulation.
7. Specify the primary analysis method and handling of missing data
   consistent with the estimand.
8. Write the protocol's statistical sections and a short design report
   with all calculations and code.

## Extension Ideas
- Design an adaptive sample size re-estimation and simulate it.
- Add a Bayesian design alternative and compare.
- Design a non-inferiority margin justification.
- Plan a cluster-randomized version and adjust for the design effect.

## Skills Demonstrated
- Estimand and endpoint definition
- Trial design selection and justification
- Sample size and operating characteristics by calculation and
  simulation
- Protocol statistical writing

## Industry Relevance

Pharmaceutical Companies, Contract Research Organizations, Academic Clinical Trial Units, Regulatory Agencies. Trial design and sample size justification are the biostatistician's first contribution to any study in these sectors, and interviews ask candidates to derive and defend a sample size. A protocol statistical section with sourced assumptions and simulations is the core biostatistics portfolio piece.
