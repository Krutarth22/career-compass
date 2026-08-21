---
title: "Streaming Ingestion Pipeline Basics"
track: "data-engineer"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["streaming-data-processing", "python", "data-pipelines"]
skill_prerequisites: ["python"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# Streaming Ingestion Pipeline Basics

## Production Workflow Mirrored
1. Produce events onto a stream/topic as they occur
2. Consume events continuously (not in scheduled batches)
3. Apply lightweight per-event or windowed processing
4. Handle out-of-order and duplicate events
5. Sink processed events into a queryable store
6. Track consumer lag / processing health
7. Handle consumer restarts without losing or duplicating data

## What You'll Build
A near-real-time pipeline that generates a simulated event stream (e.g.
clickstream events, IoT sensor readings, or order events), publishes it
onto a message broker, consumes it continuously, applies a windowed
aggregation (e.g. rolling event counts or averages per minute), and writes
results into a queryable sink — with the consumer able to restart cleanly
without duplicating or dropping already-processed events.

## Student-Scope Notes
- Runs on a single-node local Kafka (or Redpanda, which is lighter to run
  locally) instead of a managed, multi-broker production cluster — topic
  design, consumer groups, and offset management are the same concepts.
- The event producer is a script simulating realistic event arrival
  (including some out-of-order and duplicate events), not a real upstream
  system.
- Windowed processing is done with a simple in-process windowing
  implementation (or a lightweight library), not a full stream-processing
  engine like Flink — the concepts of watermarks/windows/late data are
  demonstrated at small scale.
- "Exactly-once-ish" behavior is achieved via idempotent sink writes keyed
  on event ID, not a fully transactional exactly-once pipeline.

## Steps
1. Design your event schema (e.g. `user_id`, `event_type`, `event_time`,
   `event_id` for dedup) and pick an event type to simulate.
2. Set up a local Kafka/Redpanda broker (Docker is easiest) and create a
   topic with a sensible number of partitions for your data volume.
3. Write a producer script that generates events continuously, including
   deliberately injecting some duplicate `event_id`s and some
   out-of-order `event_time`s to make the pipeline handle realistic mess.
4. Write a consumer that reads from the topic using a consumer group,
   deserializes events, and processes them.
5. Implement a windowed aggregation (e.g. tumbling 1-minute windows
   counting events per `event_type`), keyed by event_time not
   wall-clock-arrival-time.
6. Handle duplicates: dedupe on `event_id` before aggregating (e.g. a
   small in-memory or Redis-backed seen-set with TTL).
7. Sink aggregated results into a database table, writing idempotently
   (upsert on window + key) so re-processing doesn't double-count.
8. Track and log consumer lag (offset behind latest) as a basic health
   signal.
9. Kill and restart the consumer mid-stream; confirm it resumes from the
   last committed offset without losing or duplicating results.
10. Write up: how you handled out-of-order events and duplicates, what
    consumer lag told you, and how this would change at real production
    volume.

## Extension Ideas
- Add a dead-letter topic for events that fail to parse/validate.
- Implement a sliding (not just tumbling) window and compare results.
- Add schema evolution: change the producer's event schema mid-run and
  handle it gracefully on the consumer side (e.g. with Avro/Schema
  Registry).
- Swap the local broker for a managed streaming service and note what
  changes operationally.

## Skills Demonstrated
- Streaming/event-driven data pipeline design
- Consumer group semantics, offset management, and idempotent sinks
- Windowed aggregation and handling out-of-order/duplicate events
- Operational health signals for streaming systems (lag, restart safety)

## Industry Relevance

IoT & Industrial Monitoring, Ad Tech, E-commerce Clickstream. Businesses in these sectors need near-real-time visibility into events as they happen — a sensor reading, an ad impression, a click — rather than waiting for the next scheduled batch job, and getting that wrong means either double-counting events or silently dropping them after a crash. This project's windowed aggregation, dedup-on-event-ID, and restart-safe consumer offset handling are the exact concerns that separate a streaming pipeline these companies can trust from one that quietly corrupts its own metrics.
