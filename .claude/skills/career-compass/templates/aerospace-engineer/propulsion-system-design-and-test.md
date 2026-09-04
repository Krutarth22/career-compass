---
title: "Propulsion System Selection, Analysis, and Static Test"
track: "aerospace-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["propulsion", "thermal-analysis", "bench-testing", "python", "design-verification-testing"]
skill_prerequisites: ["python"]
project_prerequisites: ["airfoil-and-wing-aerodynamic-design.md"]
prerequisite_learning_hours: 4
---

# Propulsion System Selection, Analysis, and Static Test

## Production Workflow Mirrored
1. Matching a propulsion system to an aircraft's thrust and power needs
2. Analyzing propeller and motor performance across the envelope
3. Designing the electrical and thermal integration
4. Static testing on an instrumented stand
5. Correlating predictions with measurements

## What You'll Build
An electric propulsion system for your aircraft: thrust and power
requirements from the drag polar across the mission, a propeller
analysis with blade-element momentum theory in Python, motor and
battery selection from manufacturer data with efficiency maps, a
thermal and electrical integration analysis, an instrumented static
thrust stand (load cell, current, voltage, RPM, temperature), test
data across throttle settings and at least two propellers, and a
correlation report.

## Student-Scope Notes
- A hobby-scale motor, ESC, and propeller are affordable; build the
  thrust stand with a kitchen scale or a load cell and a
  microcontroller.
- Safety around spinning propellers is paramount: guards, distance,
  and no loose items.
- Blade-element momentum theory implemented yourself is required; a
  library may be used to check.

## Steps
1. Compute thrust and power required across the mission from the drag
   polar and the aircraft's weight, including climb.
2. Implement blade-element momentum theory and analyze candidate
   propellers for thrust, torque, and efficiency versus airspeed and
   RPM, using published airfoil data for the blade sections.
3. Select the motor and battery: match the propeller's torque and RPM
   to the motor's curves, and size the battery for the mission energy
   with margin.
4. Analyze the electrical integration (currents, wire gauge, connector
   ratings) and the thermal loads on the motor and ESC.
5. Build the instrumented static thrust stand and calibrate the load
   cell.
6. Run static tests across throttle for at least two propellers,
   logging thrust, current, voltage, RPM, and temperatures.
7. Compare measured static thrust and power with the blade-element
   predictions, and derive the system efficiency map.
8. Write the report with requirements, propeller analysis, selection,
   integration, test setup, data, and correlation.

## Extension Ideas
- Add a wind tunnel or car-mounted test for forward-flight thrust.
- Analyze a ducted fan or a contra-rotating pair.
- Model the battery's voltage sag and its effect on endurance.
- Compare an internal combustion option quantitatively.

## Skills Demonstrated
- Propulsion requirements from aircraft performance
- Blade-element propeller analysis
- Motor, battery, and integration selection with data
- Instrumented static testing and correlation

## Industry Relevance

UAV and Drone Companies, Electric Aviation Startups, Propulsion Suppliers, Aerospace Research. Electric propulsion integration is a growing specialty in these sectors, and engineers who can analyze a propeller from first principles and validate on a test stand are valued. A correlated propulsion report with test data is a distinctive portfolio piece.
