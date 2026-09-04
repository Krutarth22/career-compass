---
title: "Machine Safety Risk Assessment and Safety Circuit"
track: "controls-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["functional-safety", "plc-programming", "electronics-fundamentals", "technical-documentation"]
skill_prerequisites: ["plc-programming"]
project_prerequisites: ["plc-machine-control-with-hmi.md"]
prerequisite_learning_hours: 4
---

# Machine Safety Risk Assessment and Safety Circuit

## Production Workflow Mirrored
1. Performing a machine risk assessment to a standard
2. Determining required performance levels for safety functions
3. Designing safety circuits and selecting rated components
4. Validating safety functions with a test procedure
5. Documenting for compliance and for the operator

## What You'll Build
A safety package for your machine: a risk assessment per ISO 12100 with
hazards, risk estimation, and reduction measures, required performance
levels per ISO 13849 for each safety function (emergency stop, guard
interlock, safe stop), a safety circuit design with a safety relay or
safety PLC logic, dual-channel wiring diagrams, a performance level
calculation, a validation test procedure executed in simulation or on
a bench rig, and a safety manual section.

## Student-Scope Notes
- Use the standards' published methodology; free summaries from
  component vendors are acceptable references, cited.
- A safety relay module and a couple of switches on a bench is an
  affordable hardware option; simulation with documented wiring is
  acceptable.
- This is educational; state that it is not a certified assessment.

## Steps
1. Identify hazards for each machine task and mode (setup, operation,
   maintenance) and estimate risk with the standard's parameters.
2. Define the safety functions needed and determine the required
   performance level for each with the risk graph.
3. Design each safety function: sensors, logic, and actuators, with
   category and structure appropriate to the level.
4. Draw the dual-channel wiring diagrams with monitoring and manual
   reset, and select rated components from vendor data.
5. Calculate the achieved performance level from component data and
   confirm it meets the requirement.
6. Write the validation procedure: functional tests for each safety
   function, fault injection (a stuck contact, a broken wire), and
   expected results.
7. Execute the validation on the rig or in simulation, and record the
   results and any redesign.
8. Write the safety documentation: risk assessment, safety function
   specifications, circuit diagrams, calculations, validation record,
   and the operator's safety instructions.

## Extension Ideas
- Implement the logic on a safety PLC and validate it.
- Add a safe-speed or safe-torque-off function for a drive.
- Perform a functional safety assessment to SIL for a process function.
- Design light-curtain muting for a material entry point.

## Skills Demonstrated
- Machine risk assessment methodology
- Performance level determination and safety circuit design
- Rated component selection and safety calculations
- Safety validation and documentation

## Industry Relevance

Machine Builders, Automotive Assembly, Packaging, Robotics Integrators. Machine safety compliance is a legal requirement and a specialization in these sectors, and controls engineers with documented safety design experience are scarcer than those who program PLCs. A risk assessment with a validated safety circuit is a strong differentiator.
