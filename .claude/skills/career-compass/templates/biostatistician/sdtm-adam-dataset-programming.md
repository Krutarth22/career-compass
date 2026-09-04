---
title: "CDISC SDTM and ADaM Dataset Programming"
track: "biostatistician"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["cdisc-standards", "sas-programming", "r-programming", "data-cleaning", "technical-documentation"]
skill_prerequisites: ["statistics"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# CDISC SDTM and ADaM Dataset Programming

## Production Workflow Mirrored
1. Mapping raw clinical data to SDTM domains per the implementation
   guide
2. Deriving analysis datasets (ADaM) with traceability
3. Validating against conformance rules
4. Documenting with specifications and define metadata
5. Double programming for quality control

## What You'll Build
SDTM and ADaM datasets from a public or synthetic raw clinical dataset
(the CDISC pilot data or a synthetic trial you generate): mapping
specifications, programs in SAS (university edition or an open
alternative) or R with the pharmaverse packages for at least five SDTM
domains and three ADaM datasets (ADSL, an efficacy dataset, an
adverse event dataset), conformance validation with a checker, define
metadata for the datasets, and an independent double-programming
check of one dataset.

## Student-Scope Notes
- SAS OnDemand for Academics is free; R with the pharmaverse is an
  accepted industry alternative.
- Follow the current SDTM and ADaM implementation guides and cite the
  versions.
- Double programming means a second, independent implementation
  compared programmatically.

## Steps
1. Obtain the raw data, study its structure, and read the relevant
   implementation guide sections.
2. Write the SDTM mapping specification for five domains (demographics,
   adverse events, exposure, vital signs, and one findings domain).
3. Program the SDTM domains with controlled terminology, and check
   structure and content against the specification.
4. Write the ADaM specifications with derivations and traceability to
   SDTM, and program ADSL, an efficacy dataset, and an adverse event
   analysis dataset.
5. Run a conformance checker on both SDTM and ADaM and resolve or
   document every finding.
6. Generate define metadata (or a define specification) covering
   variables, codelists, and derivations.
7. Independently re-program one ADaM dataset from the specification
   and compare with the first implementation; resolve discrepancies.
8. Write the programming documentation and a summary of conformance
   and quality control results.

## Extension Ideas
- Add a time-to-event ADaM dataset and a laboratory dataset.
- Automate the full flow with a build script and version control.
- Generate a reviewer's guide document.
- Implement the same domains in the other language and compare.

## Skills Demonstrated
- SDTM mapping and programming to standards
- ADaM derivation with traceability
- Conformance validation and define metadata
- Double-programming quality control

## Industry Relevance

Pharmaceutical Companies, Contract Research Organizations, Biotech, Regulatory Consulting. Standards-compliant datasets are required for every regulatory submission in these sectors, and statistical programmers are hired primarily on SDTM and ADaM competence. A validated dataset package with define metadata and double-programming evidence is the exact work sample those roles require.
