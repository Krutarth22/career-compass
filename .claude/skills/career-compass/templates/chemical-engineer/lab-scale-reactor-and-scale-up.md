---
title: "Lab-Scale Reactor Experiment and Scale-Up Analysis"
track: "chemical-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["reaction-engineering", "thermal-analysis", "statistics", "python", "design-verification-testing"]
skill_prerequisites: ["mass-energy-balances"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Lab-Scale Reactor Experiment and Scale-Up Analysis

## Production Workflow Mirrored
1. Designing an experiment to measure reaction kinetics safely
2. Running it with controlled conditions and instrumented data
3. Fitting a kinetic model and estimating parameters with uncertainty
4. Designing a larger reactor from the kinetics with heat removal
5. Documenting scale-up risks and the pilot plan

## What You'll Build
A kinetic study of a safe, well-characterized reaction (ester
hydrolysis, a clock reaction, hydrogen peroxide decomposition with a
catalyst, sucrose inversion) at bench scale with temperature control
and time-series measurement, a fitted rate law with Arrhenius
parameters and confidence intervals, a reactor design at a hundred-fold
scale (batch, CSTR, or PFR) with heat-removal analysis, and a scale-up
report with risks and a pilot test plan.

## Student-Scope Notes
- Choose a reaction that is safe with household or basic lab
  materials; document hazards and controls. No pressure, no
  hazardous reagents.
- Measurement can be conductivity, pH, colorimetry with a phone, or
  gas evolution volume.
- Python with curve fitting is sufficient for parameter estimation.

## Steps
1. Select the reaction, write the safety assessment, and design the
   experiment: temperatures, concentrations, replicates, and the
   measurement method with calibration.
2. Run the experiments at three temperatures with replicates, logging
   time series and conditions.
3. Fit candidate rate laws to the data, select the best by statistics,
   and estimate the rate constant at each temperature.
4. Fit the Arrhenius relation and report activation energy and
   pre-exponential factor with confidence intervals.
5. Design a reactor at scale for a stated production rate: volume,
   residence time, conversion, and configuration, using the kinetics.
6. Perform the heat balance at scale: heat generation versus removal
   capacity, and identify whether a runaway is possible.
7. Analyze scale-up risks: mixing, heat transfer area to volume, and
   parameter uncertainty propagated into the design.
8. Write the report with the experimental design, data, model fit,
   reactor design, heat analysis, and a pilot test plan.

## Extension Ideas
- Add a mixing study with a tracer and residence time distribution.
- Model the reactor dynamically for startup and a cooling failure.
- Design the reactor's cooling jacket or coil.
- Run a catalyst deactivation study.

## Skills Demonstrated
- Safe experimental design and kinetic measurement
- Rate law fitting and uncertainty quantification
- Reactor design from kinetics with heat removal analysis
- Scale-up risk assessment

## Industry Relevance

Pharmaceuticals, Specialty Chemicals, Biotechnology, Food Processing. Taking chemistry from the bench to production is the defining job of process development engineers in these sectors, and scale-up failures are costly. A kinetic study with a reactor design and a scale-up risk analysis shows the full bench-to-plant reasoning employers want.
