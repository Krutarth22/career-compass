---
title: "Sensor Logger with Serial Output"
track: "embedded-software-engineer"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["microcontrollers", "c-cpp", "hardware-communication-protocols", "electronics-fundamentals"]
skill_prerequisites: ["c-cpp"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# Sensor Logger with Serial Output

## Production Workflow Mirrored
1. Reading a datasheet to bring up a peripheral from register-level docs
2. Configuring GPIO, timers, and a serial bus on a microcontroller
3. Sampling a sensor at a fixed rate without blocking
4. Framing and sending data over UART to a host
5. Verifying signals with a logic analyzer, not just trusting the code

## What You'll Build
Firmware in C for a microcontroller development board (STM32, ESP32,
RP2040, or similar) that reads an I2C or SPI sensor (temperature,
accelerometer, pressure) at a fixed rate driven by a hardware timer,
frames the readings with a checksum, streams them over UART, and a small
host-side script that parses and plots them. You will verify the bus
transactions with a logic analyzer.

## Student-Scope Notes
- A development board and a breakout sensor cost little; a cheap USB
  logic analyzer is strongly recommended and is a tool you will use in
  every later template.
- Using the vendor's HAL is fine, but you must read the sensor's
  datasheet and write the register-level driver for it yourself rather
  than using a library.
- Arduino-style frameworks are acceptable for board setup; the sensor
  driver and the timer-driven sampling must be your own code.

## Steps
1. Read the sensor datasheet and write down the register map you need:
   who-am-i, configuration, data registers, and the read sequence.
2. Bring up the board: blink an LED from a hardware timer interrupt at a
   known rate and confirm the frequency with the logic analyzer.
3. Initialize the I2C or SPI peripheral, read the who-am-i register, and
   capture the transaction on the analyzer to confirm addressing and
   timing.
4. Write the sensor driver: configure it, read raw data, and convert to
   physical units per the datasheet's formulas.
5. Sample at the timer rate using a flag or ring buffer set by the ISR
   and consumed in the main loop; never do bus I/O inside the ISR.
6. Frame each sample (start byte, sequence number, payload, checksum)
   and send it over UART with a non-blocking transmit.
7. Write a host script that reads the serial port, validates checksums,
   counts dropped sequence numbers, and plots the data live.
8. Write up the register map, the analyzer captures, the timing budget
   per sample, and the drop rate at increasing sample rates.

## Extension Ideas
- Add a second sensor on the same bus and handle both in the schedule.
- Add a command interface over UART to change the sample rate.
- Use DMA for the UART transmit and measure the CPU time saved.
- Log to an SD card instead of streaming.

## Skills Demonstrated
- Datasheet-driven peripheral driver development
- Timer interrupts and non-blocking main-loop design
- I2C/SPI and UART communication with analyzer verification
- Host-side tooling for embedded data

## Industry Relevance

Industrial IoT, Automotive Sensors, Consumer Wearables. Nearly every embedded product starts with bringing up sensors from a datasheet and streaming data reliably, and hiring managers in these sectors ask candidates to describe exactly that process. Analyzer captures alongside your driver code show you can do it without a library holding your hand.
