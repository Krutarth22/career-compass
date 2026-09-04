---
title: "Device Driver and Hardware Abstraction Layer"
track: "embedded-software-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["device-drivers", "hardware-communication-protocols", "c-cpp", "embedded-testing"]
skill_prerequisites: ["c-cpp", "microcontrollers"]
project_prerequisites: ["sensor-logger-with-serial-output.md"]
prerequisite_learning_hours: 3
---

# Device Driver and Hardware Abstraction Layer

## Production Workflow Mirrored
1. Designing a driver API that hides register details from application code
2. Separating the bus layer from the device layer so drivers are portable
3. Handling errors, timeouts, and device faults explicitly
4. Unit-testing driver logic on the host with a mocked bus
5. Documenting the driver so another engineer can use it without the
   datasheet

## What You'll Build
A portable driver library for two devices (the sensor from the logger
plus a second device such as a display, an EEPROM, or a motor driver)
behind a hardware abstraction layer you design: a bus interface (I2C,
SPI) with implementations for your board and for a host-side mock,
device drivers written only against that interface, explicit error
handling, host-side unit tests with the mock, and on-target integration
tests.

## Student-Scope Notes
- The HAL is your own thin interface, not the vendor's entire HAL; you
  may call the vendor's functions inside your board implementation.
- Host-side tests run on your laptop with a C test framework (Unity,
  CMocka, or Ceedling). This is the core of the exercise.
- Two devices is the floor; the point is that the drivers share nothing
  but the bus interface.

## Steps
1. Design the bus interface: function pointers or a struct of operations
   for transfer, with timeouts and error codes. Write the header first.
2. Implement the bus interface for your board using the vendor SDK, and
   a mock implementation for the host that records transactions and
   replays scripted responses.
3. Rewrite the sensor driver against the bus interface only, with no
   direct hardware calls, and confirm it still works on target.
4. Write the second device driver the same way, including any
   multi-step sequences (initialization, page writes, command and data
   phases).
5. Add explicit error handling: timeouts, NACKs, bad who-am-i,
   out-of-range values, each surfaced as a distinct error code.
6. Write host-side unit tests for both drivers using the mock:
   initialization sequences, correct register writes, conversion math,
   and every error path.
7. Write on-target integration tests that exercise both drivers through
   the real bus and report pass or fail over UART.
8. Document the driver API and write up the layering, the test
   coverage, and how the same drivers would move to a different board.

## Extension Ideas
- Add a DMA-backed bus implementation and confirm the drivers are
  unchanged.
- Add a Linux userspace bus implementation and run the drivers on a
  Raspberry Pi.
- Add coverage measurement for the host tests.
- Package the library with a build system so another project can import
  it.

## Skills Demonstrated
- Driver API and hardware abstraction design
- Bus and device layering for portability
- Host-side unit testing of firmware with mocks
- Explicit error handling in embedded code

## Industry Relevance

Medical Devices, Automotive, Industrial Controls. Driver portability and host-testable firmware are what let teams in these sectors ship across board revisions and satisfy audit requirements, and embedded hiring managers ask directly how you test firmware without hardware. A driver library with mock-based tests answers that in code.
