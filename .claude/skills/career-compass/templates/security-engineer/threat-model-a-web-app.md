---
title: "Threat Model a Web Application"
track: "security-engineer"
difficulty_tier: "beginner"
estimated_hours: 10
role: "core"
skill_tags: ["threat-modeling", "web-application-security", "system-design", "technical-documentation"]
skill_prerequisites: ["http-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Threat Model a Web Application

## Production Workflow Mirrored
1. Diagramming a system's components, trust boundaries, and data flows
2. Enumerating threats systematically (STRIDE or similar) per element
3. Rating likelihood and impact to prioritize
4. Proposing mitigations and mapping them to owners and tickets
5. Reviewing the model with the engineers who build the system

## What You'll Build
A written threat model for a real web application (an open-source app
you can run locally, or one you built): a data-flow diagram with trust
boundaries, a STRIDE threat table for every element, a risk rating for
each threat, proposed mitigations, and a prioritized backlog, delivered
as a document an engineering team could act on.

## Student-Scope Notes
- Pick an application with authentication, a database, and at least one
  external integration so there is enough surface to model.
- Aim for fifteen to thirty well-reasoned threats, not an exhaustive
  list. Quality of reasoning is what reviewers look for.
- No exploitation in this template; that comes later in the track.

## Steps
1. Run the application locally and read its architecture and code enough
   to draw an accurate data-flow diagram: users, processes, data stores,
   external entities, and every data flow between them.
2. Mark the trust boundaries (browser to server, server to database,
   server to third party, admin vs. user).
3. For each element, walk STRIDE (spoofing, tampering, repudiation,
   information disclosure, denial of service, elevation of privilege) and
   record concrete threats with the specific entry point.
4. Rate each threat for likelihood and impact using a simple scale and
   justify the rating in a sentence.
5. Propose a mitigation for each threat, noting whether the app already
   has it, and cross-reference OWASP guidance where applicable.
6. Build the prioritized backlog: the top ten threats with mitigations
   written as actionable tickets.
7. Validate at least three threats by inspecting the code or
   configuration to confirm whether the mitigation exists.
8. Write the final document and a one-page executive summary, and
   present it (to a peer, a mentor, or a recorded video) as you would to
   an engineering team.

## Extension Ideas
- Add attack trees for the top three threats.
- Model the deployment infrastructure, not just the application.
- Re-run the model after a feature change and diff the results.
- Map threats to a compliance framework's controls.

## Skills Demonstrated
- Data-flow diagramming and trust-boundary analysis
- Systematic threat enumeration with STRIDE
- Risk rating and mitigation planning
- Security communication to engineering audiences

## Industry Relevance

Fintech, Healthcare, Enterprise SaaS. Threat modeling is a required step in secure development lifecycles across these sectors, and application security roles are often assessed on a candidate's ability to produce a model an engineering team will actually use. A well-argued document on a real application is the standard work sample.
