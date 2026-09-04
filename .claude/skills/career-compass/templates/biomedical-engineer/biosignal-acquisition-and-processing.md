---
title: "Biosignal Acquisition and Processing"
track: "biomedical-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["biosignal-processing", "circuit-design", "microcontrollers", "python", "bench-testing"]
skill_prerequisites: ["python"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# Biosignal Acquisition and Processing

## Production Workflow Mirrored
1. Designing a safe front end for a physiological signal
2. Sampling and transmitting the signal to a computer
3. Filtering, detecting features, and computing physiological metrics
4. Validating against a reference or public database
5. Documenting safety considerations for a body-connected device

## What You'll Build
A biosignal system for ECG or EMG (or PPG using an optical sensor): a
front end using an instrumentation amplifier or an integrated
analog front end with patient safety measures (battery power,
isolation from mains, current limiting), a microcontroller sampling
and streaming the signal, Python processing with filtering, beat or
burst detection, heart rate or activation metrics, validation of the
detection algorithm on a public annotated database, and a safety and
performance report.

## Student-Scope Notes
- Battery power only, never mains-connected electronics on the body;
  document the safety measures.
- Integrated front-end breakout boards are acceptable; understand and
  document the circuit.
- Validate the algorithm on a public database (PhysioNet) with
  sensitivity and positive predictivity.

## Steps
1. Write the requirements: signal, bandwidth, sampling rate, gain,
   noise, and safety constraints.
2. Build the front end with electrode connections, common-mode
   rejection, and safety measures, and verify with a signal generator.
3. Sample on the microcontroller at the required rate and stream to
   the computer with a framing protocol.
4. Record your own signal safely and inspect noise sources (mains
   interference, motion).
5. Implement filtering (baseline removal, notch, bandpass) and compare
   spectra before and after.
6. Implement feature detection (QRS detection or EMG burst detection)
   and compute the physiological metric.
7. Validate the detection algorithm on the public annotated database
   and report performance.
8. Write the report with the design, safety analysis, signal quality,
   algorithm validation, and limitations.

## Extension Ideas
- Add wireless transmission and a mobile display.
- Implement heart rate variability analysis.
- Add multi-channel EMG for gesture recognition.
- Compare two detection algorithms on the database.

## Skills Demonstrated
- Physiological front-end design with safety considerations
- Embedded acquisition and streaming
- Signal processing and feature detection
- Algorithm validation on annotated data

## Industry Relevance

Medical Device Companies, Wearable Health Technology, Rehabilitation Engineering, Clinical Research Tools. Biosignal acquisition and processing is a core biomedical engineering skill in these sectors, and safety awareness for body-connected devices is a hiring filter. A validated system with a safety analysis is a strong first portfolio piece.
