---
title: "EHR Data Extraction and Cohort Definition"
track: "health-informatics-specialist"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["ehr-systems", "sql", "healthcare-data-standards", "hipaa-privacy-security", "data-cleaning"]
skill_prerequisites: ["sql"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# EHR Data Extraction and Cohort Definition

## Production Workflow Mirrored
1. Navigating an EHR data model to find clinical concepts
2. Defining a patient cohort with coded criteria and validating it
3. Extracting and cleaning data across encounters, diagnoses, labs, and
   medications
4. Applying privacy rules to the extract
5. Documenting definitions so clinicians trust the numbers

## What You'll Build
A cohort extraction from a public synthetic EHR dataset (MIMIC demo,
Synthea-generated data, or an OMOP sample): a data model map for the
tables used, a computable cohort definition (for example diabetic
patients with a recent hospitalization) using ICD, LOINC, and RxNorm
codes with a validation against a manual review of sample charts, a
cleaned analytic dataset with encounters, diagnoses, labs, and
medications, a de-identified version, and a data dictionary with
definitions and caveats.

## Student-Scope Notes
- Synthea data is free and needs no credentialing; MIMIC demo is a
  small credentialed set.
- Code lists should come from published value sets where possible and
  be cited.
- Manual validation means reviewing at least twenty patient records
  against the criteria.

## Steps
1. Load the dataset into a database and map the tables and
   relationships you need.
2. Define the cohort clinically, then translate it into code lists and
   temporal logic; document each decision.
3. Implement the cohort query in SQL and count the cohort with
   attrition at each criterion.
4. Validate by manually reviewing a sample of included and excluded
   records and computing agreement.
5. Extract the analytic tables (encounters, diagnoses, labs with units
   normalized, medications) for the cohort.
6. Clean the extract: duplicate encounters, implausible values, unit
   inconsistencies, and missing data patterns, with a report.
7. De-identify the dataset with a documented method and verify it.
8. Write the data dictionary and a cohort definition document with
   the attrition table and validation results.

## Extension Ideas
- Map the dataset to the OMOP common data model.
- Add a FHIR-based extraction from a test server.
- Build a phenotype library with multiple validated definitions.
- Compare cohort counts across two code list versions.

## Skills Demonstrated
- EHR data model navigation
- Computable phenotype definition and validation
- Clinical data cleaning and normalization
- Privacy-protective data preparation

## Industry Relevance

Health Systems, Academic Medical Centers, Health Analytics Vendors, Payers. Cohort definition and extraction is the starting point of nearly every informatics project in these sectors, and analysts are judged on whether clinicians trust their definitions. A validated cohort with a data dictionary is the foundational informatics portfolio piece.
