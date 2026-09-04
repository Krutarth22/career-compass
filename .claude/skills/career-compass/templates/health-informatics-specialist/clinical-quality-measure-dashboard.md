---
title: "Clinical Quality Measure Dashboard"
track: "health-informatics-specialist"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["healthcare-analytics", "sql", "data-visualization", "business-intelligence-tools", "healthcare-data-standards"]
skill_prerequisites: ["sql"]
project_prerequisites: ["ehr-data-extraction-and-cohort-definition.md"]
prerequisite_learning_hours: 3
---

# Clinical Quality Measure Dashboard

## Production Workflow Mirrored
1. Implementing published quality measures from their specifications
2. Computing numerators, denominators, exclusions, and rates
3. Validating measure logic against specifications and samples
4. Building a dashboard clinicians and quality teams use
5. Explaining variation and supporting improvement

## What You'll Build
An implementation of at least three published clinical quality
measures (for example diabetes control, hypertension control,
preventive screening) on your synthetic EHR data: measure logic in SQL
following the specifications with value sets, computed rates by
provider and site with confidence intervals, validation against a
manual sample and the specification's test cases where available, a
dashboard with drill-down to patient lists for care gaps, and a
measure guide explaining each measure and its caveats.

## Student-Scope Notes
- Use published measure specifications and value sets and cite the
  versions.
- Synthetic data will produce odd rates; document why.
- The dashboard should support a quality team's workflow: rates,
  trends, and actionable patient lists.

## Steps
1. Select three measures and read their specifications: populations,
   exclusions, value sets, and measurement periods.
2. Load the value sets and implement the denominator, exclusions, and
   numerator logic in SQL for each.
3. Compute rates overall, by provider, and by site, with confidence
   intervals and small-cell handling.
4. Validate: manually review a sample of numerator and denominator
   cases, and run any published test cases.
5. Build the dashboard with rate cards, trends over measurement
   periods, provider comparisons with appropriate caution, and
   drill-down to care-gap patient lists.
6. Add a data quality panel showing missingness that affects measures.
7. Write the measure guide with plain-language definitions, caveats,
   and how to act on the lists.
8. Present the dashboard to a peer playing a quality director and
   record their questions and your changes.

## Extension Ideas
- Implement a measure in a computable measure language.
- Add risk adjustment for a comparison across providers.
- Add a care-gap outreach workflow with tracking.
- Automate measure computation on a schedule.

## Skills Demonstrated
- Quality measure specification implementation
- Rate computation with validation
- Dashboard design for clinical quality workflows
- Measure documentation and stakeholder communication

## Industry Relevance

Health Systems, Accountable Care Organizations, Payers, Quality Reporting Vendors. Quality measurement drives reimbursement and improvement in these sectors, and informatics analysts who can implement measures correctly are in constant demand. A validated measure dashboard with a guide is the standard work sample for those roles.
