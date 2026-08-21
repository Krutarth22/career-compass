---
title: "Production Data Platform Capstone"
track: "data-engineer"
difficulty_tier: "advanced"
estimated_hours: 25
role: "capstone"
skill_tags: ["data-quality", "workflow-orchestration", "data-warehousing", "etl", "ci-cd", "data-modeling"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: ["etl-pipeline-with-validation.md", "data-warehouse-modeling.md"]
prerequisite_learning_hours: 5
---

# Production Data Platform Capstone

## Production Workflow Mirrored
1. Combining a validated ETL ingestion layer with a modeled data warehouse
   into a single, coherent platform (not two side-by-side projects)
2. End-to-end data path: raw source -> extract/transform/validate ->
   quarantine or load -> dimensional warehouse -> analytics-ready tables
3. Orchestration as a required, integrated stage: the whole path runs on a
   schedule with dependency ordering and retries, not by hand
4. Data-quality gating as a first-class control: bad data is caught and
   quarantined before it ever reaches the warehouse, and a failed
   validation stage blocks downstream loads
5. Operational readiness: run history, failure alerting, and a documented
   recovery/backfill path
6. Portfolio-level write-up connecting ingestion, modeling, orchestration,
   and data quality into one coherent platform story

## What You'll Build
An integrated data platform that takes the ETL-with-validation pipeline you
built in `etl-pipeline-with-validation.md` and feeds its clean, validated
output into the dimensional warehouse you designed in
`data-warehouse-modeling.md` — one platform, not two disconnected projects
— orchestrated end-to-end as a scheduled, dependency-ordered, retry-capable
pipeline, with validation failures blocking the warehouse load stage and a
portfolio write-up walking through the whole system the way you'd present
it in a system design interview.

## Student-Scope Notes
- This capstone assumes you completed both prerequisite projects; it does
  not re-teach ETL validation rules or star-schema design — it's about
  wiring them into one dependency-ordered platform and closing the
  operational gap between "data got extracted" and "data is safely queryable
  in the warehouse."
- Orchestration can be a lightweight local scheduler (a simple Python
  script with retry logic, or a minimal Airflow DAG if you want the
  practice) rather than a fully productionized orchestration deployment —
  the point is that scheduling, dependency ordering, and retries are a
  required stage of the platform, not that you stand up enterprise-grade
  infrastructure.
- Data volume and infrastructure stay at the same local-database scale as
  the two prerequisite projects; this capstone is about integration and
  operational rigor, not scaling up.
- The quality gate can be a single hard rule ("if quarantine rate exceeds
  X%, halt the warehouse load and alert") rather than a full
  quality-scoring system — the point is that the gate exists and actually
  blocks bad loads, not that it's exhaustive.

## Steps
1. Take your ETL pipeline's extract/transform/validate logic and make its
   clean-record output the explicit input contract for the warehouse load
   stage (same schema your warehouse's staging/dimension load code
   expects).
2. Wire the two pipelines into one dependency-ordered flow: extract ->
   transform -> validate/quarantine -> (gate) -> load dimensions -> load
   facts -> post-load checks. Each stage depends on the previous one
   succeeding.
3. Implement the quality gate: if the validation stage's quarantine rate
   exceeds a threshold you define, halt the run before touching the
   warehouse and emit a clear alert — don't let bad data reach the star
   schema.
4. Add retries with backoff to the extract stage (the most plausibly flaky
   one) and confirm a transient failure there doesn't leave the warehouse
   in a half-updated state.
5. Add post-load checks in the warehouse stage: row-count reconciliation
   between validated records and warehouse rows loaded, and at least one
   referential-integrity check across fact/dimension keys.
6. Make the whole run idempotent and re-runnable: running the full
   platform twice on the same source data should not duplicate warehouse
   rows or corrupt the Type 2 SCD history from the warehouse project.
7. Schedule the platform to run end-to-end (cron, a simple scheduler loop,
   or a minimal orchestrator) and confirm you have run history you can
   inspect — start/end time, stage-level status, quarantine counts.
8. Deliberately trigger a failure at each stage boundary (bad source data
   tripping the quality gate, a broken load) and confirm the platform
   fails safely, alerts, and leaves the warehouse in a consistent state
   rather than partially updated.
9. Write a portfolio-level write-up connecting the pieces: an architecture
   diagram of the full path, what the quality gate protects against, how a
   partial failure is handled and recovered from, and what you'd change for
   a real production version (managed warehouse, real orchestrator, larger
   data volume).

## Extension Ideas
- Swap the lightweight scheduler for the full DAG-based orchestration
  project (`workflow-orchestration-with-airflow.md`) — wire the entire
  extract -> validate -> load flow in as an actual Airflow DAG with proper
  sensors and backfill support, for readers who want to push the platform
  further than the required integration.
- Add the analytics-engineering project (`analytics-engineering-with-dbt.md`)
  as a transformation layer on top of the warehouse marts, with dbt tests
  providing a second, independent data-quality gate downstream of the
  ingestion-side one.
- Add a dead-letter review workflow where quarantined records can be
  manually corrected and re-submitted into the pipeline.
- Add cost/runtime tracking per stage so you can see where the platform
  spends its time as data volume grows.

## Skills Demonstrated
- End-to-end integration of a validated ETL ingestion layer with a
  dimensional data warehouse into one operational platform
- Data-quality gating as a required control in a production data path
- Orchestration fundamentals: dependency ordering, retries, idempotent
  reruns, and run-history visibility
- Failure handling and recovery design for multi-stage data pipelines
- Portfolio-level technical communication connecting ingestion, modeling,
  orchestration, and data quality into one system narrative

## Industry Relevance

Retail, Healthcare, Financial Services. Data platform teams at companies in these sectors are responsible for the full path from raw source data to a trustworthy warehouse that the rest of the business queries, and a validation failure that silently reaches the warehouse can mislead every downstream report or dashboard built on it. This capstone's quality gate that blocks a warehouse load when bad data is detected, combined with scheduled, idempotent, resumable runs, mirrors the operational bar a real data platform team is held to once other teams depend on its output.
