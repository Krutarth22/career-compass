---
title: "Distributed Data Processing with Spark"
track: "data-engineer"
difficulty_tier: "advanced"
estimated_hours: 18
role: "core"
skill_tags: ["distributed-data-processing", "python", "batch-processing"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: []
prerequisite_learning_hours: 12
---

# Distributed Data Processing with Spark

## Production Workflow Mirrored
1. Land a large, partitioned raw dataset in a file store
2. Read it into a distributed processing engine without loading it all
   into a single machine's memory
3. Apply transformations (filters, joins, aggregations) that Spark
   parallelizes across partitions
4. Deliberately handle skew and shuffle-heavy operations (large joins,
   group-bys)
5. Write output back out partitioned appropriately for downstream
   consumption
6. Inspect the execution plan and Spark UI to understand where time is
   actually going
7. Tune partitioning/caching based on what the plan and UI reveal

## What You'll Build
A PySpark job that processes a dataset larger than comfortably fits in
memory on a single machine (e.g. several GB of synthetic or public
clickstream/transaction data), performing a large join and a
group-by-aggregate, reading and writing partitioned Parquet, with a
written analysis of the job's execution plan and where a naive first
version was slow versus a tuned second version.

## Student-Scope Notes
- Runs on a local Spark instance (single machine, multiple cores) via
  `pyspark`, not a real multi-node cluster (EMR/Databricks/Dataproc) — the
  partitioning, shuffle, and execution-plan concepts transfer directly;
  only horizontal scale across machines differs.
- Dataset size is chosen to be "larger than trivial" (enough to force real
  partitioning/shuffle behavior, a few GB) rather than true
  production-scale (terabytes) — the point is learning to read a Spark
  plan and reason about shuffle cost, not proving cluster scalability.
- You are required to produce and compare two versions of the same job (a
  naive one and a tuned one) — this is the core learning artifact of the
  template, not optional polish.
- Cluster resource management, YARN/Kubernetes scheduling, and multi-tenant
  cluster concerns are out of scope.

## Steps
1. Get or generate a dataset large enough to be awkward in pandas on a
   single machine (a few GB) — e.g. synthetic transaction records plus a
   smaller reference/dimension dataset to join against.
2. Write the raw data out as partitioned Parquet (partition by a sensible
   column like date or region) to simulate a realistic data lake layout.
3. Set up local PySpark; read the partitioned Parquet dataset into a
   DataFrame, confirming partition pruning works when you filter on the
   partition column.
4. Write a first, naive version of the job: join the large dataset against
   the reference dataset, then group-by and aggregate. Get it correct
   first, ignore performance.
5. Run `.explain()` on the naive job and open the Spark UI; identify the
   expensive stages (shuffle size, spill, skewed partition sizes).
6. Apply at least two concrete optimizations based on what you found —
   candidates: broadcast join for the small reference dataset, repartition
   before the group-by to reduce skew, caching a reused intermediate
   DataFrame, pushing filters earlier.
7. Re-run with the tuned version; compare wall-clock time and the Spark UI
   stage breakdown against the naive version.
8. Write the aggregated output back out as partitioned Parquet, sized
   sensibly for downstream consumers (avoid the small-files problem).
9. Write up: what the naive plan's bottleneck was, which optimization
   mattered most and why, and how you'd expect this to behave differently
   on a real multi-node cluster.

## Extension Ideas
- Add a skewed key deliberately and demonstrate salting to fix it.
- Convert one stage to use Spark SQL instead of the DataFrame API and
  compare readability/plan differences.
- Run the same job against a small real multi-node setup (e.g. a free-tier
  Databricks community cluster) and compare.
- Add a window function (e.g. running totals per partition) to the
  pipeline.

## Skills Demonstrated
- Distributed data processing fundamentals (partitioning, shuffle,
  broadcast joins, skew handling)
- Reading and acting on a Spark execution plan and UI
- Batch processing of larger-than-memory datasets
- Performance tuning grounded in observed bottlenecks, not guesswork
