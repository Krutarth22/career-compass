---
title: "Analytics Engineering with dbt"
track: "data-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["dbt", "sql", "data-modeling", "ci-cd"]
skill_prerequisites: ["sql"]
project_prerequisites: []
prerequisite_learning_hours: 6
---

# Analytics Engineering with dbt

## Production Workflow Mirrored
1. Raw data lands in the warehouse (already extracted/loaded by an
   upstream pipeline)
2. Staging models clean and standardize raw sources
3. Intermediate models join and reshape staged data
4. Mart models produce final, business-facing tables
5. Automated tests enforce data-quality assumptions on every model
6. Documentation is generated from the models themselves
7. Changes run through CI before being merged/deployed

## What You'll Build
A dbt project that transforms raw tables (loaded via an earlier ETL
project or a public sample dataset like the classic Jaffle Shop) through a
staging -> intermediate -> mart layered structure, with dbt tests
(not-null, unique, relationships, and at least one custom test) on key
models, auto-generated documentation with a lineage graph, and a CI check
(GitHub Actions) that runs `dbt build` on every pull request.

## Student-Scope Notes
- Runs against a local Postgres or DuckDB target, not a paid cloud
  warehouse account — dbt's model/test/doc mechanics are identical.
- CI runs against a small, checked-in sample dataset or a seed, not a full
  production-scale warehouse — the point is proving the CI gate works, not
  CI performance at scale.
- "Raw data" can come from dbt seeds or a prior ETL project's output; this
  template is about the transformation layer, not re-doing extraction.
- One custom (singular or generic) test is required; you don't need to
  build a large custom test library.

## Steps
1. Initialize a dbt project pointing at a local Postgres or DuckDB
   database; load raw source tables via dbt seeds or from a prior
   project's output.
2. Declare your raw tables as dbt sources in a `sources.yml`, with basic
   freshness/description metadata.
3. Build staging models (one per source table): rename columns, cast
   types, light cleaning — no joins yet, `select` and `where` only.
4. Build intermediate models that join staging models together into
   reusable, business-logic-bearing shapes.
5. Build mart models: final, wide, business-facing tables analysts would
   actually query (e.g. `fct_orders`, `dim_customers`).
6. Add dbt tests: `not_null` and `unique` on primary keys, `relationships`
   for foreign keys, plus one custom test (e.g. "order total should never
   be negative").
7. Run `dbt docs generate` and browse the generated lineage graph; confirm
   it reflects your staging -> intermediate -> mart structure correctly.
8. Set up a GitHub Actions workflow that runs `dbt build` (models + tests)
   on every pull request against a throwaway/CI database.
9. Deliberately introduce a data issue (e.g. a duplicate key) and confirm
   the relevant test fails locally and in CI; then fix it.
10. Write up: your layering decisions, which tests caught real issues, and
    how the CI gate changes confidence when merging model changes.

## Extension Ideas
- Add incremental models for a large fact table instead of full-refresh.
- Add dbt's `exposures` to document downstream BI dashboards depending on
  your marts.
- Add a `dbt-utils` or custom macro to reduce repeated SQL logic.
- Wire a Slack/GitHub notification into the CI workflow on test failure.

## Skills Demonstrated
- Analytics engineering with dbt (staging/intermediate/mart layering)
- SQL-based data modeling and reusable transformation logic
- Automated data-quality testing embedded in the transformation layer
- CI/CD applied to a data transformation pipeline
