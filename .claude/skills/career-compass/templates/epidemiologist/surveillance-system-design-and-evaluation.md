---
title: "Surveillance System Design and Evaluation"
track: "epidemiologist"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["disease-surveillance", "data-pipelines", "sql", "data-visualization", "public-health-communication"]
skill_prerequisites: ["sql", "python"]
project_prerequisites: ["descriptive-epidemiology-of-a-public-dataset.md"]
prerequisite_learning_hours: 3
---

# Surveillance System Design and Evaluation

## Production Workflow Mirrored
1. Defining surveillance objectives, case definitions, and data sources
2. Building the data flow from reporting to analysis
3. Detecting aberrations automatically
4. Evaluating the system's attributes (timeliness, completeness,
   sensitivity)
5. Producing routine surveillance outputs

## What You'll Build
A surveillance system for a condition using simulated reports (or a
public feed such as syndromic or wastewater data): a surveillance
protocol with objectives, case definitions, and data sources, a
pipeline ingesting reports into a database with validation, an
aberration detection method (a statistical algorithm with a
justified threshold) with alert logging, a weekly automated report,
and a system evaluation against standard attributes with
recommendations.

## Student-Scope Notes
- Simulated reports should include realistic delays, duplicates, and
  incomplete records.
- Implement a standard aberration detection algorithm yourself and
  compare it with a package.
- Evaluate the system using a published evaluation framework and cite
  it.

## Steps
1. Write the surveillance protocol: purpose, case definition,
   reporting sources, data elements, flow, and analysis plan.
2. Build the ingestion pipeline with validation, deduplication, and a
   record of reporting delays.
3. Store the data in a database with a schema supporting person,
   place, and time analysis.
4. Implement an aberration detection algorithm, tune the threshold on
   historical data, and log alerts with their evidence.
5. Inject a simulated outbreak signal and measure detection timeliness
   and false alerts.
6. Build the weekly automated report with counts, trends, alerts, and
   data quality metrics.
7. Evaluate the system: simplicity, flexibility, data quality,
   acceptability, sensitivity, positive predictive value,
   representativeness, timeliness, and stability, with evidence.
8. Write the evaluation report with recommendations and the protocol
   as an appendix.

## Extension Ideas
- Add a second data source and compare signals.
- Build a public-facing dashboard with suppression rules.
- Add spatial cluster detection.
- Implement electronic case reporting from a FHIR source.

## Skills Demonstrated
- Surveillance protocol development
- Reporting data pipelines with quality handling
- Aberration detection and alert evaluation
- Systematic surveillance evaluation

## Industry Relevance

Public Health Departments, National and International Health Agencies, Hospital Epidemiology, Health Security Organizations. Surveillance system design and evaluation is a core epidemiologist function in these settings, and modern roles expect data pipeline and detection skills. A working system with an evaluation report matches those expectations directly.
