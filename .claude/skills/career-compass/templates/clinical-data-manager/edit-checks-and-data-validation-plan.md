---
title: "Edit Checks and Data Validation Plan"
track: "clinical-data-manager"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["clinical-data-validation", "edc-systems", "sql", "technical-documentation"]
skill_prerequisites: ["edc-systems"]
project_prerequisites: ["crf-design-and-edc-database-build.md"]
prerequisite_learning_hours: 2
---

# Edit Checks and Data Validation Plan

## Production Workflow Mirrored
1. Writing a data validation plan from the protocol and CRFs
2. Specifying edit checks with clear logic and query text
3. Programming checks in the EDC and as external listings
4. Testing checks with seeded data
5. Managing queries through their lifecycle

## What You'll Build
A data validation plan for your database: risk-based identification of
critical data, edit check specifications (univariate, cross-form,
cross-visit) with logic and query text, checks implemented in the EDC
and complementary programmed listings in SQL or R, a test data set
seeded with errors and a test log proving each check fires, a query
management process with metrics, and the finalized plan.

## Student-Scope Notes
- Aim for thirty to fifty checks with at least ten cross-form or
  cross-visit checks.
- Programmed listings can run on an export from the EDC.
- Query text must be written for site staff, not programmers.

## Steps
1. Identify critical data from the protocol (primary endpoint, safety,
   eligibility) and build the risk-based validation strategy.
2. Write the edit check specifications with identifiers, forms and
   fields, logic, severity, and query text.
3. Implement the checks that the EDC supports natively, and document
   the ones needing external programming.
4. Program external listings (protocol deviations, missing visits,
   inconsistent dates across forms) in SQL or R on an export.
5. Seed a test dataset with deliberate errors covering every check.
6. Execute the tests, log which checks fired and which did not, and
   fix the specification or implementation.
7. Define the query management process: issuance, site response,
   review, closure, and escalation, with turnaround metrics.
8. Finalize the data validation plan with the check list, listings,
   test evidence, and the query process.

## Extension Ideas
- Add a medical review listing set for clinicians.
- Build a query metrics dashboard from EDC exports.
- Implement a risk-based data review approach with key risk indicators.
- Add checks for external data reconciliation.

## Skills Demonstrated
- Risk-based data validation planning
- Edit check specification and implementation
- Programmed listings and test evidence
- Query lifecycle management

## Industry Relevance

Contract Research Organizations, Pharmaceutical Companies, Biotech, Academic Trial Units. Data validation plans and edit checks are the everyday responsibility of clinical data managers in these sectors, and the quality of query text and testing evidence is what reviewers assess. A tested validation plan with query metrics matches the daily job.
