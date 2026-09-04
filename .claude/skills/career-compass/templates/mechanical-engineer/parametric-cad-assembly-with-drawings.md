---
title: "Parametric CAD Assembly with Production Drawings"
track: "mechanical-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["cad-modeling", "engineering-drawings", "mechanical-design", "bom-and-plm"]
skill_prerequisites: []
project_prerequisites: []
prerequisite_learning_hours: 0
---

# Parametric CAD Assembly with Production Drawings

## Production Workflow Mirrored
1. Modeling parts with design intent so changes propagate cleanly
2. Building assemblies with correct mates and motion
3. Producing drawings with GD&T that a machine shop can quote from
4. Managing a bill of materials and revisions
5. Running a design review and incorporating changes

## What You'll Build
A parametric CAD model of a real multi-part mechanism (a bench vise, a
camera gimbal, a bicycle stem and clamp, a small gearbox) with at least
eight custom parts and standard hardware, a fully constrained assembly
with motion, a complete drawing package with GD&T and tolerances, a
structured bill of materials, and a documented engineering change after
a peer design review.

## Student-Scope Notes
- Any parametric CAD with a free tier works (Onshape, Fusion 360,
  FreeCAD, or student SolidWorks).
- The mechanism should exist physically so you can measure it, or be
  something you intend to build in a later template.
- Drawings must follow a standard (ASME Y14.5 or ISO GPS) and be
  checked by someone who reads drawings.

## Steps
1. Choose the mechanism, sketch the function and the parts, and write a
   short design intent note: what drives what dimension, and what may
   change later.
2. Model each part parametrically with named dimensions and equations
   for driven features, and test that intended changes propagate without
   breaking geometry.
3. Build the assembly with proper mates so the mechanism moves as
   intended; check for interference through the range of motion.
4. Add standard hardware from a library and confirm thread engagement
   and clearances.
5. Create part drawings with datums, geometric tolerances on functional
   features, surface finishes, and material callouts, plus an assembly
   drawing with a balloon-numbered BOM.
6. Run a tolerance stack-up on one critical fit (a bearing seat, a
   sliding clearance) and set tolerances from it.
7. Hold a design review with a peer or mentor who reads drawings, log
   every comment, and implement changes as a revision with an
   engineering change note.
8. Export a manufacturing package (drawings as PDF, STEP files, BOM) and
   write a README with renders, the design intent, and the change log.

## Extension Ideas
- Request a real quote from a machine shop and revise for cost.
- Add a motion study with loads and check for binding.
- Configure the model with size variants driven by a table.
- Add a sheet-metal part with flat-pattern drawing.

## Skills Demonstrated
- Parametric modeling with design intent
- Assembly constraints and motion checking
- Drawing standards, GD&T, and tolerance stack-up
- BOM structure and engineering change control

## Industry Relevance

Consumer Products, Industrial Equipment, Automotive Suppliers. Mechanical engineers in these sectors spend much of their time producing drawing packages that suppliers can build from, and hiring managers ask to see drawings, not just renders. A reviewed drawing package with GD&T and a change history shows you can do the part of the job that renders hide.
