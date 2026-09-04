---
title: "CRF Design and EDC Database Build"
track: "clinical-data-manager"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["edc-systems", "cdisc-standards", "gcp-and-clinical-regulations", "technical-documentation"]
skill_prerequisites: []
project_prerequisites: []
prerequisite_learning_hours: 3
---

# CRF Design and EDC Database Build

## Production Workflow Mirrored
1. Translating a protocol's schedule of assessments into case report forms
2. Designing forms with standards-aligned fields and controlled terms
3. Building the database in an EDC system with visit structure
4. Testing the build against specifications before go-live
5. Documenting the build for audit

## What You'll Build
A complete electronic data capture build for a realistic protocol
(a published protocol or a synthetic one you write): a CRF
specification aligned to CDASH with field definitions, formats,
controlled terminology, and completion guidelines, the database built
in REDCap (free) or an EDC trial environment with the visit schedule
and forms, a user acceptance test plan executed with documented
results, and a build documentation package with version control.

## Student-Scope Notes
- REDCap is free through many institutions and has a public demo;
  its data dictionary import makes specifications testable.
- Cover at least eight forms including demographics, medical history,
  adverse events, concomitant medications, vital signs, and a primary
  endpoint form.
- User acceptance testing must be executed and recorded, not just
  planned.

## Steps
1. Read the protocol and extract the schedule of assessments into a
   visit-by-form matrix.
2. Write the CRF specification: each form, its fields, types, formats,
   code lists, required flags, and the CDASH mapping.
3. Write completion guidelines for the forms that need them.
4. Build the forms and the visit structure in the EDC system with
   branching logic and calculated fields.
5. Add validation rules (range, required, logic) in the build,
   distinguishing hard and soft checks.
6. Write the user acceptance test plan with test cases per form and
   per rule, including negative cases.
7. Execute the tests, record results, fix defects, and re-test; sign
   off the build.
8. Assemble the build documentation: specification, data dictionary
   export, test evidence, and a version log.

## Extension Ideas
- Add role-based permissions and an audit trail review.
- Add a laboratory data import specification.
- Build a second version with a protocol amendment and migrate.
- Generate a blank CRF PDF book for the trial master file.

## Skills Demonstrated
- CRF design aligned to data standards
- EDC database configuration with logic and validation
- User acceptance testing with evidence
- Build documentation for audit readiness

## Industry Relevance

Contract Research Organizations, Pharmaceutical Companies, Academic Research Organizations, Medical Device Sponsors. Every trial in these sectors starts with a database build, and clinical data managers are hired on their ability to specify, build, and test one to standards. A documented build with executed acceptance tests is the foundational portfolio piece.
