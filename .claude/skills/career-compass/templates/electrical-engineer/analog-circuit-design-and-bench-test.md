---
title: "Analog Circuit Design, Simulation, and Bench Test"
track: "electrical-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["circuit-design", "spice-simulation", "bench-testing", "electronics-fundamentals"]
skill_prerequisites: []
project_prerequisites: []
prerequisite_learning_hours: 0
---

# Analog Circuit Design, Simulation, and Bench Test

## Production Workflow Mirrored
1. Deriving circuit requirements from a system need
2. Designing with hand analysis and component selection from datasheets
3. Simulating in SPICE and checking against hand analysis
4. Building and measuring on the bench with proper instruments
5. Documenting design, simulation, and measurement together

## What You'll Build
An analog signal chain for a real sensor (a strain gauge bridge, a
photodiode, a microphone, a thermistor): requirements for gain,
bandwidth, noise, and supply, a hand-analyzed design using op-amps and
passives selected from datasheets, an LTspice simulation with
frequency response and noise analysis, a breadboard or perfboard build,
bench measurements with an oscilloscope and function generator, and a
design report correlating all three.

## Student-Scope Notes
- A basic bench (a budget oscilloscope, a multimeter, a function
  generator or a signal from a microcontroller DAC) is enough.
- Breadboards are acceptable for audio-band circuits; note their
  parasitic limitations.
- The sensor should be real and the signal measured, not simulated only.

## Steps
1. Write the requirements: sensor output range, required gain, bandwidth,
   noise floor, supply rails, and output range for the ADC or next stage.
2. Design the signal chain by hand: topology choice, gain equations,
   filter corners, and op-amp selection from datasheet parameters
   (bandwidth, noise, input bias, rail-to-rail).
3. Simulate in SPICE: DC operating point, AC frequency response,
   transient with a realistic input, and noise analysis; compare with
   hand analysis.
4. Build the circuit, with attention to decoupling and grounding, and
   power it up with current limiting.
5. Measure gain and frequency response with the function generator and
   oscilloscope, and measure output noise.
6. Connect the real sensor and capture its signal; compare amplitude
   and noise with predictions.
7. Investigate at least one discrepancy (oscillation, offset, noise
   pickup) to root cause and fix it.
8. Write the design report with schematic, hand analysis, simulation
   plots, bench plots, correlation table, and lessons.

## Extension Ideas
- Add an anti-aliasing filter and feed an ADC; verify with an FFT.
- Design an instrumentation amplifier version and compare CMRR.
- Characterize temperature drift with a hot-air source.
- Add a precision reference and calibrate the chain.

## Skills Demonstrated
- Requirements-driven analog design with hand analysis
- Datasheet-based component selection
- SPICE simulation and correlation
- Bench measurement technique and debugging

## Industry Relevance

Medical Devices, Industrial Sensors, Audio Equipment, Test and Measurement. Analog signal chain design is a core competence in these sectors and one many graduates lack, and interviewers ask candidates to design and debug an amplifier stage on the spot. A report showing hand analysis, simulation, and bench correlation proves you can.
