---
title: "3D Character Controller and Camera System"
track: "game-developer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["game-math-physics", "gameplay-programming", "game-engines", "csharp"]
skill_prerequisites: ["game-engines"]
project_prerequisites: ["2d-game-core-loop.md"]
prerequisite_learning_hours: 4
---

# 3D Character Controller and Camera System

## Production Workflow Mirrored
1. Building movement on top of the physics or character-controller layer
   with predictable behavior
2. Handling slopes, steps, ground detection, and jumping robustly
3. Designing a third-person camera that avoids clipping and feels stable
4. Driving animation from movement state
5. Tuning with exposed parameters and a test level built for edge cases

## What You'll Build
A third-person 3D character controller in your engine with walk, run,
jump, and optionally dash or crouch; robust ground detection on slopes
and stairs; coyote time and jump buffering; a follow camera with
collision avoidance, smoothing, and look-around; an animation state
machine driven by the controller; and a gray-box test level that
exercises every edge case, plus a tuning document.

## Student-Scope Notes
- Use the engine's character controller or rigidbody, but you write the
  movement logic, ground checks, and camera; do not use an asset-store
  controller.
- Free humanoid animations (Mixamo or the engine's samples) are fine.
- A test level with ramps of several angles, stairs, ledges, narrow
  corridors, and moving platforms is part of the deliverable.

## Steps
1. Write the movement spec: max speeds, acceleration curves, jump
   height and time-to-apex, coyote time, and buffer windows. Derive
   gravity and jump velocity from height and time using the standard
   kinematic formulas.
2. Implement ground detection with a sphere or capsule cast, slope-angle
   limits, and step handling, and build the test level to verify each.
3. Implement horizontal movement relative to the camera with
   acceleration and deceleration, and confirm consistent behavior on
   slopes.
4. Implement jumping with coyote time and input buffering, and variable
   height on early release.
5. Implement the camera: an orbit with damped follow, a collision cast
   that pulls the camera in front of obstacles, and recovery when
   clear.
6. Build the animation state machine (idle, walk, run, jump, fall, land)
   driven by the controller's state and speed, with blend trees for
   locomotion.
7. Add moving platforms and confirm the character inherits platform
   motion correctly.
8. Expose every parameter in the inspector, tune with playtesters, and
   write up the math, the edge cases handled, and the final values.

## Extension Ideas
- Add wall running or ledge grabbing.
- Add a first-person camera mode with a smooth transition.
- Add root-motion animation and compare against code-driven movement.
- Add a replay recorder for reproducing movement bugs.

## Skills Demonstrated
- Vector math and kinematics applied to movement
- Physics queries for ground and collision detection
- Camera system design with collision handling
- Animation state machines driven by gameplay

## Industry Relevance

AAA Action Games, Indie 3D, Simulation and Training. Character controllers and cameras are the most scrutinized systems in 3D games, and gameplay programming interviews at studios in these sectors frequently ask candidates to derive jump physics or explain camera collision. A polished controller with a written tuning document is direct evidence.
