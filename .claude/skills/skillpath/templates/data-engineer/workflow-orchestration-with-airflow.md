---
title: "Workflow Orchestration with Airflow"
track: "data-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["workflow-orchestration", "python", "batch-processing"]
skill_prerequisites: ["python"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# Workflow Orchestration with Airflow

## Production Workflow Mirrored
1. Break a multi-step pipeline into discrete, dependency-ordered tasks
2. Define the pipeline as a DAG (directed acyclic graph) of tasks
3. Schedule the DAG to run on a recurring cadence
4. Handle task failure with retries and backoff
5. Alert/notify on failure after retries are exhausted
6. Track run history and task-level logs for debugging
7. Support manual backfill of historical runs

## What You'll Build
A multi-step data pipeline (extract -> transform -> load -> validate,
reusing or adapting an earlier project's logic) rewritten as an Airflow DAG
with explicit task dependencies, per-task retries with backoff, a failure
notification (even just a logged/emailed alert), and a working backfill for
a past date range — run locally via the Airflow scheduler and webserver so
you can watch it execute in the UI.

## Student-Scope Notes
- Runs on a local Airflow instance (Docker Compose is the standard
  quickstart), not a managed orchestration service (MWAA, Cloud Composer,
  Astronomer) — DAG authoring, scheduling, and retry semantics are the same
  concepts either way.
- The pipeline logic itself (the actual extract/transform/load code) can be
  reused from a prior project or kept intentionally simple — the point of
  this template is orchestration, not building new transform logic from
  scratch.
- One recurring schedule and one manual backfill run are enough to
  demonstrate the concept; you don't need to build out a large DAG library.
- Notification can be a logged message or a local email via a test SMTP
  server — wiring to a real Slack/PagerDuty integration is an extension.

## Steps
1. Pick (or reuse) a 3-5 step pipeline: e.g. extract raw data, transform it,
   load into a database, run a validation check.
2. Set up Airflow locally (Docker Compose quickstart is fine); confirm the
   webserver and scheduler come up and you can see the default example DAGs.
3. Write your DAG: one task per pipeline step, using `PythonOperator` (or
   the TaskFlow API) with explicit `>>` dependencies between them.
4. Add retries with exponential backoff to at least one task that's
   plausibly flaky (e.g. the extract step hitting a network source).
5. Add a failure callback (`on_failure_callback`) that logs a clear alert
   message (or sends a real email/Slack message if you want the extension).
6. Set a schedule interval (e.g. daily) and confirm the DAG appears
   correctly in the Airflow UI's graph view with dependencies rendered.
7. Trigger a backfill for a small range of past logical dates (`airflow
   dags backfill` or the UI) and confirm each run is tracked separately
   with its own task logs.
8. Deliberately break one task (e.g. point it at a bad file path) and watch
   the retry/failure/alert path fire end-to-end; then fix it and re-run.
9. Write up: your DAG's dependency graph, how retries/backfill behaved, and
   what you'd change moving from local Airflow to a managed service.

## Extension Ideas
- Add a sensor task that waits for an upstream file/table to be ready
  before proceeding.
- Parameterize the DAG with Airflow Variables/Connections instead of
  hardcoded values.
- Add SLA misses and see how Airflow surfaces them.
- Swap in a different orchestrator (Dagster or Prefect) for one DAG and
  compare the developer experience.

## Skills Demonstrated
- DAG-based workflow orchestration design
- Dependency management, scheduling, retries, and backfill for data
  pipelines
- Operational instincts around failure handling and alerting
- Reading and debugging orchestration run history/logs
