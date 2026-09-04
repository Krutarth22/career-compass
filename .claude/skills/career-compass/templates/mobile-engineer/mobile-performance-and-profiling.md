---
title: "Mobile Performance Profiling and Optimization"
track: "mobile-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["performance-profiling", "mobile-development", "debugging"]
skill_prerequisites: ["mobile-development"]
project_prerequisites: ["api-backed-list-detail-app.md"]
prerequisite_learning_hours: 3
---

# Mobile Performance Profiling and Optimization

## Production Workflow Mirrored
1. Measuring startup time, frame rate, memory, and battery on a real device
2. Finding jank with the platform profiler rather than guessing
3. Fixing the common culprits: main-thread work, oversized images,
   layout thrash, leaks
4. Setting a performance budget and checking it in CI
5. Reporting improvements with numbers

## What You'll Build
A performance pass on the app from `api-backed-list-detail-app.md` (or
your notes app): measured cold-start time, scroll frame rate on a long
list, memory over a session, and a network waterfall, followed by at least
four evidence-based optimizations and a before/after report, plus an
automated check that fails if startup time or app size regresses.

## Student-Scope Notes
- Measure on a mid-range physical device if at all possible; simulators
  hide the problems you are looking for.
- Use the platform profiler (Instruments, Android Studio Profiler, or
  Flipper/DevTools for cross-platform). Learning the tool is part of the
  work.
- Four optimizations with evidence beats twelve from a checklist.

## Steps
1. Record baselines: cold start to first interactive frame, frame
   timings while scrolling the full list, memory at start and after five
   minutes of use, and the network waterfall on first load.
2. Seed the list with a thousand items and heavy images to make problems
   visible, then profile the scroll and identify dropped frames and their
   cause.
3. Fix list performance: image downsampling and caching, cell reuse or
   lazy composition, moving decoding off the main thread.
4. Profile startup and defer non-critical work (analytics, SDK
   initialization) off the launch path.
5. Hunt for a memory leak with the profiler (retain cycles, listeners
   not removed) and fix at least one, proving it with a before/after
   memory graph.
6. Reduce app size: audit assets and dependencies, strip unused
   resources, and record the size change.
7. Add a CI check that measures app size and, where the platform
   supports it, startup time, and fails on regression past a threshold.
8. Write the report: baseline vs. after for every metric, the profiler
   evidence for each fix, and what you would monitor in production.

## Extension Ideas
- Add production performance monitoring with a crash and performance SDK.
- Add a low-end device test matrix and document the results.
- Add battery profiling for a background sync path.
- Add startup tracing with custom spans.

## Skills Demonstrated
- Profiling startup, rendering, memory, and network on mobile
- Fixing jank, leaks, and startup bloat with evidence
- App size auditing
- Performance budgets in CI

## Industry Relevance

Social Media, Gaming Companions, Emerging-Market Consumer Apps. On mid-range devices and slow networks, performance decides retention, and mobile teams in these sectors have dedicated performance goals. A profiler-backed before/after report is exactly the artifact that shows you can hit them.
