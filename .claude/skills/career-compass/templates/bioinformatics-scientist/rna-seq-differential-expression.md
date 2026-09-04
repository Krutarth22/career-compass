---
title: "RNA-Seq Differential Expression Analysis"
track: "bioinformatics-scientist"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["ngs-data-analysis", "r-programming", "statistics", "data-visualization", "linux-cli"]
skill_prerequisites: ["linux-cli"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# RNA-Seq Differential Expression Analysis

## Production Workflow Mirrored
1. Retrieving public sequencing data and its metadata
2. Quality control, trimming, and alignment or quantification
3. Statistical testing for differential expression with proper design
4. Functional enrichment and visualization
5. Reporting methods so a reviewer can reproduce every figure

## What You'll Build
A complete analysis of a public RNA-seq dataset with a clear two-group
(or factorial) design from GEO or SRA: raw read quality control,
quantification with a modern tool, a differential expression analysis
in R with a design matrix and appropriate multiple-testing correction,
diagnostic plots (PCA, MA, volcano, heatmap), functional enrichment,
and a reproducible report generated from code with a methods section
and a reflection on the original paper's findings.

## Student-Scope Notes
- Choose a dataset with published results so you can compare; a small
  study (6 to 12 samples) keeps compute manageable on a laptop.
- Use command-line tools for quality control and quantification and R
  (DESeq2 or edgeR) for statistics; explain the model you fit.
- The report must be generated from code (R Markdown or Quarto).

## Steps
1. Select the dataset, read the paper's design, and download raw reads
   and metadata; document accession numbers and versions.
2. Run quality control on the reads, inspect the reports, and trim
   adapters if warranted; record the read counts at each stage.
3. Quantify expression against a reference transcriptome or align to
   the genome and count; record tool versions and parameters.
4. Import counts into R, build the sample metadata, and explore with
   PCA and sample clustering; identify batch effects or outliers.
5. Fit the differential expression model with the correct design,
   including covariates where justified, and extract results with
   adjusted p-values and effect sizes.
6. Produce MA, volcano, and heatmap plots and a table of top genes;
   sanity-check known markers from the paper.
7. Run functional enrichment on the results and interpret cautiously.
8. Render the report with methods, results, figures, and a comparison
   with the published findings, and commit the code and environment.

## Extension Ideas
- Add a second contrast or an interaction term.
- Compare two quantification tools on the same data.
- Add transcript-level analysis or splicing.
- Package the analysis as a workflow for the next template.

## Skills Demonstrated
- Sequencing data quality control and quantification
- Statistical modeling of count data with design matrices
- Standard visualizations and enrichment analysis
- Reproducible, code-generated reporting

## Industry Relevance

Pharmaceutical R&D, Biotech, Academic Genomics Cores, Diagnostics. Differential expression is the most common request a bioinformatician receives in these sectors, and hiring managers look for correct statistical modeling and reproducible reports rather than one-off scripts. A reproducible analysis of a public dataset with a comparison to the paper is the standard entry portfolio.
