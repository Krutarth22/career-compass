---
title: "Statistical Analysis Plan and TLF Package"
track: "biostatistician"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["statistical-analysis-plans", "regression-modeling", "sas-programming", "r-programming", "cdisc-standards"]
skill_prerequisites: ["statistics"]
project_prerequisites: ["sdtm-adam-dataset-programming.md"]
prerequisite_learning_hours: 3
---

# Statistical Analysis Plan and TLF Package

## Production Workflow Mirrored
1. Writing a statistical analysis plan from the protocol
2. Producing mock tables, listings, and figures
3. Programming the outputs from analysis datasets with validation
4. Interpreting results and drafting the statistical results summary
5. Managing changes to the plan with versioning

## What You'll Build
A statistical analysis plan for your trial design with analysis
populations, endpoints, methods, handling of missing data, and
multiplicity, mock shells for at least fifteen tables, listings, and
figures, programs producing them from your ADaM datasets with an
independent validation of the primary efficacy table, a results
summary interpreting the primary and key secondary analyses, and a
versioned plan with a documented amendment.

## Student-Scope Notes
- Use the ADaM datasets you built; if using the pilot data, adapt the
  plan to its endpoints.
- Programs must be reproducible from a single driver script.
- Include at least one model-based analysis (a mixed model or a
  regression with covariates) beyond summary statistics.

## Steps
1. Write the statistical analysis plan following ICH E9: populations,
   endpoints, analysis methods, missing data, multiplicity, interim
   analyses, and sensitivity analyses.
2. Create mock shells for the tables, listings, and figures with
   numbering, titles, footnotes, and layout.
3. Program the demographic and disposition tables and the adverse
   event summaries from ADaM with a reusable macro or function set.
4. Program the primary efficacy analysis with the specified model,
   and the key secondary analyses.
5. Program the figures (Kaplan-Meier or a longitudinal profile, and a
   forest plot of subgroups).
6. Independently validate the primary efficacy table by double
   programming and reconcile.
7. Write the statistical results summary interpreting the outputs
   against the plan, including sensitivity analyses.
8. Amend the plan for a realistic change (a new sensitivity analysis),
   version it, and update the affected outputs with a change log.

## Extension Ideas
- Add a multiple-imputation sensitivity analysis.
- Build an automated output validation report comparing two runs.
- Produce a patient-narrative listing generator.
- Assemble a mock clinical study report statistical section.

## Skills Demonstrated
- Statistical analysis plan authoring to guidance
- Table, listing, and figure programming with validation
- Model-based efficacy analysis and interpretation
- Change control of statistical deliverables

## Industry Relevance

Pharmaceutical Companies, Contract Research Organizations, Biotech, Academic Trial Units. The analysis plan and the output package are the biostatistician's central deliverables in these sectors, and interview loops often include reviewing a plan or an output. A complete, validated package from plan to results summary shows readiness for study-level responsibility.
