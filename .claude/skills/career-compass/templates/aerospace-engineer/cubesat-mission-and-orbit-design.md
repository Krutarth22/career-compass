---
title: "CubeSat Mission and Orbit Design"
track: "aerospace-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["orbital-mechanics", "systems-engineering", "python", "thermal-analysis", "technical-documentation"]
skill_prerequisites: ["python"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# CubeSat Mission and Orbit Design

## Production Workflow Mirrored
1. Defining mission objectives and deriving requirements
2. Designing and analyzing the orbit for coverage, lifetime, and
   eclipses
3. Budgeting mass, power, link, and data with margins
4. Analyzing subsystem-level constraints such as thermal and attitude
5. Reviewing the concept against the requirements

## What You'll Build
A mission concept for a 3U CubeSat with a defined objective (Earth
observation of a region, a communications relay experiment, a science
payload): a requirements tree, an orbit design analyzed in Python or a
free tool (GMAT) for ground coverage, revisit, eclipse fraction, and
orbital lifetime, mass, power, link, and data budgets with margins, a
thermal first-order analysis, an attitude control concept, a concept
of operations, and a concept review package.

## Student-Scope Notes
- Use GMAT (free) or your own propagator with J2 for the orbit
  analysis, and public component data for the budgets.
- Implement the link budget and power budget yourself in Python.
- The review needs a peer or mentor asking systems-level questions.

## Steps
1. Write the mission objectives and derive top-level requirements with
   a traceable tree.
2. Design the orbit: altitude and inclination trades for coverage and
   revisit of the target, eclipse fraction, and lifetime under drag
   with a stated solar activity assumption.
3. Build the power budget: generation across the orbit with eclipses,
   subsystem consumption by mode, battery sizing, and margins.
4. Build the link budget for the downlink with a chosen ground station,
   and the data budget against the payload's data generation.
5. Build the mass budget with contingency by maturity.
6. Perform a first-order thermal analysis for hot and cold cases and an
   attitude determination and control concept with pointing
   requirements.
7. Write the concept of operations: modes, a typical orbit timeline,
   and contingency responses.
8. Assemble the concept review package and present it, recording
   actions from the reviewer.

## Extension Ideas
- Add a propulsion option and analyze station-keeping or deorbit.
- Model attitude dynamics and a detumbling controller.
- Design the flight software architecture.
- Build a ground station link test with a software-defined radio.

## Skills Demonstrated
- Mission requirements derivation
- Orbit design and analysis for coverage and lifetime
- Spacecraft budgets with margins
- Systems-level concept review

## Industry Relevance

Small Satellite Companies, Space Agencies, Defense Space, University Space Programs. Mission and systems engineering for small satellites is a growing hiring area in these sectors, and concept reviews with budgets are the standard early-phase deliverable. A complete CubeSat concept package with orbit analysis and margins matches those roles directly.
