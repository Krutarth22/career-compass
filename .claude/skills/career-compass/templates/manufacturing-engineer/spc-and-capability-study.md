---
title: "SPC Implementation and Process Capability Study"
track: "manufacturing-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["statistical-process-control", "statistics", "python", "data-visualization", "root-cause-problem-solving"]
skill_prerequisites: ["statistics"]
project_prerequisites: ["process-documentation-pfmea-and-control-plan.md"]
prerequisite_learning_hours: 3
---

# SPC Implementation and Process Capability Study

## Production Workflow Mirrored
1. Selecting characteristics and gauges for statistical control
2. Validating the measurement system before trusting the data
3. Running control charts and reacting to signals
4. Computing capability and comparing to customer requirements
5. Driving improvement from the data

## What You'll Build
A statistical process control implementation on a process you run
repeatedly (machining, 3D printing, a manual assembly step, a coffee
or baking process if that is what you have): a gauge repeatability and
reproducibility study, at least fifty subgrouped measurements on a
characteristic, control charts with rules applied and out-of-control
investigations, a capability study with indices and a sampling-based
confidence statement, a root-cause investigation into the largest
variation source, and a capability improvement with before-and-after
data.

## Student-Scope Notes
- The process must be real and repeated; the characteristic must be
  measurable with a gauge you can study.
- Python or a spreadsheet is enough for the charts; commercial SPC
  software is not required.
- Fifty measurements in subgroups of five is the floor.

## Steps
1. Select the characteristic from the control plan and the gauge, and
   run a gauge repeatability and reproducibility study with two or
   three operators; report the result and whether the gauge is
   acceptable.
2. Collect at least fifty measurements in rational subgroups over time,
   logging conditions (operator, material lot, time).
3. Build X-bar and R (or individuals and moving range) charts, apply
   the standard run rules, and investigate every signal with a note.
4. Assess normality and compute capability indices with confidence
   intervals; compare to a stated specification and requirement.
5. Stratify the data by the logged conditions to find the largest
   variation source, and run a root-cause investigation on it.
6. Implement a process change addressing the cause and collect a
   second data set under the new condition.
7. Recompute the charts and capability and compare before and after
   with a statistical test.
8. Write the study report: gauge study, charts, capability, root cause,
   the change, and the improvement, with a recommended ongoing control.

## Extension Ideas
- Add a designed experiment on two process factors.
- Implement attribute charts for a defect count.
- Build a live SPC dashboard from a data logger.
- Perform a measurement uncertainty budget for the gauge.

## Skills Demonstrated
- Measurement system analysis
- Control charting and signal interpretation
- Capability analysis with statistical rigor
- Data-driven root cause and improvement

## Industry Relevance

Automotive Suppliers, Electronics Manufacturing, Pharmaceuticals, Aerospace. Capability indices are contractual requirements in these sectors, and manufacturing and quality engineers are expected to run gauge studies and read charts correctly. A study with a measurement analysis and a proven improvement demonstrates the statistical side of the role.
