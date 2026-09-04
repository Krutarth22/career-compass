---
title: "Quality Engineering Capstone"
track: "qa-automation-engineer"
difficulty_tier: "advanced"
estimated_hours: 24
role: "capstone"
skill_tags: ["test-strategy", "api-testing", "end-to-end-testing", "performance-testing", "ci-cd", "bug-reporting-and-triage", "technical-documentation"]
skill_prerequisites: ["javascript", "python", "git-version-control"]
project_prerequisites: ["api-test-suite-with-contracts.md", "ui-end-to-end-automation-framework.md"]
prerequisite_learning_hours: 4
---

# Quality Engineering Capstone

## Production Workflow Mirrored
1. Owning quality for an application from strategy through release
2. Building and maintaining automation at every level of the pyramid
3. Gating releases on evidence and reporting risk honestly
4. Finding, reporting, and verifying fixes for real defects
5. Measuring and improving the test program over time

## What You'll Build
A complete quality program for one application you can run and change
(an open-source project you fork, or one you built): a test strategy,
unit-level contributions, the API and UI suites from earlier templates
extended to full critical-path coverage, a performance baseline, a CI
pipeline with quality gates, a defect log with at least ten real
findings and verified fixes, and a program report with metrics over at
least three release cycles.

## Student-Scope Notes
- Reuse and extend the suites and pipeline you built; the capstone is
  about running them as a program against a changing codebase.
- Release cycles can be weekly tags of your fork with real changes
  (your own or upstream's).
- Ten real defects is the floor; verified fixes are what count.

## Steps
1. Write the program plan: strategy, coverage goals per level, the
   metrics you will track (defect escape rate, pass rate, pipeline
   time, flake rate), and the release gate policy.
2. Extend the API suite to full endpoint coverage and add unit tests to
   at least one module you found under-tested.
3. Extend the UI suite to every critical journey identified in the
   strategy and stabilize it below your flake threshold.
4. Establish a performance baseline for the top endpoints and add a
   threshold gate to the pipeline.
5. Run the first release cycle: execute the gates, run an exploratory
   session, file defects, and produce the release readiness report.
6. Fix or shepherd fixes for the defects (in your fork, or via upstream
   pull requests), verify each with a regression test, and re-release.
7. Run at least two more cycles, tracking the metrics each time and
   making at least one program improvement per cycle based on them.
8. Write the program report: metrics trend, defects found and closed,
   coverage evolution, what the gates caught, and a retrospective, and
   publish the portfolio README.

## Extension Ideas
- Add contract testing with a separate client repository.
- Add chaos experiments to the release gates.
- Add test-impact analysis to cut pipeline time.
- Contribute tests upstream and document the review process.

## Skills Demonstrated
- Quality ownership across strategy, automation, and release
- Multi-level automation maintained against a changing codebase
- Defect lifecycle management with verification
- Metrics-driven test program improvement

## Industry Relevance

Enterprise SaaS, Fintech, Healthcare Software. Senior QA and SDET roles in these sectors are accountable for release quality rather than individual test scripts, and hiring managers want evidence of running a program with metrics over time. Three measured release cycles on a real codebase provide exactly that.
