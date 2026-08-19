---
title: "SQL Analytics Deep Dive: Answering Business Questions with Advanced SQL"
track: "data-analyst"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["sql", "database-design", "data-storytelling"]
skill_prerequisites: ["sql"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# SQL Analytics Deep Dive: Answering Business Questions with Advanced SQL

## Production Workflow Mirrored
1. Receive a set of ambiguous business questions from a stakeholder
2. Explore an unfamiliar relational schema to find the relevant tables
3. Translate each question into one or more precise SQL queries
4. Progress from simple aggregations to window functions and multi-table
   joins as questions get harder
5. Validate query results against sanity checks (row counts, spot checks)
6. Package results and query logic into a shareable analysis document

## What You'll Build
A written analysis answering 10-12 realistic business questions against a
multi-table relational database (a good fit: a retail orders database, a
subscription SaaS database, or a ride-hailing trips database with tables for
users, orders/trips, products, and payments). Each question is answered with
a documented SQL query, the result, and a short interpretation — building
from basic joins and aggregations up through CTEs and window functions.

## Student-Scope Notes
- Use a database with 5-8 tables and realistic (if synthetic) row counts in
  the tens of thousands — enough to require real joins and indexing
  awareness, not so much that query runtime becomes an engineering problem.
- Query performance tuning (execution plans, indexing strategy) is touched
  on lightly, not treated as a full topic — the focus is query correctness
  and expressiveness, not database administration.
- No live production database connection is required; a local Postgres or
  SQLite instance loaded from a public dataset or a generated schema is a
  faithful proxy for the SQL skills involved.
- This project is about answering point-in-time questions with queries, not
  building a refreshable, presentable dashboard — that's the BI dashboard
  template, and the two are combined in the capstone.

## Steps
1. Set up a local relational database (Postgres recommended) and load a
   multi-table dataset with clear foreign-key relationships (orders, order
   items, customers, products, payments is a solid shape).
2. Write an ER diagram (by hand or with a tool) documenting the schema as
   you understand it before writing any analysis query.
3. Answer 3-4 "level 1" questions using basic aggregation: `GROUP BY`,
   `COUNT`/`SUM`/`AVG`, simple `WHERE` filters (e.g. "what were total sales
   by month last year?").
4. Answer 3-4 "level 2" questions requiring multi-table joins and subqueries
   (e.g. "which customers have never returned a product?", "what's the
   average order value by acquisition channel?").
5. Answer 3-4 "level 3" questions requiring window functions and CTEs (e.g.
   "what's each customer's running total spend and their rank within their
   signup cohort?", "what's the month-over-month growth rate in active
   customers?", "find each product's sales rank within its category using
   `RANK()` or `DENSE_RANK()`").
6. For each query: write it cleanly with CTEs instead of nested subqueries
   where it improves readability, comment non-obvious logic, and validate
   the result with an independent sanity check (e.g. does a manual `COUNT`
   match the row count you expect?).
7. For 2 of the harder queries, capture the query execution plan
   (`EXPLAIN ANALYZE`) and note anything you'd index differently at scale.
8. Write the final analysis document: each question, the query, the result
   (as a table or small chart), and a 2-3 sentence interpretation a
   non-technical stakeholder could act on.

## Extension Ideas
- Add a recursive CTE question (e.g. an org hierarchy or referral chain).
- Rewrite 2-3 queries using a different SQL dialect (e.g. Postgres vs.
  BigQuery/Snowflake syntax) and note the differences.
- Turn the recurring questions into parameterized views or stored queries a
  BI tool could call directly.
- Add a data-quality check query set (nulls where there shouldn't be,
  orphaned foreign keys, duplicate primary keys) as a companion deliverable.

## Skills Demonstrated
- Advanced SQL: window functions, CTEs, multi-table joins, subqueries
- Relational schema comprehension and ER modeling
- Translating ambiguous business questions into precise queries
- Query validation and basic performance awareness
- Data storytelling from query results to stakeholder-ready findings
