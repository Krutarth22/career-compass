---
title: "Find and Fix Vulnerabilities in a Deliberately Vulnerable App"
track: "security-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["web-application-security", "vulnerability-assessment", "secure-code-review", "automated-testing"]
skill_prerequisites: ["backend-frameworks", "http-fundamentals"]
project_prerequisites: ["threat-model-a-web-app.md"]
prerequisite_learning_hours: 4
---

# Find and Fix Vulnerabilities in a Deliberately Vulnerable App

## Production Workflow Mirrored
1. Running scanners and manual testing against a target you are
   authorized to test
2. Confirming findings with proof and rating their severity
3. Writing a clear vulnerability report developers can act on
4. Fixing the root cause in code, not just the symptom
5. Adding regression tests so the vulnerability cannot return

## What You'll Build
A complete assess-report-fix cycle against a deliberately vulnerable
training application you run locally (OWASP Juice Shop, DVWA, or
WebGoat): identify at least eight distinct vulnerability classes
(injection, XSS, broken access control, insecure deserialization, weak
crypto, etc.) using a mix of automated scanning and manual testing,
write a professional report, then fix at least four of them in the
source code with regression tests.

## Student-Scope Notes
- Only test applications you run yourself, locally, that are designed
  for this purpose. Never point these techniques at systems you do not
  own or have written authorization to test.
- Use widely available tooling (a proxy such as ZAP or Burp Community, a
  dependency scanner, a SAST tool). Learning the tools is part of the
  work.
- Fixing four vulnerabilities properly, with tests, is worth more than
  finding twenty.

## Steps
1. Stand up the training application in Docker and read its
   documentation on the vulnerability classes it contains.
2. Run a dependency scanner and a SAST tool against its source and
   triage the results: true positives, false positives, and duplicates.
3. Run a DAST scan through a proxy, then manually verify each reported
   finding and discard the ones that do not reproduce.
4. Manually test for at least three classes automated tools miss well
   (business-logic access control, IDOR, workflow bypass) using the
   threat-modeling approach from the previous template.
5. Write the report: for each finding, a description, reproduction
   steps, evidence, CVSS or a simple severity rating, and a recommended
   fix. Include an executive summary.
6. Pick four findings across different classes and fix the root cause in
   code (parameterized queries, output encoding, authorization checks,
   safe deserialization), not with a WAF rule or input blocklist.
7. Write a regression test for each fix that fails on the vulnerable code
   and passes on the fixed code.
8. Re-run the scanners to confirm the fixes and write up what each tool
   caught, what it missed, and what only manual testing found.

## Extension Ideas
- Add the scanners to a CI pipeline for the application with a
  severity threshold that fails the build.
- Fix an additional four vulnerabilities and aim for a clean DAST scan.
- Write a secure-coding guideline for the team based on the classes you
  fixed.
- Compare two SAST tools on the same codebase and report on their
  precision.

## Skills Demonstrated
- Vulnerability assessment with SAST, DAST, and manual testing
- Triage, severity rating, and professional reporting
- Root-cause remediation in application code
- Security regression testing

## Industry Relevance

Fintech, E-commerce, Healthcare Software. Application security engineers in these sectors spend much of their time triaging scanner output, confirming real issues, and working with developers on fixes, and hiring loops often include a report-writing exercise. A report plus code fixes plus tests on a well-known training target is a complete, safe demonstration of that workflow.
