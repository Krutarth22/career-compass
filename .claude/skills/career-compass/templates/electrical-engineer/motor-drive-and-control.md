---
title: "Motor Drive Hardware and Closed-Loop Control"
track: "electrical-engineer"
difficulty_tier: "advanced"
estimated_hours: 16
role: "core"
skill_tags: ["motor-control", "power-electronics", "control-theory", "microcontrollers", "bench-testing"]
skill_prerequisites: ["circuit-design", "c-cpp"]
project_prerequisites: ["switching-power-supply-design.md"]
prerequisite_learning_hours: 4
---

# Motor Drive Hardware and Closed-Loop Control

## Production Workflow Mirrored
1. Specifying a drive from motor and load requirements
2. Designing the power stage, gate drive, current sensing, and protection
3. Implementing commutation and closed-loop current and speed control
4. Tuning controllers from a plant model and measured response
5. Validating protection and performance on a dynamometer or load

## What You'll Build
A motor drive for a small brushed DC or brushless motor: a
specification, an H-bridge or three-phase inverter stage with gate
drivers, current sensing, and overcurrent protection, a control board
or microcontroller running commutation and a tuned closed-loop speed
(and current, if brushless) controller, and a test report showing step
response, current limiting, protection trips, and efficiency under a
load.

## Student-Scope Notes
- A small motor (tens of watts) with a bench supply keeps the project
  safe; use current limiting and fuses.
- An off-the-shelf gate-driver or integrated driver IC is acceptable;
  design the surrounding circuitry and protection yourself.
- Loading can be a second motor as a generator into a resistor, or a
  friction brake with a torque estimate.

## Steps
1. Write the specification: motor type and ratings, supply, peak and
   continuous current, speed range, control mode, and protection
   requirements.
2. Design the power stage: switches with margin, gate drive with dead
   time, current sense (shunt and amplifier) with bandwidth, and
   hardware overcurrent trip.
3. Build and bring up the power stage open-loop with a current-limited
   supply, verifying switch waveforms and dead time.
4. Implement commutation (PWM for brushed, six-step or field-oriented
   for brushless) and verify rotation and current waveforms.
5. Identify the plant: measure the speed response to a voltage step
   and fit a first-order model with the motor constants.
6. Design and tune the speed controller (and inner current loop if
   applicable) from the model, then refine on hardware; capture step
   responses.
7. Test protection: force an overcurrent and a stall and confirm the
   trip; measure efficiency across load points.
8. Write the report with the specification, hardware design, plant
   identification, controller design, and all test results.

## Extension Ideas
- Implement sensorless commutation from back-EMF.
- Add regenerative braking and manage bus voltage.
- Implement field-oriented control with a position sensor.
- Add a CAN interface for setpoints and telemetry.

## Skills Demonstrated
- Motor drive power stage and protection design
- Commutation and closed-loop control implementation
- Plant identification and controller tuning
- Load testing and protection validation

## Industry Relevance

Electric Vehicles, Robotics, Industrial Automation, Drones. Motor drive design sits at the intersection of power electronics, control, and embedded firmware, and engineers who can deliver a tuned drive with validated protection are sought across these sectors. A drive with step-response and protection test data is a strong portfolio piece for any of them.
