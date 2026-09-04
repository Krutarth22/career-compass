---
title: "Performance and Load Test Campaign"
track: "qa-automation-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["performance-testing", "observability", "test-strategy", "data-visualization"]
skill_prerequisites: ["http-fundamentals", "linux-cli"]
project_prerequisites: ["api-test-suite-with-contracts.md"]
prerequisite_learning_hours: 3
---

# Performance and Load Test Campaign

## Production Workflow Mirrored
1. Defining performance requirements as measurable targets
2. Designing realistic load profiles from real usage patterns
3. Running load, stress, soak, and spike tests against a controlled
   environment
4. Correlating results with server-side metrics to find the bottleneck
5. Reporting findings with numbers and recommendations

## What You'll Build
A performance test campaign with k6, Locust, or Gatling against an
application you control (ideally one you can also observe server-side):
documented targets (p95 latency, error rate, throughput), scripted
scenarios reflecting a realistic mix, four test types (load, stress,
soak, spike), server metrics captured alongside, at least one
bottleneck identified and confirmed, and a report with charts and
recommendations.

## Student-Scope Notes
- Only test systems you own or run locally. Never load-test a third
  party's service.
- Run the target and the load generator on separate machines or
  containers so the generator does not skew results.
- One soak run of an hour is enough to look for leaks; multi-day soaks
  are out of scope.

## Steps
1. Write the performance requirements: target throughput, p95 and p99
   latency, and error-rate ceilings for the key endpoints, with a
   sentence on where each number comes from.
2. Script the scenarios with realistic think time, data variation, and
   authentication, reusing knowledge from the API suite.
3. Set up server-side observation: CPU, memory, database connections,
   and request latency histograms on the target.
4. Run the load test at the target throughput and record whether every
   requirement was met.
5. Run the stress test, ramping until errors or latency breach, and
   record the breaking point and what saturated first.
6. Run the soak test at moderate load for an hour and look for memory
   growth, connection leaks, or latency drift.
7. Run the spike test and record recovery time after the spike ends.
8. Correlate the client-side results with server metrics, name the
   bottleneck with evidence, and write the report with charts, the
   breaking point, and prioritized recommendations.

## Extension Ideas
- Add the load test as a CI stage with a threshold gate on p95.
- Fix the bottleneck (if you own the code) and re-run to prove it.
- Add distributed load generation from multiple containers.
- Add a browser-level performance test with a real-user metric.

## Skills Demonstrated
- Performance requirement definition
- Load, stress, soak, and spike test design and execution
- Correlating client results with server telemetry
- Performance reporting and recommendations

## Industry Relevance

E-commerce, Ticketing, Fintech. Launch days and flash sales in these sectors are won or lost on capacity planning, and performance test engineers are hired specifically to find the breaking point before customers do. A campaign report with a confirmed bottleneck is the standard evidence of that skill.
