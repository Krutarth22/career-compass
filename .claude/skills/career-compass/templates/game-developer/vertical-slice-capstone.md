---
title: "Vertical Slice Capstone"
track: "game-developer"
difficulty_tier: "advanced"
estimated_hours: 28
role: "capstone"
skill_tags: ["game-engines", "gameplay-programming", "game-ai", "game-design-fundamentals", "performance-profiling", "automated-testing", "technical-documentation"]
skill_prerequisites: ["game-engines", "git-version-control"]
project_prerequisites: ["2d-game-core-loop.md", "enemy-ai-with-behavior-trees.md"]
prerequisite_learning_hours: 4
---

# Vertical Slice Capstone

## Production Workflow Mirrored
1. Defining a slice that proves the game's core promise at shippable
   quality
2. Building systems (player, AI, progression, UI, audio, save) that work
   together
3. Managing scope with a backlog and milestones
4. Profiling and optimizing to a frame-rate target on the minimum spec
5. Delivering a build, a trailer or demo video, and a design document

## What You'll Build
A vertical slice of a game of your own design: ten to twenty minutes of
polished play combining the systems you built in this track (controller,
AI, effects, and optionally multiplayer) with progression, a UI flow,
audio, a save system, and a defined beginning and end, hitting a
frame-rate target on a minimum-spec machine, with automated tests for
the gameplay logic, a public build, a short video, and a design and
technical document set.

## Student-Scope Notes
- Reuse and polish your earlier systems; the capstone is integration,
  content, and finish, not new technology.
- Ten minutes of excellent play beats an hour of rough play. Cut
  ruthlessly and keep a backlog of what you cut.
- Free or purchased assets are fine as long as the code and design are
  yours and credited correctly.

## Steps
1. Write the slice document: the core promise, the player's arc over
   the slice, the systems required, the minimum spec and frame-rate
   target, and a milestone plan with three checkpoints.
2. Build the gray-box version of the whole slice end to end first, with
   placeholder everything, and playtest it before adding polish.
3. Integrate your controller, AI, and effects, and implement
   progression (unlocks, difficulty ramp, or narrative beats) and the
   save and load system.
4. Build the UI flow (title, options with rebinding and audio sliders,
   pause, results) and add audio with a mixer and basic dynamic music
   or ambience.
5. Write automated tests for the gameplay logic that can run without
   rendering (damage math, progression rules, save round-trips) and run
   them in CI.
6. Profile on the minimum-spec target, identify the top three costs, and
   optimize until the frame-rate target holds through the heaviest
   moment.
7. Run three playtest rounds at the milestones with at least five
   testers each, and make the changes their feedback demands.
8. Ship the build publicly, record a two-minute video, and assemble the
   document set: design doc, technical overview with architecture
   diagram, profiling report, playtest findings, and a retrospective.

## Extension Ideas
- Add controller and accessibility options (remapping, subtitles,
  colorblind modes).
- Add localization for a second language.
- Add analytics events and a funnel of where testers stop.
- Submit the slice to a game jam or showcase.

## Skills Demonstrated
- Scoping and delivering a polished vertical slice
- Systems integration: gameplay, AI, UI, audio, save, progression
- Performance optimization to a target on a minimum spec
- Playtesting, documentation, and production discipline

## Industry Relevance

Indie and AA Studios, Publisher Pitching, AAA Gameplay Teams. A vertical slice is the exact artifact studios build to secure funding and the exact artifact hiring managers ask to play, and a finished, profiled, documented slice shows scoping judgment and finish that no collection of prototypes can. It is the definitive game-development portfolio piece.
