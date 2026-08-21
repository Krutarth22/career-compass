---
title: "Orchestrating a Multi-Step ML Pipeline"
track: "ml-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["workflow-orchestration", "data-pipelines", "ci-cd", "python"]
skill_prerequisites: ["python", "data-pipelines"]
project_prerequisites: []
prerequisite_learning_hours: 6
---

# Orchestrating a Multi-Step ML Pipeline

## Production Workflow Mirrored
1. Breaking an ML workflow into discrete stages (ingest, preprocess, train,
   evaluate, publish)
2. Explicit dependency graph between stages
3. Retries and failure isolation per stage
4. Run logging/observability (what ran, when, with what inputs, pass/fail)
5. Scheduling/triggering a run
6. Re-running from a failed stage instead of from scratch

## What You'll Build
A multi-step ML pipeline (ingest -> preprocess -> train -> evaluate ->
publish) expressed as an explicit DAG with a lightweight orchestration tool
(or a well-structured plain-Python DAG runner), with per-stage retries,
structured run logs, and the ability to resume a failed run from the
stage that broke instead of restarting from scratch.

## Student-Scope Notes
- A lightweight orchestrator (e.g. Prefect, a small local Airflow instance,
  or a hand-rolled DAG runner) run locally, not a managed production
  scheduler cluster.
- Retries are simple (fixed attempts + backoff) rather than a full
  failure-classification policy.
- "Scheduling" means a cron-style trigger or manual CLI invocation, not a
  distributed scheduler with SLAs.

## Steps
1. Pick or reuse an ML workflow with at least 4 distinct stages (ingest,
   preprocess, train, evaluate, publish are a good default).
2. Express each stage as a discrete unit with declared inputs/outputs.
3. Wire the stages into a DAG with explicit dependencies using a lightweight
   orchestration tool or a hand-rolled DAG runner.
4. Add retries with backoff to at least one stage prone to transient
   failure (e.g. a network call or flaky I/O).
5. Add structured run logging: run id, stage, start/end time, status,
   inputs summary.
6. Deliberately fail a stage (inject an error) and implement resuming the
   pipeline from that stage rather than from the start.
7. Add a trigger (cron entry or CLI command) to kick off a run.
8. Write up: what failure modes this catches that a single monolithic
   script wouldn't, and what you'd add for a real production scheduler.

## Extension Ideas
- Add data quality checks as a gating stage before training proceeds.
- Emit pipeline run metadata to a small dashboard (success rate, duration
  trend per stage).
- Parameterize runs (e.g. different training configs) and track which
  config produced which run.
- Wire the pipeline into a CI job that runs it on a schedule or on data
  changes.

## Skills Demonstrated
- Workflow/DAG orchestration for ML pipelines
- Building resilient, resumable multi-stage data pipelines
- Run observability and structured logging
- CI/CD instincts applied to recurring ML workflows

## Industry Relevance

E-commerce Personalization, Financial Risk Modeling, Ad Tech. Models in these sectors are commonly retrained on a recurring schedule as new data arrives, and a monolithic training script that fails midway through a multi-hour run forces an expensive full restart instead of resuming from the broken stage. This project's DAG-based pipeline with per-stage retries, structured run logging, and resume-from-failure is the orchestration discipline that keeps a retraining pipeline cheap to operate and easy to debug when a stage inevitably breaks.
