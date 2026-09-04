---
title: "Airfoil and Wing Aerodynamic Design"
track: "aerospace-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["aerodynamics", "python", "cfd-simulation", "technical-documentation"]
skill_prerequisites: ["python"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Airfoil and Wing Aerodynamic Design

## Production Workflow Mirrored
1. Deriving aerodynamic requirements from a mission
2. Selecting and analyzing airfoils with panel methods
3. Designing a wing planform and estimating lift, drag, and stall
4. Checking with a higher-fidelity method
5. Documenting the design trade-offs

## What You'll Build
An aerodynamic design for a small aircraft wing (a UAV or a model
glider you could build): mission-derived requirements (cruise speed,
weight, stall speed), airfoil comparison and selection with XFOIL or a
Python panel code across Reynolds numbers, a wing planform with
lifting-line or vortex-lattice analysis of lift distribution, induced
drag, and stall characteristics, a CFD check of the airfoil at one
condition, and a design report with a drag polar and trade-offs.

## Student-Scope Notes
- XFOIL and open vortex-lattice tools are free; OpenFOAM or a free CFD
  service is enough for the check.
- Design for a low Reynolds number regime appropriate to a small
  aircraft, where airfoil choice matters most.
- The wing should be one you could actually build in a later template.

## Steps
1. Write the mission and derive wing loading, cruise lift coefficient,
   and stall requirements with the standard relations.
2. Compare at least four candidate airfoils across the operating
   Reynolds range for lift-to-drag, maximum lift, and pitching moment;
   select one with justification.
3. Design the planform: span, area, aspect ratio, taper, and twist
   from the requirements and structural considerations.
4. Analyze the wing with a lifting-line or vortex-lattice method for
   the lift distribution, induced drag, and the span efficiency.
5. Estimate the stall behavior from the section and spanwise loading,
   and adjust twist or taper for a benign stall.
6. Run a CFD case for the airfoil at the cruise condition and compare
   with the panel method.
7. Build the aircraft drag polar and the cruise and stall performance
   predictions.
8. Write the design report with requirements, airfoil selection data,
   planform analysis, CFD comparison, and the trade-offs made.

## Extension Ideas
- Add a tail and compute static stability margins.
- Optimize twist for minimum induced drag with a constraint on stall.
- Add high-lift devices and analyze their effect.
- Build the wing and measure lift on a simple rig.

## Skills Demonstrated
- Mission-driven aerodynamic requirements
- Airfoil analysis and selection with panel methods
- Wing planform design and lifting-line analysis
- CFD cross-checking and design reporting

## Industry Relevance

UAV Manufacturers, General Aviation, Aerospace Research, Wind Energy. Aerodynamic design fundamentals are the entry test for aerospace roles in these sectors, and interviewers ask candidates to explain airfoil selection and induced drag. A wing design report with panel and CFD results is the natural first portfolio piece.
