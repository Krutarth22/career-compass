---
title: "Outbreak Investigation Simulation"
track: "epidemiologist"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["disease-surveillance", "epidemiological-methods", "r-programming", "statistics", "public-health-communication"]
skill_prerequisites: ["statistics", "r-programming"]
project_prerequisites: ["descriptive-epidemiology-of-a-public-dataset.md"]
prerequisite_learning_hours: 2
---

# Outbreak Investigation Simulation

## Production Workflow Mirrored
1. Confirming an outbreak and establishing a case definition
2. Finding cases and building a line list
3. Describing the outbreak with an epidemic curve and attack rates
4. Testing hypotheses with a cohort or case-control analysis
5. Recommending control measures and reporting

## What You'll Build
A complete investigation of a simulated outbreak using a published
teaching exercise or a synthetic scenario you construct with a known
source: a case definition with sensitivity and specificity tiers, a
line list built from case reports, an epidemic curve with
interpretation of the likely exposure type, attack rates by exposure,
an analytic study (retrospective cohort or case-control) with measures
of association and confidence intervals, a stratified analysis for
confounding, control recommendations, and an outbreak report in the
standard format.

## Student-Scope Notes
- Published teaching exercises from public health agencies are freely
  available; a self-constructed scenario must have a known truth.
- Perform the analysis in R with reproducible code.
- The report should follow the standard structure used by public
  health agencies.

## Steps
1. Review the initial reports, confirm the outbreak against expected
   background, and write the case definition with confirmed, probable,
   and suspected tiers.
2. Build the line list from the case data with demographics, onset,
   exposures, and outcomes.
3. Construct the epidemic curve and interpret the likely mode of
   transmission and exposure period, estimating the incubation period.
4. Compute attack rates by exposure and identify candidate sources.
5. Design and run the analytic study (cohort if the population is
   enumerable, case-control otherwise) with risk or odds ratios and
   confidence intervals.
6. Stratify by potential confounders and assess effect modification.
7. Draft control measures and communication for the affected
   population and providers.
8. Write the outbreak report: background, methods, results with tables
   and figures, discussion, recommendations, and limitations.

## Extension Ideas
- Add laboratory and environmental sampling logic to the investigation.
- Estimate the reproduction number from the epidemic curve.
- Design a contact tracing protocol for the scenario.
- Present the findings in a mock press briefing.

## Skills Demonstrated
- Case definition and line list construction
- Epidemic curve interpretation
- Analytic epidemiology for source identification
- Outbreak reporting and control recommendations

## Industry Relevance

Public Health Departments, National Health Agencies, Hospital Infection Prevention, International Health Organizations. Outbreak investigation is the defining competency of field epidemiologists in these settings, and hiring for those roles tests the standard steps directly. A completed investigation with an analytic study and a formal report demonstrates that competency.
