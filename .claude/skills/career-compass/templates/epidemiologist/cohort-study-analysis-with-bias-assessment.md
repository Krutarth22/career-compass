---
title: "Cohort Study Analysis with Bias Assessment"
track: "epidemiologist"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["epidemiological-methods", "regression-modeling", "causal-inference", "r-programming", "scientific-writing"]
skill_prerequisites: ["statistics", "r-programming"]
project_prerequisites: ["descriptive-epidemiology-of-a-public-dataset.md"]
prerequisite_learning_hours: 3
---

# Cohort Study Analysis with Bias Assessment

## Production Workflow Mirrored
1. Framing an exposure-outcome question with a causal diagram
2. Analyzing a cohort with appropriate regression models
3. Assessing confounding, selection bias, and misclassification
4. Running quantitative bias analysis
5. Reporting to STROBE standards

## What You'll Build
An analysis of an exposure-outcome relationship in a public cohort or
longitudinal survey dataset: a causal diagram and adjustment set, an
analysis plan, descriptive comparison of exposed and unexposed,
regression models (logistic, Poisson, or Cox as appropriate) with
adjusted effect estimates, an assessment of each major bias with
evidence from the data, a quantitative bias analysis for one bias,
and a STROBE-compliant manuscript-style report.

## Student-Scope Notes
- Public cohort data with documentation are available from health
  surveys and research repositories; choose one with follow-up.
- Write the analysis plan before modeling.
- Quantitative bias analysis for misclassification or unmeasured
  confounding must use sourced bias parameters.

## Steps
1. Define the question and draw the causal diagram; identify the
   minimal sufficient adjustment set and potential selection issues.
2. Write the analysis plan: population, exposure and outcome
   definitions, covariates, models, and sensitivity analyses.
3. Build the analysis dataset and describe the cohort by exposure
   status with a table.
4. Fit the crude and adjusted models, check assumptions, and report
   effect estimates with intervals.
5. Assess confounding (change in estimate, diagram-based), selection
   bias (participation and loss to follow-up patterns), and
   misclassification (validation data or literature).
6. Perform a quantitative bias analysis for the most important bias
   and present corrected estimates across parameter ranges.
7. Run planned sensitivity analyses and summarize robustness.
8. Write the STROBE-compliant report with the diagram, methods,
   results, bias assessment, and discussion.

## Extension Ideas
- Apply inverse probability weighting for loss to follow-up.
- Add a mediation analysis with clear assumptions.
- Replicate a published cohort finding and compare.
- Conduct a probabilistic bias analysis with Monte Carlo methods.

## Skills Demonstrated
- Causal framing and adjustment set identification
- Regression analysis of cohort data
- Systematic bias assessment
- Quantitative bias analysis and transparent reporting

## Industry Relevance

Academic Epidemiology, Government Research Agencies, Pharmacoepidemiology, Health Outcomes Research. Analytic epidemiologists in these sectors are distinguished by rigorous bias assessment, not just modeling, and reviewers expect STROBE compliance. A cohort analysis with quantitative bias analysis shows that rigor.
