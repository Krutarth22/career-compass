---
title: "Mass and Energy Balance Flowsheet"
track: "chemical-engineer"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["mass-energy-balances", "process-flow-diagrams", "python", "technical-documentation"]
skill_prerequisites: []
project_prerequisites: []
prerequisite_learning_hours: 0
---

# Mass and Energy Balance Flowsheet

## Production Workflow Mirrored
1. Defining a process basis: feed, product specification, and capacity
2. Drawing the block flow and process flow diagrams
3. Solving mass and energy balances around every unit and the whole plant
4. Building a stream table engineers and simulators share
5. Checking the balance closes and documenting assumptions

## What You'll Build
A complete mass and energy balance for a small real process (ethanol
fermentation and distillation, biodiesel production, a wastewater
neutralization plant, an ammonia synthesis loop): a design basis, a
block flow diagram and a process flow diagram with numbered streams, a
solved balance in a spreadsheet or Python with all assumptions, a
stream table with composition, temperature, pressure, and enthalpy,
and a closure check with a written basis document.

## Student-Scope Notes
- Choose a process with published literature data so property values
  and yields are sourced, not guessed.
- Spreadsheet or Python (with a properties library) is sufficient;
  simulators come in the next template.
- Keep to five to eight unit operations.

## Steps
1. Write the design basis: capacity, feed composition, product
   specification, and operating assumptions, each with a source.
2. Draw the block flow diagram, then the process flow diagram with every
   unit, stream numbers, and major control intent.
3. Set up the degree-of-freedom analysis for the whole flowsheet and
   confirm it is solvable.
4. Solve the mass balance unit by unit, including a recycle loop with
   a purge if the process has one, using iteration where needed.
5. Solve the energy balance: enthalpies from sourced property data,
   heat duties for exchangers, reactors, and columns.
6. Build the stream table and check overall closure for mass and each
   element; document any imbalance and its cause.
7. Run a sensitivity: change conversion or a feed composition and show
   the effect on product rate and utility duties.
8. Write the basis document with the diagrams, assumptions, methods,
   stream table, closure, and sensitivity results.

## Extension Ideas
- Add a utility summary (steam, cooling water, power) and cost it.
- Model a non-ideal separation with an equilibrium stage calculation.
- Build the balance in a simulator and compare.
- Add a preliminary environmental emissions inventory.

## Skills Demonstrated
- Design basis definition and flowsheet drawing
- Degree-of-freedom analysis and balance solving with recycle
- Sourced property data and energy balances
- Stream tables and closure documentation

## Industry Relevance

Chemicals, Food and Beverage Processing, Biofuels, Water Treatment. Every process design in these sectors starts from a closed mass and energy balance, and entry-level process engineers are tested on exactly this ability. A documented flowsheet with a closed balance and a sensitivity is the fundamental process portfolio piece.
