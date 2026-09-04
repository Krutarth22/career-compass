---
title: "ROS 2 Mobile Robot in Simulation"
track: "robotics-engineer"
difficulty_tier: "beginner"
estimated_hours: 14
role: "core"
skill_tags: ["ros", "robot-simulation", "python", "linux-cli"]
skill_prerequisites: ["python", "linux-cli"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# ROS 2 Mobile Robot in Simulation

## Production Workflow Mirrored
1. Describing a robot with URDF and simulating it with physics
2. Structuring software as nodes, topics, services, and launch files
3. Teleoperating and reading sensors through standard interfaces
4. Recording and replaying data for debugging
5. Testing nodes automatically

## What You'll Build
A differential-drive mobile robot described in URDF with a lidar and a
camera, simulated in Gazebo or Webots, with a ROS 2 package containing
a teleoperation node, an obstacle-stop safety node that uses the lidar,
a launch file that brings up the whole system, recorded bag files of a
run, and unit tests for the safety node's logic.

## Student-Scope Notes
- Ubuntu with ROS 2 in a container or VM is enough; no hardware.
- Use standard message types so the software would work on a real robot
  with the same interfaces.
- The safety node must be tested in simulation with a wall in the path.

## Steps
1. Write the URDF: chassis, wheels with joints, lidar and camera links
   with sensor plugins, and visualize it.
2. Launch the robot in the simulator with a simple world containing
   obstacles and confirm the sensors publish.
3. Write a teleoperation node that publishes velocity commands from
   keyboard input.
4. Write the safety node: subscribe to the lidar, detect obstacles
   within a threshold in the forward arc, and override velocity to stop.
5. Compose a launch file that starts the simulator, the robot, and both
   nodes with parameters.
6. Drive toward a wall and confirm the safety stop; record a bag file
   of the run and replay it to inspect the data.
7. Write unit tests for the safety logic with synthetic scan messages,
   and a launch test that checks the nodes come up.
8. Write the package README with the architecture graph, how to run
   it, and the test results.

## Extension Ideas
- Add odometry from wheel encoders and publish transforms.
- Add a simple wall-following behavior.
- Add a parameter server and dynamic reconfiguration of the threshold.
- Port the package to a real low-cost robot kit.

## Skills Demonstrated
- Robot description and physics simulation
- ROS 2 node, topic, and launch architecture
- Sensor-driven safety behavior
- Data recording and automated testing for robotics software

## Industry Relevance

Warehouse Robotics, Autonomous Vehicles, Agricultural Robotics, Research Labs. ROS 2 is the common language of robotics software in these sectors, and hiring managers expect candidates to structure software as nodes with tests and to be comfortable in simulation before hardware. A simulated robot package with a tested safety node is the standard starting portfolio.
