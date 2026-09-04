---
title: "Research Data Analysis and Publication Figure Preparation"
track: "research-scientist-life-sciences"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["r-programming", "python", "data-visualization", "statistics", "scientific-writing", "reproducible-research"]
skill_prerequisites: ["statistics"]
project_prerequisites: ["designed-experiment-with-statistical-analysis.md"]
prerequisite_learning_hours: 3
---

# Research Data Analysis and Publication Figure Preparation

## Production Workflow Mirrored
1. Organizing raw data from instruments into analyzable form
2. Analyzing with reproducible scripts rather than manual spreadsheets
3. Producing figures that meet journal standards
4. Writing figure legends and a results section
5. Preparing data and code for sharing

## What You'll Build
A reproducible analysis and figure package for a body of experimental
data (your own from earlier templates, or a public dataset from a
paper with raw data): a tidy data structure with a data dictionary,
analysis scripts in R or Python producing every statistic, a
multi-panel publication figure with consistent styling, color
accessibility, and individual data points, an image-processing
workflow for a microscopy or blot figure with documented adjustments,
figure legends and a results section, and a data and code archive
ready for a repository.

## Student-Scope Notes
- Manual spreadsheet analysis is not acceptable for the final
  version; scripts must regenerate every number and figure.
- Follow a target journal's figure guidelines and cite them.
- Image adjustments must be documented and applied uniformly.

## Steps
1. Organize the raw data into a tidy structure with a data dictionary
   and provenance for each file.
2. Write the analysis scripts with functions for each analysis and a
   driver that regenerates all outputs.
3. Compute the statistics with appropriate methods, and store results
   in tables the figures read from.
4. Build the multi-panel figure with consistent fonts, sizes, colors
   checked for color-vision accessibility, and individual points with
   summaries.
5. Process the image-based figure with documented, uniform adjustments,
   scale bars, and annotations.
6. Write the figure legends with all necessary detail and the results
   section referencing the figures.
7. Have a peer regenerate the figures from the archive on their
   machine and fix any reproducibility gaps.
8. Package the data, code, and environment for a public repository
   with a README and a license.

## Extension Ideas
- Build a supplementary interactive figure.
- Add an automated report that updates when data are added.
- Prepare the package for a specific journal's submission system.
- Create a graphical abstract.

## Skills Demonstrated
- Tidy data organization with provenance
- Scripted, reproducible analysis
- Publication-quality figure and image preparation
- Results writing and data sharing

## Industry Relevance

Academic Research, Biotechnology, Pharmaceutical Research, Scientific Publishing. Reproducible analysis and clear figures are what get research published and trusted in these sectors, and labs value scientists who can produce them without a data analyst. A regenerable figure package with an archive demonstrates that capability.
