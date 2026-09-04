---
title: "Quality Gates and Test Reporting in CI"
track: "qa-automation-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["ci-cd", "automated-testing", "test-strategy", "docker"]
skill_prerequisites: ["git-version-control", "linux-cli"]
project_prerequisites: ["api-test-suite-with-contracts.md"]
prerequisite_learning_hours: 3
---

# Quality Gates and Test Reporting in CI

## Production Workflow Mirrored
1. Deciding which checks block a merge and which only inform
2. Running unit, API, and UI suites at the right pipeline stages
3. Spinning up ephemeral environments for tests in CI
4. Publishing results where the team sees them, with trends over time
5. Managing flaky tests without hiding real failures

## What You'll Build
A CI quality pipeline for an application with the API suite from
`api-test-suite-with-contracts.md` (and the UI suite if you built it):
staged jobs (static checks, unit, API against an ephemeral environment,
UI on a production build), required-check configuration, a merged
report with pass rates and duration trends, a flaky-test quarantine
policy with automatic detection, and a documented gate policy.

## Student-Scope Notes
- GitHub Actions or GitLab CI free tier is sufficient.
- The ephemeral environment is docker-compose inside the CI job; no
  cloud environments required.
- Trend reporting can be a simple stored history in the repository or a
  free-tier dashboard.

## Steps
1. Write the gate policy: which checks are required to merge, which run
   nightly, which are advisory, and the SLA for fixing a red main branch.
2. Build the static stage: lint, formatting, type checks, and dependency
   audit, all as required checks.
3. Build the API stage: start the application and database in
   docker-compose within the job, wait for health, run the API suite,
   and tear down.
4. Build the UI stage against a production build with the E2E framework
   if available, sharded across parallel jobs.
5. Merge all results into one report with JUnit outputs, publish it on
   the pull request, and store run history for trend charts of pass
   rate and duration.
6. Implement flake detection: rerun failures once in a separate step,
   and tag tests that pass on retry as flaky in the report without
   letting them pass silently.
7. Create the quarantine process: a labelled list of flaky tests that
   run but do not block, with an owner and an expiry date.
8. Verify the gates by opening pull requests that break each stage, and
   write up the pipeline diagram, timings, and the policy.

## Extension Ideas
- Add test-impact analysis to run only the tests affected by a change.
- Add code coverage with a ratchet that only allows increases.
- Add a nightly full-matrix run with a summary posted to chat.
- Add a dashboard of defect escape rate against test coverage.

## Skills Demonstrated
- Pipeline staging and required-check design
- Ephemeral test environments in CI
- Test reporting and trend analysis
- Flake management and quarantine policy

## Industry Relevance

SaaS, Fintech, Enterprise Software. Quality engineering roles in these sectors own the pipeline's gates and the trust the team places in them, and interviewers ask how you handle flakiness and what should block a merge. A working pipeline with a written policy demonstrates both judgment and execution.
