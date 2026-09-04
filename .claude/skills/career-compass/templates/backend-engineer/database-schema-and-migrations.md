---
title: "Relational Schema Design with Migrations"
track: "backend-engineer"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["relational-databases", "database-design", "orm-and-migrations", "sql"]
skill_prerequisites: ["sql"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# Relational Schema Design with Migrations

## Production Workflow Mirrored
1. Translating product requirements into normalized tables and constraints
2. Evolving the schema through versioned, reversible migrations
3. Indexing for the queries the application actually runs
4. Seeding realistic data and measuring query plans
5. Handling a backwards-compatible schema change while the app keeps running

## What You'll Build
A relational schema for a realistic multi-entity domain (an order system,
a booking system, a content platform) with at least six tables, foreign
keys, unique and check constraints, a migration history that evolves the
schema through at least four versions, and a short performance write-up
showing how indexes changed the query plans for your three most important
queries.

## Student-Scope Notes
- Use Postgres locally (Docker is fine). SQLite works for the first pass
  but its constraint and index behavior differs, so finish on Postgres.
- Seed data is generated with a script (Faker or a hand-written loop) at
  the scale of tens of thousands of rows -- enough for EXPLAIN to show
  index effects, not enough to need a data-generation framework.
- Use whichever migration tool matches your stack (Alembic, Django
  migrations, Prisma Migrate, Flyway, Rails). The concepts are the point.

## Steps
1. Write the requirements as a short list of user stories, then draw the
   entity-relationship diagram before writing any SQL.
2. Create migration 1: the core tables with primary keys, foreign keys,
   NOT NULL, unique, and check constraints. Justify each constraint in a
   comment.
3. Write a seed script that populates the schema with realistic, related
   data at tens of thousands of rows.
4. Write the three most important application queries (a join across three
   tables, an aggregate with GROUP BY, and a filtered list with ORDER BY
   and LIMIT). Capture their EXPLAIN ANALYZE output.
5. Create migration 2: add indexes chosen from those query plans. Re-run
   EXPLAIN ANALYZE and record the before/after timing.
6. Create migration 3: a backwards-compatible change -- add a nullable
   column, backfill it, then add the NOT NULL constraint in a later step,
   the way you would with a running application.
7. Create migration 4: rename or split a column using the expand/migrate/
   contract pattern, and confirm every migration rolls back cleanly.
8. Write up: the ER diagram, the constraint rationale, the index
   before/after table, and what would break if you ran migration 3 as a
   single step against a live app.

## Extension Ideas
- Add a soft-delete pattern and a partial index that excludes deleted rows.
- Add row-level multi-tenancy with a tenant_id on every table and a test
  that proves cross-tenant reads are impossible.
- Add a materialized view for a reporting query and a refresh strategy.

## Skills Demonstrated
- Normalized relational schema design with real constraints
- Versioned, reversible schema migrations and zero-downtime change patterns
- Reading query plans and choosing indexes from evidence
- Seeding and benchmarking against realistic data volumes

## Industry Relevance

E-commerce, Fintech, Healthcare Software. Every transactional product depends on a schema that enforces its invariants in the database, and schema changes against live systems are where outages happen. Backend hiring managers in these sectors look for engineers who can explain constraints, read a query plan, and ship a migration without locking a table.
