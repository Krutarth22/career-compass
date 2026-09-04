---
title: "Application Security Program Capstone"
track: "security-engineer"
difficulty_tier: "advanced"
estimated_hours: 24
role: "capstone"
skill_tags: ["threat-modeling", "web-application-security", "vulnerability-assessment", "security-monitoring", "ci-cd", "technical-documentation"]
skill_prerequisites: ["backend-frameworks", "linux-cli", "git-version-control"]
project_prerequisites: ["threat-model-a-web-app.md", "vulnerable-app-find-and-fix.md"]
prerequisite_learning_hours: 4
---

# Application Security Program Capstone

## Production Workflow Mirrored
1. Assessing an application's security posture from architecture to code
2. Prioritizing a remediation roadmap by risk
3. Building security into the pipeline so fixes stay fixed
4. Adding detection so remaining risk is visible
5. Reporting posture to engineering and leadership audiences

## What You'll Build
A complete application security program for one real application you
own or an open-source project you can fork: a threat model, an
assessment with findings, a prioritized remediation roadmap, at least
six fixes shipped with tests, a hardened pipeline with scanning and
secret detection, security logging with at least three detection rules,
and two reports: a technical one for engineers and a one-page posture
summary for leadership.

## Student-Scope Notes
- Reuse the threat model, assessment techniques, pipeline hardening, and
  detection stack from earlier templates. The capstone integrates them
  around one application.
- If you use an open-source project, keep everything in your own fork
  and follow the project's responsible disclosure policy for anything
  real you find.
- Six fixes with tests is the floor; measurable posture improvement is
  the goal.

## Steps
1. Choose the application and write the program plan: scope, the
   assessment approach, success metrics (findings closed by severity,
   pipeline gates in place, detection coverage).
2. Produce or refresh the threat model for the application as it exists
   today.
3. Run the assessment: SAST, dependency and container scanning, DAST,
   and manual testing of access control and business logic. Produce the
   findings report with severities.
4. Build the remediation roadmap: order findings by risk and effort, and
   write each as a ticket with acceptance criteria.
5. Ship at least six fixes across different vulnerability classes, each
   with a regression test, and re-run the scanners to prove closure.
6. Harden the pipeline with the controls from
   `dependency-and-pipeline-security.md` (or a minimal set: scanning
   gates, secret detection, pinned dependencies).
7. Add security event logging and three tuned detection rules for the
   highest-risk remaining threats from the model.
8. Write the technical report (model, findings, fixes, controls,
   coverage) and the leadership one-pager (posture before and after,
   residual risk, next steps), and present both.

## Extension Ideas
- Add a bug bounty or responsible disclosure policy and intake process.
- Add security champions guidance for the development team.
- Add a quarterly re-assessment schedule with automated evidence
  collection.
- Map the program to a framework such as OWASP SAMM and score it.

## Skills Demonstrated
- End-to-end application security assessment and remediation
- Risk-based prioritization and roadmap communication
- Pipeline and detection controls that sustain posture
- Reporting to both engineering and leadership audiences

## Industry Relevance

Fintech, Healthcare, Enterprise SaaS. Security engineers in these sectors are hired to raise and sustain the security posture of real products, not just to find bugs, and the ability to run the whole loop from model to fix to detection to report is what separates senior candidates. A documented program on a real application is exactly the portfolio that demonstrates it.
