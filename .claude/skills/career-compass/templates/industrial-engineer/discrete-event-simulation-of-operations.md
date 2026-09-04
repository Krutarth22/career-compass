---
title: "Discrete-Event Simulation of an Operation"
track: "industrial-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["discrete-event-simulation", "statistics", "python", "data-visualization", "operations-research"]
skill_prerequisites: ["statistics", "python"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# Discrete-Event Simulation of an Operation

## Production Workflow Mirrored
1. Collecting input data and fitting distributions
2. Building a simulation model of a process with queues and resources
3. Verifying and validating the model against the real system
4. Running experiments with proper replication and statistics
5. Recommending changes with quantified confidence

## What You'll Build
A validated discrete-event simulation of a real operation with queues
(a campus dining line, a clinic check-in, a small warehouse pick
process, your balanced assembly line): input data collected and fitted
to distributions with goodness-of-fit tests, a model in SimPy or a
free simulation tool, verification and validation against measured
throughput and wait times, designed experiments over at least two
alternatives with replications and confidence intervals, and a
recommendation report.

## Student-Scope Notes
- The real system must be observed for input data and validation; a
  purely hypothetical model fails the exercise.
- SimPy in Python is free and sufficient; student editions of commercial
  tools are fine.
- Report confidence intervals, not point estimates.

## Steps
1. Define the system, its boundary, entities, resources, and the
   performance measures, and get permission to observe.
2. Collect input data: arrivals, service times, and routing, and fit
   distributions with goodness-of-fit tests.
3. Build the model with the observed logic, animation or logging for
   verification, and a warm-up period analysis.
4. Verify the model (traces, extreme conditions) and validate it
   against measured throughput and waits with a statistical comparison.
5. Design experiments: at least two alternatives (added resource, new
   routing, priority rule) with replications sized for the precision
   you want.
6. Run the experiments and analyze with confidence intervals and
   paired comparisons.
7. Perform a sensitivity analysis on the most uncertain input.
8. Write the report with data, model, validation, experiments, and a
   recommendation with the expected effect and its uncertainty.

## Extension Ideas
- Optimize a decision variable with an optimizer over the simulation.
- Add a cost model and compare alternatives economically.
- Build an animated dashboard of the simulation for stakeholders.
- Model a second site and compare configurations.

## Skills Demonstrated
- Input modeling and distribution fitting
- Simulation model building, verification, and validation
- Experimental design and statistical analysis of simulation output
- Decision recommendations with quantified uncertainty

## Industry Relevance

Logistics and Warehousing, Healthcare Operations, Manufacturing, Airports and Transit. Simulation is the industrial engineer's tool for testing changes before spending money, and validated models are what operations leaders in these sectors trust. A validated model with statistically sound experiments is a strong differentiator.
