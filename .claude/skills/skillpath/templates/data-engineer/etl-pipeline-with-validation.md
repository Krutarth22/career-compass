---
title: "ETL Pipeline with Data Validation"
track: "data-engineer"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["etl", "python", "data-quality", "data-pipelines", "sql"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# ETL Pipeline with Data Validation

## Production Workflow Mirrored
1. Extract raw data from a source system (files, API, or database dump)
2. Land raw data unchanged (bronze/raw zone) before touching it
3. Transform: clean, type-cast, deduplicate, reshape into target structure
4. Validate: enforce data-quality rules before data is considered usable
5. Load into a queryable destination (warehouse table or file store)
6. Quarantine/report records that fail validation instead of silently dropping them
7. Run summary: rows in, rows out, rows quarantined, rule failures

## What You'll Build
A batch ETL pipeline that pulls raw data from a public dataset (e.g. a CSV
dump of e-commerce orders, or a public API), lands it untouched, transforms
it into a clean tabular structure, runs an explicit data-quality validation
layer against it, and loads only the records that pass into a local
database — while writing every failing record to a separate quarantine
table with a reason code, and printing a run summary.

## Student-Scope Notes
- Source is a static file or a simple public API, not a live production
  system with authentication, pagination edge cases, or rate-limit backoff
  logic — the extract/transform/validate/load shape is the point, not
  connector robustness.
- Destination is a local Postgres or SQLite database, not a managed cloud
  warehouse — the load pattern (idempotent upsert, staging-then-swap)
  transfers directly.
- Validation rules are hand-written Python/SQL checks (not-null, type,
  range, referential, uniqueness), not a full data-quality framework like
  Great Expectations — you're expected to understand what those frameworks
  automate by building a handful of the checks yourself first.
- Runs on-demand from the command line, not scheduled — scheduling and
  retries are covered in the orchestration template.

## Steps
1. Pick a raw dataset with realistic messiness (missing values, inconsistent
   types, duplicate rows, a few malformed records) — either download a
   public CSV or pull from a free public API.
2. Write the extract step: pull the raw data and write it to a "raw" landing
   location (a local file or raw table) exactly as received, with an
   ingestion timestamp column. Never mutate this copy.
3. Write the transform step: parse types, standardize formats (dates,
   currency, casing), deduplicate on a natural key, and reshape into your
   target table structure.
4. Design your target schema: pick primary keys, foreign keys, and column
   types deliberately — write this down before writing load code.
5. Build a validation layer as a list of explicit rules (not-null checks,
   type checks, allowed-range checks, uniqueness on the key, referential
   checks against a lookup table). Each rule returns pass/fail per row plus
   a reason.
6. Split records into "clean" (all rules pass) and "quarantined" (any rule
   fails). Load clean records into your destination table; write quarantined
   records plus their failure reasons to a separate quarantine table.
7. Make the load idempotent: re-running the pipeline on the same source
   data should not create duplicate rows (use upsert or a staging-table
   swap pattern).
8. Print a run summary at the end: rows extracted, rows loaded, rows
   quarantined, and a breakdown of which validation rules fired most.
9. Write up: what messiness you found in the raw data, which validation
   rules mattered most, and how you'd extend this to a source that changes
   schema over time.

## Extension Ideas
- Add schema-drift detection: alert if the source adds/removes/renames a
  column between runs.
- Add a second source and a merge/dedup step across sources sharing an
  entity (e.g. customers appearing in two feeds).
- Emit validation results as a small HTML or Markdown data-quality report
  instead of just console output.
- Parameterize the pipeline to run incrementally (only new/changed records)
  instead of a full reload each time.

## Skills Demonstrated
- Building an ETL pipeline with a clear extract/transform/validate/load
  separation
- Designing and implementing explicit data-quality validation rules
- Idempotent loading patterns (upsert, staging-then-swap)
- SQL schema design for a transform target
- Communicating data-quality findings from a real, messy dataset
