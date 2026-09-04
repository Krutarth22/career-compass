---
title: "PCB Design, Fabrication, and Bring-Up"
track: "electrical-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["pcb-layout", "circuit-design", "microcontrollers", "bench-testing", "bom-and-plm"]
skill_prerequisites: ["circuit-design"]
project_prerequisites: ["analog-circuit-design-and-bench-test.md"]
prerequisite_learning_hours: 3
---

# PCB Design, Fabrication, and Bring-Up

## Production Workflow Mirrored
1. Capturing a schematic with a proper block structure and design rules
2. Selecting parts for availability and cost, and managing the BOM
3. Laying out a board with attention to power, ground, and signal routing
4. Generating fabrication and assembly files and ordering
5. Bringing up the board methodically and documenting every issue

## What You'll Build
A custom PCB integrating your analog signal chain with a microcontroller
and power supply (a sensor node board): a structured schematic with
design-rule checks passing, a BOM with sourced part numbers and
alternates, a two- or four-layer layout following power and ground best
practices, fabrication and assembly outputs, an ordered and assembled
board, a bring-up checklist executed with measurements, and an errata
list feeding a revision.

## Student-Scope Notes
- KiCad is free and sufficient; Altium or Eagle are fine if available.
- Low-cost fabrication services make a two-layer board affordable;
  assembling by hand is acceptable for most parts.
- Expect at least one mistake on revision A. Finding and documenting it
  is part of the exercise.

## Steps
1. Define the board: functions, connectors, power input, microcontroller,
   the analog front end, and the size envelope.
2. Capture the schematic in hierarchical blocks with net names, test
   points, and decoupling per datasheet; run the electrical rules check.
3. Build the BOM with manufacturer part numbers, distributor stock
   checks, and at least one alternate for critical parts.
4. Lay out the board: placement by signal flow, a solid ground plane,
   short power paths, separated analog and digital areas, and design
   rule checks matching the fabricator's capabilities.
5. Generate Gerbers, drill files, pick-and-place, and assembly drawings;
   review them in a Gerber viewer before ordering.
6. Order the board and parts, assemble, and inspect under magnification.
7. Bring up with a checklist: shorts check, power rails at limited
   current, clocks, microcontroller programming, then each function
   with measurements at the test points.
8. Record every issue in an errata list with root cause and the fix for
   revision B, and write the project README with photos, schematic,
   layout images, and bring-up results.

## Extension Ideas
- Design revision B with the errata fixed and order it.
- Add a USB interface and handle its layout requirements.
- Run a thermal check on the regulator under full load.
- Create a test jig with pogo pins for the board.

## Skills Demonstrated
- Schematic capture and BOM management
- PCB layout for power integrity and signal quality
- Fabrication output generation and ordering
- Methodical board bring-up and errata tracking

## Industry Relevance

Consumer Electronics, IoT Hardware, Industrial Controls, Medical Devices. Board design and bring-up is the central skill for hardware engineers in these sectors, and hiring managers ask to see a board you designed and what went wrong on the first revision. A fabricated board with a bring-up log and errata is exactly that evidence.
