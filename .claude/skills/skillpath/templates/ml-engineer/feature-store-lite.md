---
title: "Feature Store Lite: Batch + Online Lookup"
track: "ml-engineer"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["feature-engineering", "data-pipelines", "python", "sql"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# Feature Store Lite: Batch + Online Lookup

## Production Workflow Mirrored
1. Raw event/data source ingestion
2. Offline batch feature computation
3. Feature versioning & a feature registry (names, types, owners)
4. Materializing features into a fast online lookup store
5. Point-in-time correctness (no leaking future data into training features)
6. Serving features to a downstream consumer (e.g. a model or API)

## What You'll Build
A minimal feature store for a dataset of your choice: a batch job that
computes a handful of features from raw data, a small registry describing
them, and a fast key-based lookup service so a downstream model or API can
fetch the latest feature values for an entity (user, product, etc.) by ID.

## Student-Scope Notes
- Offline batch job is a plain Python/pandas or SQL job you run manually or
  on a schedule, not a distributed Spark pipeline.
- Online store is a local key-value store (SQLite, Redis, or even a JSON
  file behind a lookup function), not a managed low-latency production store.
- Point-in-time correctness is handled with a simple timestamp-filtering
  rule you implement and test yourself, not a formal feature-store framework.

## Steps
1. Pick a raw dataset with a natural entity id and timestamped events (e.g.
   user clickstream, transactions, sensor readings).
2. Design 5-10 features (aggregates, ratios, recency/frequency) and write a
   feature registry (name, description, dtype, source columns).
3. Build the offline batch job computing these features from raw data.
4. Implement a point-in-time correctness check: given a training example's
   timestamp, only aggregate features from data strictly before it.
5. Materialize the latest feature values into an online key-value store.
6. Build a small lookup function/endpoint: given an entity id, return its
   current feature vector.
7. Write a test that deliberately tries to leak future data and confirms
   your point-in-time logic catches it.
8. Write up: what point-in-time correctness bugs would have looked like
   silently in production, and how your design prevents them.

## Extension Ideas
- Add feature freshness/staleness monitoring (age of last materialization).
- Support multiple feature "views" that compose into different feature sets
  per model.
- Add a simple backfill command to recompute features over a historical
  date range.
- Wrap the online lookup in a small REST endpoint (pairs naturally with the
  model-serving template).

## Skills Demonstrated
- Feature engineering and feature registry design
- Batch data pipeline construction
- Point-in-time correctness reasoning for ML training data
- Online/offline feature store architecture at a small scale

## Industry Relevance

Fraud Detection, Personalization/Recommendation, Credit Risk. Real-time ML systems in these sectors need to fetch a user's or transaction's current feature values in milliseconds while also guaranteeing the exact same feature logic was used consistently at training time, and a point-in-time correctness bug silently leaks future information into training data, producing a model that looks great offline and fails online. This project's registry, batch computation, and leakage-testing discipline mirrors the feature-store architecture that keeps these production ML systems both fast and honest.
