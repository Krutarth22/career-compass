---
title: "Electronic Product Development Capstone"
track: "electrical-engineer"
difficulty_tier: "advanced"
estimated_hours: 28
role: "capstone"
skill_tags: ["circuit-design", "pcb-layout", "power-electronics", "microcontrollers", "emc-compliance", "design-verification-testing", "bom-and-plm", "technical-documentation"]
skill_prerequisites: ["circuit-design", "c-cpp"]
project_prerequisites: ["pcb-design-fabrication-and-bringup.md", "switching-power-supply-design.md"]
prerequisite_learning_hours: 2
---

# Electronic Product Development Capstone

## Production Workflow Mirrored
1. Defining a product's electrical requirements and architecture
2. Designing power, processing, sensing, and interfaces on one board
3. Considering EMC, safety, and manufacturability from the start
4. Verifying the design against every requirement with a test plan
5. Releasing a production package with BOM, files, and test procedure

## What You'll Build
A complete electronic product of your own definition (a data logger, a
battery-powered sensor hub, a bench instrument, a motor controller with
an interface) integrating a power supply, microcontroller, analog front
end, and interfaces on a custom PCB, with an architecture document, a
design review record, a fabricated and assembled revision, a
verification test report against all requirements, a pre-compliance
EMC check, a production release package, and a portfolio case study.

## Student-Scope Notes
- Reuse the analog, power, and layout work from earlier templates; the
  capstone integrates them into one product with a release package.
- Pre-compliance EMC can be a near-field probe survey and a conducted
  emissions look with a spectrum analyzer or SDR, not a certified test.
- Two board revisions are expected; plan the schedule for it.

## Steps
1. Write the product requirements and the electrical architecture with
   block diagram, power budget, and interface definitions.
2. Design the schematic in blocks, hold a schematic review with a peer,
   and close the actions.
3. Lay out the board with power integrity, analog isolation, and EMC
   practices (return paths, filtering at connectors), and hold a layout
   review.
4. Fabricate, assemble, and bring up revision A with a checklist and
   errata list; write the firmware needed to exercise every function.
5. Write the verification test plan mapping every requirement to a
   measurement, execute it, and record results.
6. Run a pre-compliance EMC survey, identify the worst emitters, and
   plan mitigations for revision B.
7. Design and build revision B with errata and EMC fixes, and rerun the
   verification tests.
8. Assemble the release package (schematics, layout, BOM with sources,
   fabrication files, firmware, test procedure) and write the case study.

## Extension Ideas
- Design an enclosure and validate thermal and EMC effects.
- Build a functional test fixture for production.
- Take the product to a real pre-compliance lab session.
- Run a small batch and analyze yield.

## Skills Demonstrated
- Electrical architecture and requirements definition
- Integrated board design with reviews
- Verification testing and EMC awareness
- Production release documentation

## Industry Relevance

Consumer Electronics, Industrial IoT, Medical Devices, Test Equipment. Hardware teams in these sectors want engineers who have taken a board from requirements through two revisions to a release package, and that is the story hardware interviews are built around. A complete product with verification and EMC evidence is the strongest possible hardware portfolio.
