---
title: "Shaders and Rendering Effects"
track: "game-developer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["graphics-programming", "game-math-physics", "game-engines", "performance-profiling"]
skill_prerequisites: ["game-engines"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# Shaders and Rendering Effects

## Production Workflow Mirrored
1. Writing vertex and fragment shaders by hand rather than only in node
   graphs
2. Implementing lighting models and stylized effects
3. Building post-processing passes
4. Profiling GPU cost and staying within a frame budget
5. Documenting effects so artists can use and tune them

## What You'll Build
A set of hand-written shaders in your engine's shading language (HLSL,
GLSL, or the engine's own): a custom lit surface shader with a
stylized (toon or ramp) lighting model, a vertex-animated effect (wind
on foliage, water surface), a dissolve or hologram effect driven by
noise, a full-screen post-process (outline, color grading, or pixelate),
and a demo scene with a GPU profile showing each effect's cost and a
tuning guide.

## Student-Scope Notes
- Node-based shader editors are allowed for prototyping, but the
  deliverable is written shader code you can explain line by line.
- Physically based rendering theory is not required; a correct
  Lambert or Blinn-Phong plus a stylized ramp is the target.
- Use the engine's frame debugger and GPU profiler; standalone
  capture tools are optional.

## Steps
1. Write a minimal unlit shader from scratch and explain every stage:
   vertex transform, interpolation, fragment output.
2. Implement diffuse and specular lighting in the fragment shader using
   the engine's light data, then add a ramp or step function for a toon
   look.
3. Implement vertex animation: displace vertices with time-based noise
   for wind or waves, and fix normals so lighting stays correct.
4. Implement a dissolve or hologram effect using a noise texture,
   a threshold, and an emissive edge, with parameters exposed to the
   material.
5. Implement a full-screen post-process pass (edge detection from depth
   and normals for outlines, or a color-grading LUT).
6. Build a demo scene showcasing every effect with parameter sliders.
7. Profile the scene: measure the GPU time of each effect with the
   frame debugger, then optimize the most expensive one (fewer texture
   samples, cheaper math, lower precision) and record the change.
8. Write the tuning guide for each effect with screenshots of parameter
   ranges, and the profiling table before and after.

## Extension Ideas
- Add a compute shader for a particle simulation.
- Add a custom render feature or pass in the engine's render pipeline.
- Add shadow handling to the toon shader.
- Port one effect between two engines and note the differences.

## Skills Demonstrated
- Vertex and fragment shader programming
- Lighting models and stylized shading
- Post-processing and render-pipeline integration
- GPU profiling and optimization

## Industry Relevance

AAA and Indie Studios, Real-Time VFX, Architectural Visualization. Technical artists and graphics-leaning gameplay programmers are in short supply across these sectors, and the ability to write and profile shaders by hand separates candidates from those who only assemble node graphs. A demo scene with profiled, documented effects is the standard technical-art portfolio.
