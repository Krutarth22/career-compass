---
title: "Real Hardware Integration of a Robot"
track: "robotics-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["ros", "microcontrollers", "motor-control", "control-theory", "embedded-debugging"]
skill_prerequisites: ["ros", "c-cpp"]
project_prerequisites: ["ros2-mobile-robot-simulation.md"]
prerequisite_learning_hours: 4
---

# Real Hardware Integration of a Robot

## Production Workflow Mirrored
1. Bridging high-level software to motor controllers and sensors
2. Implementing low-level control on a microcontroller with real-time
   loops
3. Calibrating odometry and sensor mounts on the physical robot
4. Running the simulation-developed software on hardware and closing gaps
5. Handling safety: emergency stop, watchdogs, and current limits

## What You'll Build
A physical differential-drive robot (a low-cost kit or your own build
with two motors with encoders, a microcontroller, a single-board
computer, and a lidar or depth camera) running your ROS 2 software: a
firmware layer with PID wheel velocity control and a serial or
micro-ROS interface, a hardware interface node, calibrated odometry,
the safety node from simulation working on hardware, an emergency stop
and watchdog, and a comparison of simulated versus real behavior.

## Student-Scope Notes
- Kits under a few hundred dollars are adequate; a cheap 2D lidar is the
  main sensor cost.
- Keep speeds low and test on the bench with wheels off the ground
  before driving.
- The safety node must stop the real robot before a wall, with
  measured stopping distance.

## Steps
1. Assemble the robot and write firmware to read encoders and drive
   motors with a PWM H-bridge; verify direction and counts.
2. Implement a fixed-rate PID velocity loop per wheel on the
   microcontroller, tune it, and log step responses.
3. Implement the serial or micro-ROS interface for velocity commands
   and encoder feedback with a watchdog that stops motors on timeout.
4. Write the hardware interface node that maps ROS velocity commands to
   the firmware and publishes odometry from encoder counts.
5. Calibrate odometry: wheel diameter and track width via straight-line
   and rotation tests; report residual error.
6. Mount and configure the lidar, verify its transform, and run the
   safety node on hardware; measure stopping distance at several speeds.
7. Wire an emergency stop that cuts motor power independently of
   software, and test it.
8. Run the same teleoperation and safety scenarios as in simulation,
   compare behaviors, and write up the gaps and fixes.

## Extension Ideas
- Run SLAM and navigation on the real robot.
- Add an IMU and fuse it with odometry on hardware.
- Add battery monitoring and a low-battery behavior.
- Characterize latency from command to motion.

## Skills Demonstrated
- Firmware-level motor control with real-time loops
- Hardware abstraction between microcontroller and ROS
- Odometry and sensor calibration on physical robots
- Safety mechanisms and sim-to-real gap analysis

## Industry Relevance

Robotics Startups, Industrial Automation, Consumer Robots, Research. The gap between simulation and hardware is where most robotics projects stall, and engineers who have closed it, including safety and calibration, are valued in every one of these sectors. A working physical robot with a sim-to-real comparison is a distinctive portfolio piece.
