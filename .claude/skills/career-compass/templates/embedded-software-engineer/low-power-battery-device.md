---
title: "Low-Power Battery-Operated Device"
track: "embedded-software-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["low-power-design", "microcontrollers", "electronics-fundamentals", "embedded-debugging"]
skill_prerequisites: ["c-cpp", "microcontrollers"]
project_prerequisites: ["sensor-logger-with-serial-output.md"]
prerequisite_learning_hours: 3
---

# Low-Power Battery-Operated Device

## Production Workflow Mirrored
1. Setting a battery-life target and deriving a power budget
2. Measuring current in every device state with real instrumentation
3. Using sleep modes, wake sources, and peripheral gating
4. Minimizing radio or bus activity and duty-cycling sensors
5. Validating the projected battery life against measurement

## What You'll Build
A battery-powered sensing node built from the sensor logger that wakes
periodically or on an interrupt, samples, transmits (UART, BLE, or LoRa
if you have a radio module), and returns to deep sleep, with measured
current in every state, a power budget spreadsheet, a projected battery
life, and at least a tenfold reduction in average current from your
starting point.

## Student-Scope Notes
- You need a way to measure current: a multimeter for sleep current
  plus a power profiler or a shunt and oscilloscope for active bursts.
  A basic USB power meter is not enough.
- A coin cell or a small LiPo with a protection board is fine; follow
  the board's guidance for safe battery use.
- Radio is optional; UART transmit is acceptable as the "expensive"
  operation.

## Steps
1. Set a battery-life target and write the power budget: capacity,
   target life, and the average current that implies.
2. Measure the baseline: current while the logger runs continuously.
   This is your starting point.
3. Implement the lowest sleep mode the board supports with a real-time
   clock or low-power timer wake, and measure sleep current. Fix
   anything keeping it high (floating pins, peripherals left on, debug
   interfaces).
4. Gate the sensor's power or put it in its own sleep mode between
   samples, and measure the difference.
5. Minimize the active window: batch samples, transmit in bursts, and
   measure the active current profile with the profiler.
6. Add an interrupt wake source (a button or a sensor threshold) and
   confirm the device responds while remaining asleep otherwise.
7. Compute average current from the measured state currents and duty
   cycle, project battery life, and compare against a multi-day run on a
   real battery with voltage logging.
8. Write up the state machine, the current in each state, the before and
   after average, the projected vs. observed life, and the largest wins.

## Extension Ideas
- Add brown-out handling and a graceful low-battery shutdown.
- Add adaptive sampling that slows down when readings are stable.
- Add energy harvesting (a small solar cell) and characterize it.
- Compare two microcontrollers' sleep behavior with the same firmware.

## Skills Demonstrated
- Power budgeting and battery-life projection
- Sleep modes, wake sources, and peripheral power gating
- Current measurement with proper instrumentation
- Duty-cycle optimization validated against real batteries

## Industry Relevance

Wearables, Smart Home, Asset Tracking, Agricultural IoT. Battery life is the headline spec in these sectors, and firmware engineers who can take a design from milliamps to microamps with measurements to prove it are directly responsible for whether the product ships. A before-and-after power report is the artifact that shows you can.
