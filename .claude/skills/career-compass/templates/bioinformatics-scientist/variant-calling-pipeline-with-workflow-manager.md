---
title: "Variant Calling Pipeline with a Workflow Manager"
track: "bioinformatics-scientist"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["bioinformatics-pipelines", "ngs-data-analysis", "docker", "hpc-cluster-computing", "reproducible-research"]
skill_prerequisites: ["linux-cli", "python"]
project_prerequisites: ["rna-seq-differential-expression.md"]
prerequisite_learning_hours: 4
---

# Variant Calling Pipeline with a Workflow Manager

## Production Workflow Mirrored
1. Building a multi-step pipeline as a workflow, not a shell script
2. Containerizing tools so results are reproducible anywhere
3. Running on a cluster or cloud with resource specifications
4. Validating variant calls against a truth set
5. Documenting and testing the pipeline for other users

## What You'll Build
A germline variant calling pipeline in Nextflow or Snakemake for a
public human exome or a small genome dataset: alignment, duplicate
marking, base recalibration, variant calling, filtering, and
annotation, each step in a container, with configuration profiles for
a laptop and a cluster, a test dataset that runs in minutes,
validation against a benchmark truth set with precision and recall,
and documentation with usage, parameters, and outputs.

## Student-Scope Notes
- Use a benchmark sample (Genome in a Bottle) subset to a chromosome
  so the truth set comparison is possible on a laptop.
- Containers with published bioinformatics images are acceptable; you
  write the workflow, not the tools.
- A cluster profile can be tested on a free cloud tier or a university
  cluster if available; otherwise document the profile carefully.

## Steps
1. Define the pipeline steps, inputs, outputs, and parameters, and
   draw the directed acyclic graph.
2. Implement the workflow with one process per step, containerized,
   with channels or rules connecting them and resource requests per
   step.
3. Create a small test dataset and a test profile so the pipeline runs
   end to end in minutes; add it to a continuous integration job.
4. Run on the benchmark subset and produce a filtered, annotated
   variant file.
5. Compare calls with the truth set using a benchmarking tool; report
   precision, recall, and F1 by variant type.
6. Tune filtering and rerun; document the effect on the metrics.
7. Add a cluster or cloud configuration profile and run (or document)
   with appropriate resources and a resume feature.
8. Write the documentation: purpose, quick start, parameters, outputs,
   validation results, and versioning, and tag a release.

## Extension Ideas
- Add joint calling across multiple samples.
- Add a somatic calling mode with tumor-normal pairs.
- Add structural variant calling and evaluate.
- Contribute a module to a community pipeline project.

## Skills Demonstrated
- Workflow-manager pipeline engineering
- Containerized, reproducible bioinformatics
- Cluster and cloud execution configuration
- Benchmark-based validation of variant calls

## Industry Relevance

Clinical Genomics Labs, Pharmaceutical Genomics, Sequencing Service Providers, Biotech. Production bioinformatics in these sectors runs on workflow managers with containers and validation, and bioinformatics engineers are hired specifically to build and maintain such pipelines. A validated, documented pipeline with a test suite matches the job description directly.
