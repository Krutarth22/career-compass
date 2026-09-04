---
title: "Connected Embedded Device Capstone"
track: "embedded-software-engineer"
difficulty_tier: "advanced"
estimated_hours: 26
role: "capstone"
skill_tags: ["rtos", "device-drivers", "low-power-design", "firmware-updates", "embedded-testing", "ci-cd", "technical-documentation"]
skill_prerequisites: ["c-cpp", "microcontrollers", "git-version-control"]
project_prerequisites: ["rtos-multitasking-controller.md", "device-driver-and-hal.md"]
prerequisite_learning_hours: 4
---

# Connected Embedded Device Capstone

## Production Workflow Mirrored
1. Specifying a device's requirements, timing, power, and update needs
2. Architecting firmware as RTOS tasks over a portable driver layer
3. Meeting power and timing budgets with measurements
4. Shipping a field-update path and a manufacturing test mode
5. Continuous integration with host tests and hardware-in-the-loop runs

## What You'll Build
A complete connected device of your own design (an environmental
monitor, a smart plant sensor, a door sensor, a small data logger with a
radio) whose firmware combines the RTOS architecture, the driver
library, low-power operation, and a firmware update path from earlier
templates, plus a manufacturing self-test mode, a CI pipeline running
host-side unit tests and an automated hardware-in-the-loop smoke test,
and a full engineering document set.

## Student-Scope Notes
- Reuse everything from the track. The capstone is integration, the
  self-test mode, and CI with hardware.
- Hardware-in-the-loop CI can be a self-hosted runner attached to your
  board that flashes and reads a UART test report; it does not need to
  be elaborate.
- Choose a product small enough to finish; polish and documentation are
  weighted heavily.

## Steps
1. Write the requirements: function, sampling and latency budgets,
   battery life target, update requirements, and the self-test list.
2. Write the architecture document: task diagram, driver layering, flash
   layout, power state machine, and the interfaces between them.
3. Integrate the RTOS controller and the driver library, and add the
   product's actual sensing and communication behavior.
4. Apply the low-power design and measure against the battery target;
   iterate until met.
5. Integrate the bootloader and update path if you built it, or a
   minimal verified-update path, and perform an update in the field
   configuration.
6. Add a manufacturing self-test mode entered via a pin or command that
   exercises every peripheral and reports pass or fail over UART.
7. Set up CI: host-side unit tests for drivers and logic on every push,
   and a hardware-in-the-loop job that flashes the board, runs the
   self-test, and parses the report.
8. Assemble the document set: requirements, architecture, power report,
   update procedure, test report, and a portfolio README with photos
   and a demo video.

## Extension Ideas
- Add a cloud endpoint that receives the data and shows a dashboard.
- Add a second board variant and prove the drivers port unchanged.
- Add a fault-injection test mode that simulates sensor failures.
- Add a simple enclosure and document the mechanical constraints.

## Skills Demonstrated
- Embedded system architecture from requirements to shipped firmware
- RTOS, drivers, power, and updates integrated in one product
- Manufacturing test and hardware-in-the-loop CI
- Engineering documentation for an embedded product

## Industry Relevance

IoT Product Companies, Medical Devices, Industrial Sensors, Consumer Electronics. Employers in these sectors want embedded engineers who have taken a device through the whole lifecycle, including test modes and update paths that manufacturing and support teams depend on. A finished device with a document set and CI on real hardware is the strongest embedded portfolio a candidate can present.
