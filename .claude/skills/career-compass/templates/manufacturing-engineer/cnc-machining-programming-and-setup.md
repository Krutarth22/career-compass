---
title: "CNC Machining: CAM Programming, Setup, and First Article"
track: "manufacturing-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["cnc-cam", "cad-modeling", "engineering-drawings", "tooling-fixture-design", "statistical-process-control"]
skill_prerequisites: ["cad-modeling"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# CNC Machining: CAM Programming, Setup, and First Article

## Production Workflow Mirrored
1. Planning operations, workholding, and tooling from the drawing
2. Programming toolpaths in CAM with feeds and speeds from data
3. Setting up the machine with offsets and proving out the program
4. Inspecting the first article against the drawing
5. Estimating cycle time and cost and improving them

## What You'll Build
A machined part produced from your own CAM program on a CNC mill or
router (a makerspace, school shop, or a desktop CNC): a process plan
with operations and workholding, a fixture or workholding design, a
CAM program with tool library and feeds and speeds justified from
manufacturer data, a simulated and proven-out program, a first-article
inspection report against every drawing dimension, and a cycle-time
and cost analysis with one implemented improvement.

## Student-Scope Notes
- Access to any CNC machine is required; a desktop router with aluminum
  or plastic is acceptable.
- Free CAM (Fusion 360 personal, FreeCAD Path) is sufficient.
- Safety training on the machine comes first; document it.

## Steps
1. Study the drawing and write the process plan: operations, datums,
   workholding for each, tools, and inspection points.
2. Design the workholding: a vise setup with soft jaws or a simple
   fixture plate, modeled and drawn.
3. Build the CAM program: stock setup, tool library with feeds and
   speeds computed from manufacturer data and machine limits, toolpaths
   per operation, and simulation with collision checking.
4. Post-process and review the G-code for safe starts, tool changes,
   and retracts.
5. Set up the machine: workholding, tool offsets, work offset, and a
   dry run above the part, then run the first part with reduced feed.
6. Inspect the first article against every dimension with appropriate
   instruments, record actuals, and disposition out-of-tolerance
   features with root cause.
7. Measure cycle time per operation and estimate cost with machine and
   labor rates; identify the largest time contributor.
8. Implement one improvement (toolpath strategy, tool change reduction,
   feed optimization), rerun, and report the new cycle time and quality.

## Extension Ideas
- Run a short batch and chart a critical dimension on a control chart.
- Add a second setup with a tombstone or a fourth axis.
- Design a dedicated fixture for a batch of ten.
- Program the same part on a lathe if available.

## Skills Demonstrated
- Process planning and workholding design
- CAM programming with justified cutting parameters
- Machine setup and program prove-out
- First-article inspection and cycle-time improvement

## Industry Relevance

Precision Machining, Aerospace Suppliers, Medical Device Manufacturing, Tooling. Manufacturing engineers in these sectors program, set up, and improve machining processes, and credibility on the shop floor comes from having done it. A part with a CAM program, a first-article report, and a measured improvement is direct proof of that hands-on competence.
