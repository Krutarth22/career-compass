---
title: "Data Warehouse Modeling with a Star Schema"
track: "data-engineer"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["data-warehousing", "data-modeling", "sql", "database-design"]
skill_prerequisites: ["sql"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# Data Warehouse Modeling with a Star Schema

## Production Workflow Mirrored
1. Gather business questions the warehouse needs to answer
2. Identify grain, facts, and dimensions from raw source data
3. Design dimension tables (with slowly changing dimension handling)
4. Design fact tables at a deliberate grain
5. Build the ETL/load logic that populates the model from raw source data
6. Write analytical queries against the model to validate it answers the
   original business questions
7. Document the model (schema diagram, grain definitions, known limitations)

## What You'll Build
A dimensional data warehouse (star schema) built on top of a raw
transactional dataset of your choice (e.g. retail orders, ride-hailing
trips, or subscription billing events), with properly designed fact and
dimension tables, a load process that populates them from raw source data,
and a slowly changing dimension implemented for at least one dimension —
plus a handful of analytical queries proving the model actually answers
realistic business questions faster and more simply than querying the raw
source directly.

## Student-Scope Notes
- Runs on a local Postgres or DuckDB database, not a managed cloud
  warehouse (Snowflake/BigQuery/Redshift) — star-schema design and SCD
  logic are identical; only the compute/storage backend differs.
- Data volume is small enough to fully reload each run — partitioning and
  incremental-load performance at scale are out of scope here (see the
  distributed-processing and orchestration templates for that).
- One slowly changing dimension is required (Type 2, tracked with
  effective-date columns); you don't need to implement every SCD type.
- The load logic here can be a straightforward script; wiring it into a
  scheduled, dependency-aware pipeline is the orchestration template's job.

## Steps
1. Pick a raw transactional dataset (or reuse output from an ETL project)
   with at least one entity that changes over time (e.g. a customer's
   address, a product's price or category).
2. Write down 5-8 concrete business questions the warehouse should answer
   (e.g. "revenue by region by month", "which customer segment churns
   fastest").
3. Identify the fact grain (one row = one what?) and the dimensions that
   describe it (customer, product, date, location, etc.).
4. Design your dimension tables: surrogate keys, natural keys, descriptive
   attributes. Pick one dimension to implement as Type 2 SCD (add
   `effective_start`, `effective_end`, `is_current` columns).
5. Design your fact table(s): foreign keys to each dimension, the grain
   explicitly documented, additive/semi-additive/non-additive measures
   identified.
6. Build a date dimension (calendar table) — this is standard practice and
   worth doing properly (day, week, month, quarter, fiscal periods, is_weekend, etc.).
7. Write the load scripts: populate dimensions first (with SCD logic for
   your Type 2 dimension), then load facts referencing dimension surrogate
   keys.
8. Write the analytical queries answering your original business questions
   directly against the star schema; compare query complexity/readability
   to writing the same query against raw normalized source tables.
9. Document the model: an entity-relationship diagram, grain definitions
   for each fact table, and known limitations (e.g. late-arriving facts not
   handled).

## Extension Ideas
- Add a second fact table at a different grain (e.g. order-line-level and
  order-level) and reconcile them.
- Implement a snapshot fact table for point-in-time balance/inventory
  tracking.
- Add a bridge table for a many-to-many relationship (e.g. products with
  multiple categories).
- Benchmark query performance with and without indexes on foreign keys.

## Skills Demonstrated
- Dimensional data modeling (star schema, fact/dimension design)
- Slowly changing dimension implementation
- SQL schema design and database design tradeoffs
- Translating business questions into a queryable data model
- Data warehousing fundamentals independent of any specific vendor
