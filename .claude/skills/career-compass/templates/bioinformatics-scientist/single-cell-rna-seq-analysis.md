---
title: "Single-Cell RNA-Seq Analysis and Cell Typing"
track: "bioinformatics-scientist"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["single-cell-analysis", "ngs-data-analysis", "python", "r-programming", "data-visualization", "statistics"]
skill_prerequisites: ["python", "statistics"]
project_prerequisites: ["rna-seq-differential-expression.md"]
prerequisite_learning_hours: 4
---

# Single-Cell RNA-Seq Analysis and Cell Typing

## Production Workflow Mirrored
1. Quality control and filtering of cells and genes
2. Normalization, feature selection, dimensionality reduction, and
   clustering
3. Annotating cell types with markers and references
4. Comparing conditions at the cell-type level
5. Communicating results with interpretable figures

## What You'll Build
An analysis of a public single-cell RNA-seq dataset with at least two
conditions or samples: cell and gene quality control with justified
thresholds, normalization and integration across samples, clustering
with a resolution choice explained, cell type annotation with marker
genes and an automated reference method compared, differential
abundance and per-cell-type differential expression between
conditions, and a report with the figures a biologist expects.

## Student-Scope Notes
- Choose a dataset of moderate size (ten to fifty thousand cells) with
  a paper for comparison.
- Scanpy in Python or Seurat in R; be able to explain each step's
  purpose and parameters.
- Annotation must be justified with markers, not just accepted from a
  tool.

## Steps
1. Load the data and examine per-cell metrics (counts, genes,
   mitochondrial fraction); choose and justify filtering thresholds.
2. Normalize, select highly variable genes, scale, and reduce
   dimensions; inspect for batch effects between samples.
3. Integrate samples if needed and explain the method; cluster and
   choose a resolution using stability or marker coherence.
4. Annotate clusters using canonical markers and an automated
   reference-based method; resolve disagreements and document.
5. Compute cell-type proportions per condition and test differential
   abundance appropriately.
6. Run differential expression within cell types between conditions
   using pseudobulk to respect replicates.
7. Produce the standard figures (UMAP by cluster and condition, marker
   dot plot, proportion bars, top differential genes).
8. Write the report comparing your findings with the paper, discussing
   parameter sensitivity, and commit the code and environment.

## Extension Ideas
- Add trajectory or pseudotime analysis for a differentiating lineage.
- Add cell-cell communication analysis.
- Integrate with a public atlas as a reference.
- Analyze a multimodal dataset (RNA plus protein).

## Skills Demonstrated
- Single-cell quality control and preprocessing decisions
- Clustering and cell type annotation with justification
- Condition comparison respecting experimental design
- Biologist-facing visualization and reporting

## Industry Relevance

Pharmaceutical Discovery, Biotech, Immunology and Oncology Research, Cell Therapy. Single-cell analysis is among the most requested bioinformatics skills in these sectors, and employers look for judgment in quality control and annotation rather than tool familiarity alone. A documented analysis with justified decisions and a paper comparison shows that judgment.
