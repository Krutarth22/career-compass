---
title: "Enemy AI with State Machines and Behavior Trees"
track: "game-developer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["game-ai", "gameplay-programming", "game-engines", "data-structures-algorithms"]
skill_prerequisites: ["game-engines"]
project_prerequisites: ["2d-game-core-loop.md"]
prerequisite_learning_hours: 3
---

# Enemy AI with State Machines and Behavior Trees

## Production Workflow Mirrored
1. Designing enemy behavior that is readable and fair to the player
2. Implementing perception (sight, hearing) with sensible limits
3. Choosing between finite state machines and behavior trees per enemy
4. Pathfinding on a navmesh with dynamic obstacles
5. Debugging AI with visualizations and telemetry

## What You'll Build
Three enemy types for your 2D or 3D game with distinct, readable
behaviors: one driven by a hand-written finite state machine (patrol,
investigate, chase, attack, retreat), one driven by a behavior tree you
implement or configure, and one using group or coordination behavior
(flanking, surrounding, alerting allies), all with perception systems,
navmesh pathfinding, and in-editor debug visualization of state,
perception, and paths.

## Student-Scope Notes
- Implement the state machine yourself; for the behavior tree, either
  write a minimal one (composites, decorators, leaves) or use the
  engine's built-in system and be able to explain how it evaluates.
- Perception can be cone-of-vision raycasts plus a hearing radius; full
  stimulus systems are an extension.
- Use the engine's navmesh; writing A* yourself is an extension.

## Steps
1. Write a behavior description for each enemy from the player's point
   of view: what it does, how the player can tell, and how the player
   can beat it.
2. Implement perception: a vision cone with line-of-sight raycasts, a
   hearing radius reacting to player noise events, and memory of the
   last known position.
3. Implement the finite-state-machine enemy with explicit transitions
   and a debug label showing the current state above its head.
4. Implement or configure the behavior-tree enemy with at least one
   selector, one sequence, a decorator (cooldown or condition), and
   leaves for movement and attack.
5. Implement the coordinating enemy: when one sees the player it alerts
   nearby allies, and they take distinct positions around the player
   using navmesh queries.
6. Add debug visualization: vision cones, paths, target positions, and
   a toggle to slow time while watching decisions.
7. Playtest for fairness and readability, and tune perception ranges,
   reaction delays, and attack telegraphs so players can learn the
   enemies.
8. Write up the three architectures, when you would choose each, the
   perception model, and the tuning outcomes.

## Extension Ideas
- Add a utility-based AI for one enemy and compare.
- Add dynamic navmesh obstacles the player can create.
- Add an AI director that adjusts spawn intensity from player stress.
- Implement A* yourself on a grid and compare against the navmesh.

## Skills Demonstrated
- State machines and behavior trees implemented and compared
- Perception systems and memory
- Navmesh pathfinding and group coordination
- AI debugging tools and tuning for player experience

## Industry Relevance

Action and Stealth Games, Strategy, Simulation. AI programmers are a distinct hiring track at studios in these sectors, and even generalist gameplay roles expect fluency with state machines and behavior trees. Enemies that are readable, fair, and debuggable, with a written comparison of the architectures, are the portfolio these teams want.
