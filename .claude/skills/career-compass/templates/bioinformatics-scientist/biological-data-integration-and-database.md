---
title: "Biological Data Integration and Queryable Database"
track: "bioinformatics-scientist"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["sql", "python", "database-design", "data-pipelines", "api-design", "reproducible-research"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Biological Data Integration and Queryable Database

## Production Workflow Mirrored
1. Pulling data from multiple public biological databases and APIs
2. Modeling entities (genes, variants, samples, annotations) relationally
3. Loading with identifier mapping and provenance
4. Exposing the data through queries and a small API or dashboard
5. Keeping it updated and documented

## What You'll Build
A relational database integrating at least three public sources for a
gene set or disease area of your choice (gene annotations, variants
and their clinical significance, expression summaries, pathway
membership, literature counts): a schema with identifier mapping and
provenance, loading scripts that are idempotent and rerunnable,
validation checks, a set of documented analytical queries, a small
API or dashboard for common questions, and a data dictionary.

## Student-Scope Notes
- SQLite or Postgres is enough; the modeling and identifier mapping
  are the difficulty.
- Respect each source's terms of use and rate limits; cache downloads.
- Scope to a few hundred genes so the whole thing is tractable.

## Steps
1. Choose the biological scope and the sources, and read each source's
   data model and access method.
2. Design the schema: entities, relationships, identifier tables for
   cross-referencing, and provenance columns (source, version, date).
3. Write loading scripts per source with identifier mapping, handling
   ambiguous and missing mappings explicitly.
4. Add validation checks: referential integrity, expected counts,
   duplicate detection, and a load report.
5. Write and document ten analytical queries that answer real
   questions (which genes have pathogenic variants and high expression
   in a tissue, for example).
6. Build a small API or dashboard exposing three of those queries.
7. Rerun the full load from scratch to prove idempotence, and add a
   scheduled update path with change detection.
8. Write the data dictionary and a README with the schema diagram,
   sources, licenses, and how to rerun.

## Extension Ideas
- Add a graph representation for pathways and query it.
- Add full-text search over annotations.
- Add versioned snapshots and a diff between releases.
- Containerize the whole stack for one-command deployment.

## Skills Demonstrated
- Biological data modeling with identifier mapping
- Rerunnable, validated loading pipelines
- Analytical SQL over integrated biology data
- Serving integrated data through an API or dashboard

## Industry Relevance

Pharmaceutical Informatics, Biotech Platforms, Diagnostics, Research Databases. Integrating heterogeneous biological data with reliable identifier mapping is a constant need in these sectors, and bioinformaticians who can model and serve it are valued beyond analysis alone. A documented, rerunnable integration with real queries is a practical portfolio piece.
