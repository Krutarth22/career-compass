---
title: "Production AI System Capstone"
track: "ai-ml-engineer"
difficulty_tier: "advanced"
estimated_hours: 25
role: "capstone"
skill_tags: ["retrieval-augmented-generation", "model-serving", "ml-monitoring", "mlops-basics", "docker", "api-design"]
skill_prerequisites: ["python", "ml-monitoring"]
project_prerequisites: ["rag-pipeline-with-eval.md", "ml-model-serving-api.md"]
prerequisite_learning_hours: 5
---

# Production AI System Capstone

## Production Workflow Mirrored
1. Combining a generative component (RAG) with a served, containerized
   inference API
2. End-to-end request path: client -> API -> retrieval -> generation ->
   response
3. Monitoring and drift-detection as a required, integrated stage (not an
   afterthought)
4. Operational readiness: logging, health checks, basic load handling
5. Portfolio-level write-up connecting architecture, evaluation, and
   monitoring into one coherent system story

## What You'll Build
An integrated AI system that takes the RAG pipeline you built in
`rag-pipeline-with-eval.md` and deploys it behind the containerized,
monitored serving API from `ml-model-serving-api.md` — one system, not two
side-by-side projects — with a required monitoring/drift-detection stage on
top, and a portfolio write-up walking through the whole thing end-to-end as
you'd present it in an interview or a design doc.

## Student-Scope Notes
- This capstone assumes you completed both prerequisite projects; it does
  not re-teach RAG mechanics or API/container basics — it's about wiring
  them together into one system and closing the observability gap between
  them.
- Drift detection can be a single reasonable signal (e.g. retrieval
  hit-rate drift or answer-length/latency drift over time), not a full
  drift-detection suite — the point is that monitoring is a required stage
  of the system, not the entire scope of the project.
- Load handling is still a basic concurrent-request script, consistent with
  the serving-API template's scope.

## Steps
1. Take your RAG pipeline's retrieval + generation logic and wrap it as the
   model/inference layer behind the serving API's FastAPI structure
   (single service, single request path).
2. Containerize the combined service; confirm it runs end-to-end in Docker
   with a single `docker run`.
3. Carry over (or rebuild, improved) input validation and error handling
   from the serving-API template, now covering RAG-specific failure modes
   (empty retrieval, generation timeout).
4. Add the required monitoring/drift-detection stage: log per-request
   metrics (latency, retrieval hit signal, output length) and implement one
   drift/degradation signal computed over a rolling window of requests.
5. Re-run (or extend) your eval harness against the deployed service, not
   just the offline pipeline, to confirm behavior didn't regress in the
   move to production shape.
6. Run a basic load test against the combined service; record p50/p95
   latency end-to-end (retrieval + generation included).
7. Write a portfolio-level write-up connecting the pieces: architecture
   diagram, eval results, what the drift signal would tell you if the
   system degraded, and what you'd do next for a real production version.

## Extension Ideas
- Swap or augment the RAG pipeline with the agent-tool-use project
  (`llm-agent-tool-use.md`) — wire in tool-calling (e.g. a live lookup tool)
  alongside or instead of pure retrieval, for readers who want to push the
  system further than the required RAG + serving integration.
- Add a shadow-deployment or canary path for testing pipeline changes
  before they hit the primary route.
- Add cost tracking per request (embedding + generation token costs)
  alongside the latency/drift dashboard.
- Add automated rollback if the drift signal crosses a threshold.

## Skills Demonstrated
- End-to-end integration of a generative AI system with a served,
  containerized inference API
- Production-shaped monitoring and drift-detection instincts
- System-level evaluation (post-deployment, not just offline)
- Portfolio-level technical communication connecting architecture,
  evaluation, and monitoring into one narrative
