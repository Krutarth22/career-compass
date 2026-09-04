---
title: "External Data Reconciliation and Medical Coding"
track: "clinical-data-manager"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["clinical-data-validation", "medical-coding", "sql", "python", "adverse-event-reporting"]
skill_prerequisites: ["sql"]
project_prerequisites: ["crf-design-and-edc-database-build.md"]
prerequisite_learning_hours: 3
---

# External Data Reconciliation and Medical Coding

## Production Workflow Mirrored
1. Receiving external data (central laboratory, safety database) with
   transfer specifications
2. Reconciling it against the clinical database
3. Coding adverse events and medications to dictionaries
4. Managing coding queries and consistency
5. Reporting reconciliation and coding status

## What You'll Build
A reconciliation and coding package for your trial database: a data
transfer specification for a central laboratory feed, a synthetic lab
dataset with deliberate discrepancies, a programmed reconciliation in
SQL or Python producing a discrepancy report, a serious adverse event
reconciliation between the database and a safety listing, medical
coding of adverse events and medications using MedDRA-style and
WHODrug-style hierarchies (with public or demo dictionaries), a
coding consistency review, and status reports.

## Student-Scope Notes
- Real dictionaries require licenses; use demo versions or a small
  public subset and note that.
- Generate the external datasets yourself with realistic
  discrepancies (missing visits, date mismatches, unit differences).
- Report discrepancy rates and resolution status.

## Steps
1. Write the data transfer specification: file format, variables,
   units, frequency, and identifiers.
2. Generate a synthetic laboratory dataset matching the specification
   with seeded discrepancies against the database.
3. Program the reconciliation: matching on identifiers and dates,
   comparing units and results, and producing a discrepancy report by
   type.
4. Reconcile serious adverse events between the database and a
   synthetic safety listing, and document the resolution workflow.
5. Code adverse event verbatim terms to the dictionary hierarchy and
   medications to a drug dictionary, with autocoding and manual review.
6. Run a coding consistency review across similar verbatim terms and
   resolve with coding conventions.
7. Issue coding queries for uncodeable terms with clear text.
8. Produce reconciliation and coding status reports and write the
   process documentation.

## Extension Ideas
- Add an imaging or ECG vendor data reconciliation.
- Build a dictionary version upgrade impact assessment.
- Automate the reconciliation on a schedule with notifications.
- Add a synonym list management process.

## Skills Demonstrated
- Data transfer specifications and programmed reconciliation
- Serious adverse event reconciliation
- Medical coding with dictionaries and consistency review
- Status reporting for data management

## Industry Relevance

Contract Research Organizations, Pharmaceutical Companies, Central Laboratories, Safety Vendors. Reconciliation and coding are required before database lock in every trial across these sectors, and clinical data managers are expected to run both. A package with programmed reconciliation and reviewed coding demonstrates readiness for lock activities.
