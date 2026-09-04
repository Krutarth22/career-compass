---
title: "Clinical Decision Support Rule Design and Evaluation"
track: "health-informatics-specialist"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["clinical-decision-support", "ehr-systems", "sql", "user-research", "technical-documentation"]
skill_prerequisites: ["sql"]
project_prerequisites: ["ehr-data-extraction-and-cohort-definition.md"]
prerequisite_learning_hours: 2
---

# Clinical Decision Support Rule Design and Evaluation

## Production Workflow Mirrored
1. Identifying a clinical need and the evidence for an intervention
2. Designing a rule with triggers, logic, and an action that fits the
   workflow
3. Estimating alert volume and precision before deployment
4. Reviewing with clinicians and refining
5. Planning monitoring for alert fatigue and effectiveness

## What You'll Build
A clinical decision support design package: a clinical need statement
with evidence, a rule specification (trigger, inclusion and exclusion
logic with codes, action, and presentation) following the five rights,
a retrospective simulation on your synthetic EHR data estimating firing
volume, positive predictive value against a chart-review standard,
and override likelihood, a clinician review session with documented
feedback and changes, an implementation prototype (a CDS Hooks service
or a rule engine), and a monitoring plan.

## Student-Scope Notes
- Choose a well-evidenced intervention (a drug interaction, a screening
  reminder, a sepsis screen) and cite guidelines.
- Clinician review can be a clinical student, a nurse, or a physician
  you know; record their feedback faithfully.
- The prototype can be minimal but must execute the logic against data.

## Steps
1. Write the clinical need and the evidence summary with citations.
2. Specify the rule: who, what, when, where, and how, with code lists
   and temporal logic.
3. Simulate the rule retrospectively on the data to estimate firings
   per encounter and per clinician per day.
4. Review a sample of firings against clinical judgment (chart review)
   to estimate positive predictive value and refine the logic.
5. Hold a clinician review session, walk through examples, capture
   feedback, and revise the rule and its presentation.
6. Build the prototype that evaluates the logic and returns a
   recommendation (a CDS Hooks service or equivalent).
7. Write the monitoring plan: firing rates, override rates and
   reasons, outcome measures, and the review cadence.
8. Assemble the design package with the specification, simulation
   results, review notes, prototype, and monitoring plan.

## Extension Ideas
- Implement the rule in an EHR sandbox's rule engine.
- Add a machine-learning risk score as an alternative trigger and
  compare.
- Design a non-interruptive presentation and compare expected
  effectiveness.
- Run a usability test of the alert design.

## Skills Demonstrated
- Evidence-based decision support specification
- Retrospective simulation of alert performance
- Clinician-centered design review
- Implementation prototyping and monitoring planning

## Industry Relevance

Health Systems, EHR Vendors, Digital Health Companies, Clinical Informatics Departments. Decision support that clinicians tolerate and act on is a core deliverable of clinical informatics in these sectors, and alert fatigue is the most common failure. A design package with simulated performance and clinician review demonstrates the discipline the field demands.
