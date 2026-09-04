---
title: "Customer Data Integration and Cleanup Pipeline"
track: "forward-deployed-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["data-pipelines", "etl", "sql", "python", "data-quality", "data-modeling"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: ["customer-discovery-and-scoping.md"]
prerequisite_learning_hours: 4
---

# Customer Data Integration and Cleanup Pipeline

## Production Workflow Mirrored
1. Getting access to messy source systems (exports, spreadsheets, legacy
   databases, APIs) under real constraints
2. Profiling the data and documenting every quality problem found
3. Building a repeatable pipeline that lands clean, modeled data
4. Reconciling the output against the customer's own numbers
5. Handing the customer a data dictionary they trust

## What You'll Build
A pipeline that ingests the customer's real data sources from your
discovery engagement (at least two, of different shapes: a spreadsheet
export and a database or API, for example), profiles and documents
their quality issues, cleans and conforms them into a small modeled
schema, reconciles totals against figures the customer already reports,
and produces a data dictionary and a quality report the customer reviews.

## Student-Scope Notes
- Real customer data means real sensitivity: agree on handling rules,
  keep it off shared machines, and anonymize anything in your
  portfolio write-up.
- Python plus SQL (DuckDB, SQLite, or Postgres) is enough. Orchestration
  tooling is not required; a scripted, rerunnable pipeline is.
- Two sources is the floor; the difficulty is in reconciliation and
  documentation, not volume.

## Steps
1. Obtain access to the sources listed in your data inventory and record
   what it actually took (people, approvals, formats) versus the plan.
2. Profile each source: row counts, null rates, duplicates, inconsistent
   codes, date formats, and orphaned references. Write the findings up
   as a quality report with examples.
3. Design the target schema (a few conformed tables with clear keys) and
   the mapping from each source field, including the rules for every
   quality issue found.
4. Build the pipeline as rerunnable scripts: extract, validate, clean,
   load, with each rule tested against a sample of known-bad rows.
5. Add validation checks that fail loudly (row-count drift, key
   uniqueness, referential integrity) and log a run summary.
6. Reconcile: pick three numbers the customer already reports (monthly
   totals, counts by category) and match them from your schema,
   documenting every discrepancy and its cause.
7. Write the data dictionary: every target field, its source, its
   transformation, and known caveats, in language the customer's staff
   understand.
8. Walk the customer through the quality report and reconciliation,
   capture corrections, and rerun. Write up the access story, the issue
   catalogue, and the reconciliation outcome.

## Extension Ideas
- Schedule the pipeline and add a change-detection alert on the sources.
- Add a lightweight lineage diagram from source field to target field.
- Add a slowly-changing-dimension pattern for a reference table.
- Deliver the modeled data into the customer's own BI tool.

## Skills Demonstrated
- Extracting from heterogeneous, imperfect real-world sources
- Data profiling and quality documentation
- Rerunnable cleaning and conforming pipelines with validation
- Reconciliation and customer-facing data dictionaries

## Industry Relevance

Enterprise AI Platforms, Healthcare Analytics, Public Sector Modernization. Forward-deployed work in these sectors is dominated by getting a customer's fragmented data into a shape the product can use, and reconciliation against the customer's own reports is what earns trust. A pipeline built on real messy data, with a documented issue catalogue, is the core FDE portfolio piece.
