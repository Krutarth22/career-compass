---
title: "Clinical Data Programming and Study Reporting"
track: "clinical-data-manager"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["sql", "python", "r-programming", "data-visualization", "cdisc-standards", "hipaa-privacy-security"]
skill_prerequisites: ["sql"]
project_prerequisites: ["crf-design-and-edc-database-build.md"]
prerequisite_learning_hours: 3
---

# Clinical Data Programming and Study Reporting

## Production Workflow Mirrored
1. Extracting and transforming clinical data for reports and transfers
2. Producing study status and data quality reports for teams
3. Preparing standards-aligned transfer datasets
4. Protecting participant privacy in every output
5. Automating recurring reports reproducibly

## What You'll Build
A reporting and programming toolkit for your trial: automated
extraction from the EDC, transformation scripts producing enrollment,
visit compliance, adverse event, and data quality reports, a
standards-aligned transfer of raw data toward SDTM structure with a
mapping document, de-identification applied to every output with a
documented method, and a scheduled, reproducible reporting pipeline
with version control.

## Student-Scope Notes
- Use the EDC's API or export files; automate the pull.
- Reports should be readable by study teams, with definitions on every
  metric.
- De-identification must follow a recognized method and be verified.

## Steps
1. Set up automated extraction from the EDC into a working database or
   files with a run log.
2. Write the transformation scripts for enrollment and screening
   metrics by site, with definitions.
3. Add visit compliance, missing data, and query aging reports.
4. Add adverse event summaries by term and severity with the coded
   data.
5. Produce a raw-to-SDTM-structured transfer for three domains with a
   mapping document, in preparation for statistical programming.
6. Implement de-identification (dates shifted or removed, free text
   reviewed, identifiers replaced) and verify no direct identifiers
   remain.
7. Schedule the pipeline, version the code, and add a change log and
   validation of each report against a manual check.
8. Write the toolkit documentation and present the reports to a mock
   study team.

## Extension Ideas
- Build an interactive dashboard for the study team.
- Add a risk-based monitoring key risk indicator report.
- Produce a data transfer package with a transfer log and checksums.
- Add unit tests for the transformation logic.

## Skills Demonstrated
- Automated clinical data extraction and transformation
- Study reporting with defined metrics
- Standards-aligned data transfer preparation
- Privacy-protective output generation

## Industry Relevance

Contract Research Organizations, Pharmaceutical Companies, Academic Research Organizations, Health Data Vendors. Clinical data managers who can program reports and transfers are increasingly required in these sectors as data management becomes more technical. A reproducible reporting toolkit with de-identification is a differentiating portfolio piece.
