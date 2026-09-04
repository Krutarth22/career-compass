---
title: "Test Strategy and Risk-Based Test Plan"
track: "qa-automation-engineer"
difficulty_tier: "beginner"
estimated_hours: 10
role: "core"
skill_tags: ["test-strategy", "bug-reporting-and-triage", "technical-documentation"]
skill_prerequisites: ["http-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 2
---

# Test Strategy and Risk-Based Test Plan

## Production Workflow Mirrored
1. Reading requirements and identifying what could fail and how badly
2. Deciding what to test at which level and what to automate first
3. Writing test cases that are precise enough for someone else to run
4. Executing an exploratory session and logging defects properly
5. Reporting coverage and risk to a delivery team

## What You'll Build
A test strategy and plan for a real application (an open-source web app
you can run, or one you built): a risk assessment of its features, a
test-pyramid decision for each behavior, thirty to fifty written test
cases across functional, negative, and boundary categories, an
exploratory testing session with a charter, at least five well-written
bug reports from real defects you found, and a coverage and risk
summary.

## Student-Scope Notes
- The target should have a login, forms, and some business logic so
  there is real risk to assess. Many open-source demo apps have known
  bugs, which is ideal.
- Manual execution is expected here; automation starts in the next
  template. This template teaches what to automate and why.
- Bug reports go into a real tracker (a GitHub project or free-tier
  tracker), not a spreadsheet.

## Steps
1. Read the application's documentation and use it for an hour. Write a
   feature inventory and, for each feature, a likelihood-and-impact risk
   rating with a sentence of justification.
2. Write the strategy: which behaviors get unit, API, UI, or manual
   coverage, what will be automated first based on risk and stability,
   and what stays exploratory.
3. Write test cases for the top-risk features with preconditions, steps,
   expected results, and test data, including negative and boundary
   cases.
4. Execute the cases and record results honestly, including cases that
   were unclear or blocked.
5. Run a timeboxed exploratory session with a written charter (target,
   resources, information sought) and take notes as you go.
6. File at least five defects with a title that states the problem,
   reproduction steps, expected vs. actual, environment, severity and
   priority, and evidence (screenshot or log).
7. Triage your own defects with a written rationale for each severity
   and priority, and note any duplicates or non-bugs you almost filed.
8. Write the summary: coverage by feature and risk, defects by severity,
   residual risk, and the recommended automation order for the next
   template.

## Extension Ideas
- Add a traceability matrix from requirements to test cases.
- Add a session-based test management log across several sessions.
- Add accessibility and localization checks to the plan.
- Present the summary as a short readout to a peer or mentor.

## Skills Demonstrated
- Risk-based test planning and test-pyramid reasoning
- Precise test case authoring
- Exploratory testing with charters
- Professional defect reporting and triage

## Industry Relevance

Healthcare Software, Financial Services, Enterprise SaaS. Regulated and high-stakes sectors still require documented test plans and traceable defects, and QA leads there hire on the ability to assess risk and write cases and bug reports that developers act on. This plan is the artifact those interviews ask for.
