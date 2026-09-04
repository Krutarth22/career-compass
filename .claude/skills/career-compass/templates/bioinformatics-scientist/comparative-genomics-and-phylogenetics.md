---
title: "Comparative Genomics and Phylogenetic Analysis"
track: "bioinformatics-scientist"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["sequence-analysis", "python", "data-visualization", "reproducible-research"]
skill_prerequisites: ["python", "linux-cli"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Comparative Genomics and Phylogenetic Analysis

## Production Workflow Mirrored
1. Assembling or retrieving genomes and annotating genes
2. Identifying orthologs and building multiple sequence alignments
3. Inferring phylogenies with model selection and support values
4. Detecting selection or gene gain and loss across lineages
5. Reporting with publication-grade trees and tables

## What You'll Build
A comparative analysis of a set of related microbial (or viral)
genomes from public databases: retrieval and annotation, ortholog
identification, a core-gene alignment, a maximum-likelihood phylogeny
with model selection and bootstrap support, a pan-genome or gene
presence-absence analysis, one analysis of selection or a trait
association, and a report with an annotated tree figure and methods
that another analyst could rerun from your scripts.

## Student-Scope Notes
- Bacterial or viral genomes are small enough for a laptop; ten to
  thirty genomes is a good range.
- Use established tools for annotation, orthology, alignment, and tree
  inference; write the glue and the analysis in Python.
- Trees must include support values and be rooted with justification.

## Steps
1. Choose the organism group and a question (an outbreak lineage, a
   trait's distribution, a taxonomic revision), and retrieve genomes
   with accession records.
2. Annotate the genomes consistently and summarize genome statistics.
3. Identify orthologous gene clusters and extract the core genes.
4. Align core genes, concatenate or partition, and run model selection.
5. Infer a maximum-likelihood tree with bootstrap support, root it, and
   visualize with metadata annotations.
6. Analyze the accessory genome: gene presence and absence patterns
   across the tree, and any association with the trait or lineage.
7. Run a selection analysis on a gene of interest, or a
   trait-association test, and interpret carefully.
8. Write the report with methods, the annotated tree, tables, and a
   discussion of limitations; commit the scripts and environment.

## Extension Ideas
- Assemble a genome from raw reads and add it to the analysis.
- Add a dated phylogeny with a molecular clock.
- Add antimicrobial resistance gene detection and mapping onto the tree.
- Build an interactive tree viewer for the results.

## Skills Demonstrated
- Genome annotation and orthology inference
- Multiple sequence alignment and phylogenetic inference
- Pan-genome analysis
- Publication-quality reporting of evolutionary analyses

## Industry Relevance

Public Health Genomics, Infectious Disease Research, Agricultural Biotech, Microbiome Companies. Phylogenetics and comparative genomics underpin outbreak tracking and strain characterization in these sectors, and analysts who can build a defensible tree with proper model selection and support are needed. A comparative genomics report with reproducible scripts is a strong portfolio addition.
