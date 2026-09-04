---
title: "Security Questionnaire and Architecture Review Response"
track: "solutions-engineer"
difficulty_tier: "intermediate"
estimated_hours: 10
role: "core"
skill_tags: ["solution-architecture", "web-application-security", "technical-documentation", "networking-fundamentals"]
skill_prerequisites: ["http-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Security Questionnaire and Architecture Review Response

## Production Workflow Mirrored
1. Answering a customer's security questionnaire accurately and completely
2. Producing architecture and data-flow documentation for a customer's
   review board
3. Explaining authentication, encryption, tenancy, and data handling
   clearly to non-experts
4. Tracking gaps and commitments across the review
5. Presenting to a customer's security and architecture reviewers

## What You'll Build
A complete review package for a real product you know well (the same
one from your other templates): a filled-in standard security
questionnaire (a public one such as CAIQ or SIG Lite), a reference
architecture diagram with data flows and trust boundaries, an
integration architecture for a typical customer deployment (SSO, network
access, data residency), a gap register with mitigations, and a recorded
fifteen-minute architecture review presentation.

## Student-Scope Notes
- Answers must be accurate for the product as it is; if you do not know,
  find out from documentation or mark it as unknown with a plan to
  confirm. Guessing fails the exercise.
- Use the product's public security documentation as your source of
  truth and cite it.
- Present to a peer playing the reviewer, who should ask hard follow-ups.

## Steps
1. Read the product's security, compliance, and architecture
   documentation end to end and build a fact sheet with citations.
2. Complete the questionnaire, answering each item with the fact and its
   source, and marking gaps honestly.
3. Draw the reference architecture: components, data stores, external
   dependencies, data flows, encryption points, and trust boundaries.
4. Draw the customer integration architecture for a typical enterprise:
   identity (SSO, SCIM), network access (allowlists, private
   connectivity), data residency, and logging export.
5. Build the gap register: every "no" or "partial" answer, its risk, the
   mitigation or compensating control, and the commitment status.
6. Prepare the review presentation: the architectures, the top ten
   questions reviewers ask and their answers, and the gap register.
7. Deliver the presentation to a peer acting as the reviewer, handle
   follow-up questions, and record it.
8. Write up the questions you could not answer, how you would get the
   answers, and what you would change in the package.

## Extension Ideas
- Map the questionnaire answers to a compliance framework's controls.
- Add a data-processing diagram for privacy review.
- Build a reusable answer library with citations.
- Add a threat model for the customer integration architecture.

## Skills Demonstrated
- Accurate security questionnaire completion with sources
- Reference and integration architecture documentation
- Gap tracking and commitment management
- Presenting to security and architecture reviewers

## Industry Relevance

Enterprise SaaS, Fintech Vendors, Healthcare Technology. Every enterprise deal in these sectors passes through a security review, and solutions engineers who can answer accurately, draw the architecture, and handle a review board shorten sales cycles measurably. A complete, cited review package is a differentiating portfolio piece.
