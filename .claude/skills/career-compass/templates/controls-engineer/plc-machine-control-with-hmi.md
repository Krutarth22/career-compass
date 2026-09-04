---
title: "PLC Machine Control with an HMI"
track: "controls-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["plc-programming", "hmi-scada", "electronics-fundamentals", "technical-documentation"]
skill_prerequisites: []
project_prerequisites: []
prerequisite_learning_hours: 4
---

# PLC Machine Control with an HMI

## Production Workflow Mirrored
1. Writing a functional description and sequence of operations for a machine
2. Designing I/O and a control panel layout
3. Programming a PLC with structured, documented logic
4. Building an operator interface with alarms and modes
5. Testing against the sequence with a simulator or a bench rig

## What You'll Build
A PLC program and HMI for a small automated machine (a conveyor sorting
station, a bottle filling sequence, a two-axis pick-and-place with
pneumatics) using a free PLC environment with simulation (CODESYS,
OpenPLC, or a vendor's free edition): a functional description and
sequence of operations, an I/O list and panel layout drawing, ladder or
structured text organized in a state machine with modes (auto, manual,
stop, fault), an HMI with status, controls, and alarms, and a test
record against the sequence.

## Student-Scope Notes
- Simulation is sufficient; a low-cost PLC or an Arduino running OpenPLC
  with switches and LEDs is a good hardware option.
- Use IEC 61131 languages and a state-machine structure; spaghetti
  ladder fails the exercise.
- Alarms must have acknowledgement and a history.

## Steps
1. Write the functional description: the machine, its inputs and
   outputs, the sequence of operations step by step, the modes, and the
   fault conditions.
2. Build the I/O list with tags, types, and wiring designations, and
   draw the panel layout and a wiring diagram for the I/O.
3. Program the state machine in ladder or structured text with a step
   variable, transitions, timers, and interlocks, and comment every
   rung or block.
4. Implement the modes: auto cycle, manual jog of each actuator with
   interlocks, controlled stop, and fault handling with a reset.
5. Build the HMI: a machine overview with animated status, mode
   controls, manual controls with permissions, an alarm banner with
   acknowledge, and an alarm history.
6. Write the test plan from the sequence of operations, covering every
   step, every mode transition, and every fault.
7. Execute the test in simulation or on the rig, record results, fix
   defects, and retest.
8. Write the control documentation: functional description, I/O list,
   program structure, HMI screens, and the test record.

## Extension Ideas
- Add recipe management for different product sizes.
- Add production counters and downtime tracking to the HMI.
- Add a safety circuit with an emergency stop relay and test it.
- Connect the HMI to a historian and trend the counters.

## Skills Demonstrated
- Functional specification and I/O design
- Structured PLC programming with modes and faults
- HMI design with alarms
- Sequence-based testing and documentation

## Industry Relevance

Packaging Machinery, Food and Beverage, Automotive Assembly, Material Handling. PLC and HMI programming to a clear functional specification is the core of controls work in these sectors, and employers ask candidates about program structure and alarm handling. A documented, tested machine program with an HMI is the standard entry portfolio piece.
