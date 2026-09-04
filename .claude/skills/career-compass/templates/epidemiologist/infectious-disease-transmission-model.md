---
title: "Infectious Disease Transmission Model"
track: "epidemiologist"
difficulty_tier: "advanced"
estimated_hours: 14
role: "core"
skill_tags: ["infectious-disease-modeling", "python", "r-programming", "statistics", "public-health-communication"]
skill_prerequisites: ["python", "statistics"]
project_prerequisites: ["outbreak-investigation-simulation.md"]
prerequisite_learning_hours: 4
---

# Infectious Disease Transmission Model

## Production Workflow Mirrored
1. Choosing a model structure appropriate to the disease and question
2. Parameterizing from literature and fitting to data
3. Quantifying uncertainty in parameters and projections
4. Evaluating interventions in the model
5. Communicating projections with their assumptions to decision makers

## What You'll Build
A compartmental transmission model for a disease with public incidence
data (an influenza season, a measles outbreak, a COVID-19 wave in one
region): a model structure justified by the disease's natural history,
parameters from cited literature, a fit to incidence data with
uncertainty estimation, estimation of the reproduction number over
time, scenario analysis of at least two interventions (vaccination,
contact reduction), sensitivity analysis, and a policy brief with
projections and their assumptions clearly stated.

## Student-Scope Notes
- Implement the model equations yourself; use libraries for solving
  and fitting.
- Fit to data with a method that yields uncertainty (likelihood-based
  or Bayesian), not by eye.
- The brief must explain what the model cannot tell decision makers.

## Steps
1. Summarize the disease's natural history and choose compartments,
   transitions, and any age or risk structure.
2. Write the model equations and implement the solver; verify with a
   known analytical case.
3. Collect parameters from literature with ranges and citations.
4. Fit the model to the incidence data, estimating key parameters with
   uncertainty and checking the fit.
5. Estimate the time-varying reproduction number from the data by an
   independent method and compare with the model.
6. Implement intervention scenarios and project outcomes with
   uncertainty bands.
7. Run sensitivity analysis on the most uncertain parameters and
   report which drive the conclusions.
8. Write the policy brief with the scenarios, uncertainty, and
   assumptions, and a technical appendix with the model and code.

## Extension Ideas
- Add age structure with a contact matrix.
- Build a stochastic version and compare extinction probabilities.
- Add a hospital capacity model to the projections.
- Fit to multiple regions with hierarchical parameters.

## Skills Demonstrated
- Compartmental model formulation and implementation
- Parameter estimation with uncertainty
- Reproduction number estimation
- Scenario analysis and policy communication

## Industry Relevance

National Health Agencies, Academic Modeling Groups, International Health Organizations, Pharmaceutical Epidemiology. Modeling capacity became a permanent requirement in these sectors, and epidemiologists who can build, fit, and honestly communicate a transmission model are in demand. A fitted model with intervention scenarios and a policy brief is a distinctive portfolio piece.
