---
title: "Mechanism Design, Build, and Verification Test"
track: "mechanical-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["mechanical-design", "design-verification-testing", "cad-modeling", "rapid-prototyping", "root-cause-problem-solving"]
skill_prerequisites: ["cad-modeling"]
project_prerequisites: ["parametric-cad-assembly-with-drawings.md"]
prerequisite_learning_hours: 2
---

# Mechanism Design, Build, and Verification Test

## Production Workflow Mirrored
1. Writing requirements for a mechanism with measurable targets
2. Synthesizing and analyzing a mechanism (linkage, cam, gear train)
3. Selecting bearings, fasteners, springs, and motors from catalogs
4. Building and running a verification test plan
5. Investigating failures with a root-cause method

## What You'll Build
A working mechanism designed to requirements (a four-bar gripper, a
cam-driven indexer, a spring-return latch, a small gear-driven
actuator): a requirements list with targets, kinematic synthesis and
analysis, component selection with catalog calculations, a built
prototype, a design verification test plan executed with data, and an
8D-style root-cause report on at least one failure or shortfall.

## Student-Scope Notes
- Printed parts plus off-the-shelf bearings, shafts, and springs are
  sufficient; the engineering is in the analysis and the test.
- Requirements must be measurable (force, stroke, cycle count, speed).
- A failure will happen; that is the point of the root-cause step.

## Steps
1. Write the requirements: function, force or torque, stroke or range,
   speed, cycle life target, size envelope, and cost cap.
2. Synthesize the mechanism (graphical or analytical), and analyze
   position, velocity, and force transmission across the range of
   motion.
3. Select bearings, fasteners, springs, and any motor or actuator using
   catalog calculations for load, life, and margin.
4. Model the mechanism, check for interference and singularities, and
   produce the drawings.
5. Build the prototype and write the verification test plan mapping
   each requirement to a test method, instrument, and pass criterion.
6. Run the tests, including a cycle test to a meaningful count, and
   record data against every requirement.
7. Investigate the first failure or shortfall with a root-cause method
   (5 whys, fishbone), implement a corrective action, and retest.
8. Write the design report: requirements, synthesis, analysis,
   selections, test results, root-cause report, and the verified status
   of each requirement.

## Extension Ideas
- Add a motion study with dynamic loads and compare to measured motor
  current.
- Optimize the linkage for transmission angle or force profile.
- Run a longer cycle test and inspect wear.
- Design a second-generation version from the lessons learned.

## Skills Demonstrated
- Requirements-driven mechanism synthesis and analysis
- Catalog-based component selection with margins
- Verification test planning and execution
- Structured root-cause analysis and corrective action

## Industry Relevance

Industrial Automation, Medical Devices, Consumer Appliances, Robotics Hardware. Mechanism design and verification testing are daily work in these sectors, and interviewers ask candidates to describe a mechanism that failed and what they did about it. A mechanism with a test plan, data, and a root-cause report is that story with evidence.
