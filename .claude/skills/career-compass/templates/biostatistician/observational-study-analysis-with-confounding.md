---
title: "Observational Study Analysis with Confounding Control"
track: "biostatistician"
difficulty_tier: "advanced"
estimated_hours: 14
role: "core"
skill_tags: ["regression-modeling", "causal-inference", "epidemiological-methods", "r-programming", "statistics"]
skill_prerequisites: ["statistics", "r-programming"]
project_prerequisites: ["survival-analysis-on-real-data.md"]
prerequisite_learning_hours: 4
---

# Observational Study Analysis with Confounding Control

## Production Workflow Mirrored
1. Specifying a causal question and drawing the assumptions
2. Choosing a confounding-control strategy
3. Estimating the effect with propensity or outcome models
4. Assessing balance, overlap, and sensitivity to unmeasured confounding
5. Reporting transparently with limitations

## What You'll Build
An analysis estimating a treatment effect from public observational
health data (a survey with treatment information, a registry, or a
synthetic dataset with known truth for validation): a causal diagram
with justified assumptions, a pre-specified analysis plan, propensity
score estimation with balance diagnostics, effect estimation by at
least two methods (matching or weighting, and an outcome regression or
doubly robust estimator), sensitivity analysis for unmeasured
confounding, and a report following reporting guidelines for
observational studies.

## Student-Scope Notes
- A dataset with a known truth (simulated from a real structure) is
  valuable for checking your methods; pair it with a real dataset for
  the report.
- Follow STROBE for the write-up.
- State the target trial you are emulating.

## Steps
1. Define the causal question as a target trial: eligibility,
   treatment strategies, follow-up, outcome, and estimand.
2. Draw the causal diagram, identify the adjustment set, and write the
   pre-specified analysis plan.
3. Prepare the data with eligibility criteria and time-zero alignment,
   documenting exclusions.
4. Estimate propensity scores, assess overlap, and achieve balance with
   matching or weighting; report standardized differences.
5. Estimate the effect with the propensity method and with an outcome
   model or doubly robust estimator; compare.
6. Run sensitivity analyses: an E-value or a bias analysis for
   unmeasured confounding, and alternative model specifications.
7. If using a simulated dataset with known truth, report the methods'
   bias and coverage.
8. Write the STROBE-compliant report with the diagram, methods,
   results, sensitivity, and an honest limitations section.

## Extension Ideas
- Add an instrumental variable analysis if a plausible instrument
  exists.
- Apply a marginal structural model for a time-varying treatment.
- Use machine learning for nuisance models within a doubly robust
  framework.
- Replicate a published observational finding and compare.

## Skills Demonstrated
- Causal question specification with target trial emulation
- Propensity score methods and balance diagnostics
- Multiple estimation approaches and sensitivity analysis
- Transparent observational study reporting

## Industry Relevance

Health Outcomes Research, Pharmacoepidemiology, Payers and Health Systems, Regulatory Real-World Evidence. Real-world evidence is a growing part of decision-making in these sectors, and biostatisticians who can handle confounding rigorously and report honestly are in demand. A target-trial analysis with balance diagnostics and sensitivity analyses demonstrates that rigor.
