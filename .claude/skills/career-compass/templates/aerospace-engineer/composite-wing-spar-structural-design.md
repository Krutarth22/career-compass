---
title: "Composite Wing Spar Structural Design and Test"
track: "aerospace-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["aerospace-structures", "fea-simulation", "material-selection", "design-verification-testing", "cad-modeling"]
skill_prerequisites: ["cad-modeling"]
project_prerequisites: ["airfoil-and-wing-aerodynamic-design.md"]
prerequisite_learning_hours: 4
---

# Composite Wing Spar Structural Design and Test

## Production Workflow Mirrored
1. Deriving structural loads from the flight envelope
2. Sizing a primary structure with hand analysis and margins
3. Designing a composite layup and analyzing it
4. Building a test article and loading it to limit and ultimate
5. Correlating test with analysis and documenting margins

## What You'll Build
A wing spar for your aircraft designed to a flight envelope: the V-n
diagram and critical load cases with factors, a spanwise shear and
moment distribution from the lift distribution, a composite (or
wood-and-composite) spar sized by hand with laminate analysis and
margins of safety, a finite element check, a built test article, a
static load test to limit and to failure with deflection and strain
data, and a correlation report.

## Student-Scope Notes
- A small spar (under a meter) from carbon or glass with a foam or
  balsa core is affordable and safe to test with sandbags or a
  whiffletree.
- Classical laminate theory in a spreadsheet or Python is sufficient
  for layup analysis.
- Testing to failure is the point; plan for it safely.

## Steps
1. Construct the V-n diagram from the aircraft's data and identify the
   critical maneuver and gust load cases with load factors.
2. Compute the spanwise shear, bending moment, and torsion from the
   lift distribution at the critical case.
3. Choose the spar concept (I-beam, box, tube) and materials, and size
   the caps and web by hand with allowables and margins of safety.
4. Design the laminate layup and analyze it with classical laminate
   theory for stiffness and first-ply failure; check buckling of the
   web and caps.
5. Model the spar in FEA, apply the distributed load, and compare
   stresses and deflection with the hand analysis.
6. Build the test article with documented process, and instrument it
   with a deflection measurement and, if possible, a strain gauge.
7. Load test to limit load, holding and recording, then to failure;
   record the failure load and mode.
8. Correlate test with analysis, explain differences, and write the
   report with the load derivation, sizing, laminate analysis, FEA,
   test data, and final margins.

## Extension Ideas
- Add a fatigue estimate for a repeated-load spectrum.
- Design the wing skin and rib attachment and test a section.
- Optimize the layup for minimum mass at the required margin.
- Perform a damage tolerance assessment with an induced defect.

## Skills Demonstrated
- Load derivation from a flight envelope
- Primary structure sizing with margins of safety
- Composite laminate analysis and FEA correlation
- Structural testing to failure and reporting

## Industry Relevance

Aircraft Manufacturers, UAV Companies, Space Launch Providers, Composite Suppliers. Structural engineers in these sectors are expected to derive loads, size with margins, and correlate with test, and interviews ask about margins of safety and failure modes. A spar designed, tested to failure, and correlated is a compelling structures portfolio piece.
