---
title: "Caching Layer and Rate Limiting for an API"
track: "backend-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["caching", "performance-profiling", "api-design", "http-fundamentals"]
skill_prerequisites: ["backend-frameworks", "relational-databases"]
project_prerequisites: ["rest-api-with-auth.md"]
prerequisite_learning_hours: 3
---

# Caching Layer and Rate Limiting for an API

## Production Workflow Mirrored
1. Measuring an endpoint's baseline latency and database load under load
2. Adding a read-through cache with explicit invalidation on writes
3. Setting HTTP cache headers so clients and CDNs can cache safely
4. Protecting the service with per-client rate limits and correct 429 responses
5. Proving the change with before/after measurements, not intuition

## What You'll Build
Take the API from `rest-api-with-auth.md` and add two production
protections: a Redis-backed cache for the hottest read endpoints with
invalidation on every write path, and a token-bucket rate limiter applied
per authenticated user. Deliver a benchmark report showing p50/p95 latency
and database query counts before and after.

## Student-Scope Notes
- Redis runs locally in Docker. An in-process dictionary is acceptable for
  the first pass, but finish on Redis so eviction and TTL behavior is real.
- Load is generated with a simple tool (k6, locust, hey, or a Python
  script). You need enough concurrency to see the cache matter, not a
  distributed load test.
- One rate-limit policy is enough. Skip tiered plans and distributed
  limiter coordination.

## Steps
1. Pick the two most-read endpoints and record baseline p50/p95 latency
   and database queries per request under a fixed load.
2. Implement a read-through cache: on miss, query the database, store the
   serialized response with a TTL; on hit, return the cached value.
3. Implement invalidation: every create, update, and delete path evicts or
   updates the affected keys. Write a test that proves a stale read is
   impossible after a write.
4. Add HTTP caching headers (ETag or Last-Modified plus Cache-Control) and
   handle conditional requests with 304 responses.
5. Implement a token-bucket rate limiter keyed by user id, stored in
   Redis, returning 429 with Retry-After and rate-limit headers.
6. Write tests for the limiter's boundary (the Nth request passes, the
   N+1th is rejected, the bucket refills after the window).
7. Re-run the load test and produce a before/after table for latency and
   database queries per request.
8. Write up: what you cached and why, the invalidation strategy and its
   failure modes, and what you would change for a multi-instance
   deployment.

## Extension Ideas
- Add cache stampede protection (request coalescing or probabilistic
  early expiration).
- Add a sliding-window limiter and compare its fairness to token bucket.
- Add per-endpoint limits for expensive operations on top of the per-user
  limit.

## Skills Demonstrated
- Read-through caching with correct write invalidation
- HTTP caching semantics and conditional requests
- Rate limiting design and correct 429 handling
- Load testing and evidence-based performance reporting

## Industry Relevance

Social Media, E-commerce, API Platforms. High-traffic products live or die on cache hit rates and abuse protection; a single hot endpoint without a cache can take down a database, and a missing rate limit invites scraping and denial-of-service. Engineers who can measure the problem, add the protection, and prove the improvement are exactly who these teams hire.
