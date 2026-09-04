---
title: "RTOS-Based Multitasking Controller"
track: "embedded-software-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["rtos", "concurrency", "c-cpp", "microcontrollers", "embedded-debugging"]
skill_prerequisites: ["c-cpp", "microcontrollers"]
project_prerequisites: ["sensor-logger-with-serial-output.md"]
prerequisite_learning_hours: 4
---

# RTOS-Based Multitasking Controller

## Production Workflow Mirrored
1. Decomposing firmware into tasks with priorities and timing requirements
2. Sharing data between tasks safely with queues, semaphores, and mutexes
3. Meeting deadlines and proving it with measurements
4. Handling priority inversion, stack sizing, and starvation
5. Debugging concurrency with a debugger and trace hooks

## What You'll Build
Port the sensor logger to FreeRTOS or Zephyr and extend it into a small
controller: a high-priority sampling task, a processing task (filtering
and threshold detection), a communication task streaming over UART, and
a control output (an LED, a PWM fan, a relay) driven by the processed
data, with all inter-task communication through RTOS primitives and a
measured worst-case latency from sample to output.

## Student-Scope Notes
- Same board as the previous template. FreeRTOS via the vendor SDK or
  Zephyr are both fine; pick one and stay with it.
- "Control output" can be as simple as PWM on an LED; the timing
  guarantees are the point, not the actuator.
- Use the RTOS's built-in stack-watermark and runtime-stats features
  rather than external trace tools, unless you have them.

## Steps
1. Write the task design: each task's responsibility, period or
   trigger, priority, stack estimate, and the data flowing between them.
2. Bring up the RTOS with a single blink task and confirm the tick rate
   with the analyzer.
3. Implement the sampling task triggered by the timer interrupt via a
   semaphore or task notification, pushing samples into a queue.
4. Implement the processing task consuming the queue, applying a filter,
   and posting events (threshold crossed) to the control task.
5. Implement the control and communication tasks, protecting any shared
   state with a mutex, and confirm no data races with a deliberate
   stress test.
6. Measure sample-to-output latency by toggling GPIO pins at each stage
   and capturing on the analyzer; record worst case over thousands of
   cycles.
7. Deliberately create a priority-inversion scenario, observe it, then
   fix it with priority inheritance, and tune stack sizes from the
   watermarks.
8. Write up the task diagram, the latency measurements, the CPU
   utilization per task, and what you learned from the inversion
   experiment.

## Extension Ideas
- Add a watchdog fed only when every task checks in.
- Add a low-priority shell task for runtime inspection.
- Add a software timer for a periodic housekeeping job.
- Port the same design between FreeRTOS and Zephyr and compare.

## Skills Demonstrated
- RTOS task decomposition and priority design
- Queues, semaphores, mutexes, and task notifications used correctly
- Latency measurement and deadline verification
- Concurrency debugging on real hardware

## Industry Relevance

Automotive, Medical Devices, Industrial Automation. Products in these sectors run on RTOSes with hard timing requirements, and embedded interviews probe priority inversion, ISR-to-task handoff, and how you prove latency. A controller with measured worst-case latency and a documented inversion fix is precisely the experience those teams ask about.
