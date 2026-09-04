---
title: "Cell Culture and Assay Development"
track: "research-scientist-life-sciences"
difficulty_tier: "intermediate"
estimated_hours: 18
role: "core"
skill_tags: ["cell-culture", "assay-development", "experimental-design-biology", "statistics", "lab-records-data-integrity"]
skill_prerequisites: ["molecular-biology-techniques"]
project_prerequisites: ["molecular-biology-core-techniques-portfolio.md"]
prerequisite_learning_hours: 3
---

# Cell Culture and Assay Development

## Production Workflow Mirrored
1. Maintaining cell lines aseptically with documented passage history
2. Developing a plate-based assay with optimization of key parameters
3. Validating the assay for robustness and reproducibility
4. Running a small screen or dose-response experiment
5. Analyzing with proper statistics and reporting

## What You'll Build
A cell-based assay developed and validated in a lab with culture
facilities: aseptic maintenance of a cell line with a passage log and
contamination checks, an assay (viability, reporter, or an ELISA on
supernatants) optimized for cell density, incubation time, and
reagent concentration, validation with Z-factor, intra- and
inter-assay variability, and edge effects, a dose-response experiment
with a reference compound fitted to a model, and a report following
assay validation guidance.

## Student-Scope Notes
- Requires access to a cell culture facility; university and
  community labs are the typical routes.
- Use a robust, well-characterized cell line and a standard viability
  assay if in doubt.
- Compute the assay quality metrics yourself in R or Python.

## Steps
1. Train in aseptic technique, thaw and maintain the cell line, and
   keep a passage log with morphology checks and a mycoplasma test if
   available.
2. Choose the assay and design the optimization experiments for
   density, time, and reagent concentration with a matrix.
3. Run the optimization, analyze signal-to-background and variability,
   and select conditions.
4. Validate: run plates with positive and negative controls to compute
   Z-factor, assess edge effects, and run on three days for
   inter-assay variability.
5. Design the dose-response experiment with a reference compound,
   replicates, and randomized plate layout.
6. Run it, fit a four-parameter model, and report the potency with
   confidence intervals.
7. Document everything in the notebook with plate maps and raw data
   files linked.
8. Write the assay development report with optimization data,
   validation metrics, the dose-response result, and a standard
   operating procedure for the final assay.

## Extension Ideas
- Miniaturize the assay to a higher-density plate and revalidate.
- Add a counter-screen for cytotoxicity.
- Automate the analysis with a script that reads plate reader files.
- Run a small compound library and hit-pick.

## Skills Demonstrated
- Aseptic cell culture with documentation
- Assay optimization and validation with quality metrics
- Dose-response experimental design and analysis
- Assay reporting and procedure writing

## Industry Relevance

Pharmaceutical Discovery, Biotechnology, Contract Research Organizations, Academic Screening Cores. Assay development and validation are the central skills of research associates and scientists in these sectors, and quality metrics like Z-factor are the shared language. A validated assay with a dose-response result and a procedure is a strong, industry-relevant portfolio piece.
