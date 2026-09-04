---
title: "Switching Power Supply Design and Characterization"
track: "electrical-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["power-electronics", "spice-simulation", "pcb-layout", "bench-testing", "thermal-analysis"]
skill_prerequisites: ["circuit-design"]
project_prerequisites: ["analog-circuit-design-and-bench-test.md"]
prerequisite_learning_hours: 4
---

# Switching Power Supply Design and Characterization

## Production Workflow Mirrored
1. Specifying a power supply from load requirements and input range
2. Selecting a topology and controller and designing the power stage
3. Simulating the converter and designing the compensation loop
4. Laying out the power stage with switching-loop discipline
5. Characterizing efficiency, ripple, transient response, and thermal
   performance

## What You'll Build
A DC-DC converter (a buck from a 12 to 24 volt input to a 5 or 3.3 volt
rail at a few amps, or a boost for a battery application): a
specification, a controller and component selection with inductor and
capacitor calculations, a SPICE simulation including a loop stability
check, a PCB layout with a tight switching loop, a built board, and a
characterization report covering efficiency across load, output ripple,
load-step transient, and thermal imaging or thermocouple data.

## Student-Scope Notes
- Use an integrated controller or a controller with external MOSFETs
  from a major vendor; their design tools and reference layouts are
  legitimate resources.
- Keep voltages low and currents moderate; use a current-limited bench
  supply and an electronic load or resistor bank.
- Loop measurement with a network analyzer is optional; a load-step
  transient on the oscilloscope is required.

## Steps
1. Write the specification: input range, output voltage and current,
   ripple limit, efficiency target, transient requirement, and size.
2. Choose the topology and controller, and calculate the inductor,
   input and output capacitors, and switching frequency with ripple and
   current-rating margins.
3. Simulate the converter: steady-state waveforms, ripple, a load step,
   and the control loop's gain and phase margin; adjust compensation.
4. Lay out the board with the switching loop minimized, the feedback
   trace protected, and thermal relief for the power components.
5. Build and bring up with a current-limited supply, checking switch
   node waveforms and verifying regulation.
6. Measure efficiency at ten load points, output ripple with proper
   probing technique, and the load-step response; compare with
   simulation.
7. Measure component temperatures at full load and compare with loss
   estimates.
8. Write the characterization report with the specification, design
   calculations, layout rationale, and all measurements versus
   predictions.

## Extension Ideas
- Measure the loop response with an injection transformer.
- Design a synchronous version and compare efficiency.
- Add input EMI filtering and measure conducted emissions roughly.
- Design a multi-output supply for a full system board.

## Skills Demonstrated
- Power supply specification and topology selection
- Power stage and compensation design with simulation
- Switching-loop-aware PCB layout
- Efficiency, ripple, transient, and thermal characterization

## Industry Relevance

Electric Vehicles, Renewable Energy, Consumer Electronics, Industrial Power. Power electronics is one of the highest-demand electrical specialties in these sectors, and a characterized converter with measured efficiency and transient response is the kind of concrete evidence power teams ask for in interviews.
