---
title: "FPGA Digital Design with Simulation and Hardware Test"
track: "electrical-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["fpga-hdl", "circuit-design", "bench-testing", "automated-testing"]
skill_prerequisites: []
project_prerequisites: []
prerequisite_learning_hours: 5
---

# FPGA Digital Design with Simulation and Hardware Test

## Production Workflow Mirrored
1. Specifying a digital function with interfaces and timing
2. Writing synthesizable HDL with a clean module hierarchy
3. Verifying with self-checking testbenches before touching hardware
4. Meeting timing constraints and understanding the synthesis report
5. Testing on a board with a logic analyzer

## What You'll Build
A digital design on a low-cost FPGA development board (a UART-controlled
signal generator, a PWM motor controller with encoder feedback, a
simple SPI peripheral, or a video test-pattern generator): a
specification with interface timing, Verilog or VHDL modules,
self-checking testbenches with coverage of every interface, timing
constraints met with a reviewed report, and hardware verification with
a logic analyzer capturing the interfaces.

## Student-Scope Notes
- Any budget FPGA board with a free toolchain (Lattice with open tools,
  Xilinx or Intel free editions) is suitable.
- Simulation first is mandatory; the board is for confirmation, not
  debugging by trial.
- The design should include at least one clock-domain crossing or an
  asynchronous input handled correctly.

## Steps
1. Write the specification: function, interfaces with timing diagrams,
   clock frequency, and resource budget.
2. Design the module hierarchy and the state machines, and document
   them with block diagrams.
3. Write synthesizable HDL with synchronous resets, registered outputs,
   and explicit clock-domain crossing synchronizers where needed.
4. Write self-checking testbenches for every module and a top-level
   testbench that drives the interfaces and checks results
   automatically; run them in a simulator.
5. Synthesize, apply timing constraints, and review the timing and
   utilization reports; fix any violations by design, not by tweaking
   constraints.
6. Program the board and verify each interface with a logic analyzer,
   comparing captures with simulation waveforms.
7. Add a testbench regression script so all tests run with one command.
8. Write the design document with the specification, architecture,
   verification results, timing summary, and hardware captures.

## Extension Ideas
- Add a soft-core processor and move control into firmware.
- Implement a DSP block (a FIR filter) and verify against a model.
- Add formal verification of a state machine property.
- Port the design to a second FPGA family and compare resources.

## Skills Demonstrated
- Digital specification with interface timing
- Synthesizable HDL and clock-domain discipline
- Self-checking verification and regression
- Timing closure and hardware validation

## Industry Relevance

Telecommunications, Defense Electronics, Test Equipment, Data Center Hardware. FPGA design and verification skills are scarce and well paid in these sectors, and hiring loops probe whether candidates verify before synthesizing and understand timing reports. A design with self-checking testbenches, a clean timing report, and analyzer captures demonstrates the full discipline.
