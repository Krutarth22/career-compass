---
title: "Automation Cell Integration Capstone"
track: "controls-engineer"
difficulty_tier: "advanced"
estimated_hours: 28
role: "capstone"
skill_tags: ["plc-programming", "hmi-scada", "industrial-protocols", "functional-safety", "control-theory", "systems-engineering", "technical-documentation"]
skill_prerequisites: ["plc-programming"]
project_prerequisites: ["scada-and-industrial-networking.md", "machine-safety-risk-assessment-and-circuit.md"]
prerequisite_learning_hours: 2
---

# Automation Cell Integration Capstone

## Production Workflow Mirrored
1. Specifying an automation cell from a customer's process requirements
2. Designing controls, networks, safety, and supervisory layers together
3. Building and testing to a factory acceptance test protocol
4. Simulating commissioning, including startup issues and changes
5. Delivering documentation and training for operations and maintenance

## What You'll Build
A complete automation cell (a simulated or bench-scale cell combining a
process sequence, a motion axis or conveyor, safety, and supervision):
a user requirements specification and functional design specification,
electrical drawings, PLC and HMI programs, SCADA integration with
historical data, a safety system, a factory acceptance test protocol
executed with a witness, a change during commissioning handled through
change control, and an operations and maintenance manual with training
delivered.

## Student-Scope Notes
- Reuse and integrate every earlier template; the capstone is the full
  project lifecycle.
- A peer or mentor acts as the customer and witnesses the acceptance
  test.
- The commissioning change should be realistic (a new product variant,
  a sensor relocation) and traced through the documents.

## Steps
1. Write the user requirements specification with the "customer" and
   derive the functional design specification with a traceability
   matrix.
2. Produce the electrical design: panel layout, power distribution, I/O
   wiring, network diagram, and the safety circuit drawings.
3. Implement the PLC program, HMI, motion or conveyor control, and
   SCADA integration to the functional specification.
4. Implement and validate the safety system per your risk assessment.
5. Write the factory acceptance test protocol from the requirements
   with pass criteria for every function, and execute it with the
   witness, recording results and punch-list items.
6. Handle a commissioning change: assess impact, update the
   specification, drawings, program, and tests through change control,
   and retest.
7. Write the operations and maintenance manual: operation, alarms and
   responses, maintenance tasks, spare parts, and troubleshooting.
8. Deliver operator and maintenance training, obtain acceptance
   sign-off, and assemble the project documentation with an index.

## Extension Ideas
- Add a manufacturing execution system interface for orders and results.
- Implement a digital twin for virtual commissioning.
- Add predictive maintenance from drive and sensor data.
- Run a site acceptance test with a second witness.

## Skills Demonstrated
- Requirements-driven automation project delivery
- Integrated controls, safety, network, and supervisory design
- Acceptance testing and change control
- Operations documentation and training

## Industry Relevance

Systems Integrators, Machine Builders, Manufacturing Plants, Pharmaceuticals. Automation projects in these sectors follow this lifecycle with formal specifications and acceptance tests, and integrators hire controls engineers who have run one end to end. A cell delivered to a witnessed acceptance test with change control is the definitive controls portfolio.
