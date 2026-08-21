---
title: "ML Model Lifecycle Capstone"
track: "ml-engineer"
difficulty_tier: "advanced"
estimated_hours: 26
role: "capstone"
skill_tags: ["model-serving", "workflow-orchestration", "ml-monitoring", "mlops-basics", "docker", "data-pipelines"]
skill_prerequisites: ["python", "ml-monitoring"]
project_prerequisites: ["ml-model-serving-api.md", "ml-pipeline-orchestration.md"]
prerequisite_learning_hours: 5
---

# ML Model Lifecycle Capstone

## Production Workflow Mirrored
1. An orchestrated, resumable training pipeline producing a versioned model
   artifact
2. Automatic promotion of that artifact to a served, containerized
   inference API
3. Monitoring and drift-detection wired directly into the serving layer
4. Operational readiness: logging, health checks, basic load handling
5. A portfolio-level write-up connecting pipeline, serving, and monitoring
   into one coherent system story

## What You'll Build
An integrated system where the orchestrated training pipeline you built in
`ml-pipeline-orchestration.md` feeds its output directly into the
containerized, monitored serving API from `ml-model-serving-api.md` — one
system that trains, promotes, serves, and watches a model end to end, not
two side-by-side projects.

## Student-Scope Notes
- This capstone assumes you completed both prerequisite projects; it does
  not re-teach pipeline orchestration or serving/container basics — it's
  about wiring them into one closed loop and closing the monitoring gap
  between "a pipeline produced a model" and "that model is now live."
- Drift detection can be a single reasonable signal (e.g. prediction
  distribution drift or feature-distribution drift over time), not a full
  drift-detection suite — monitoring is a required stage of the system,
  not the entire scope of the project.
- "Promotion" can be a simple rule (new model beats the currently-served
  model on a held-out metric) rather than a full model registry with
  approval gates.

## Steps
1. Take your orchestrated pipeline's final "publish" stage and have it
   write a versioned model artifact to a location the serving API reads
   from.
2. Add a promotion check: the pipeline only promotes the new artifact to
   "current" if it beats the currently-served model on your evaluation
   metric on a held-out set.
3. Update the serving API to load whichever artifact is currently marked
   "current," and confirm a full pipeline run followed by a new request
   picks up the newly promoted model without a manual redeploy.
4. Carry over (or extend) input validation and error handling from the
   serving-API template, now covering "no model promoted yet" and
   "artifact failed to load" cases.
5. Add the required monitoring/drift-detection stage: log per-request
   prediction distributions and implement one drift/degradation signal
   computed over a rolling window of requests, tagged with the model
   version that produced them.
6. Run a basic load test against the combined system; record p50/p95
   latency for both a pipeline run and inference requests.
7. Write a portfolio-level write-up connecting the pieces: architecture
   diagram, what triggers a promotion, what the drift signal would tell
   you if the live model degraded, and what you'd do next for a real
   production version (model registry, canary rollout, automated
   rollback).

## Extension Ideas
- Add the feature-store project (`feature-store-lite.md`) as the pipeline's
  feature source instead of ad hoc feature computation, for readers who
  want to push the system further than the required orchestration +
  serving integration.
- Add a canary or shadow-deployment path that serves a fraction of traffic
  from the newly promoted model before fully cutting over.
- Add automated rollback if the drift signal crosses a threshold.
- Track training cost/compute per pipeline run alongside serving latency.

## Skills Demonstrated
- End-to-end integration of an orchestrated training pipeline with a
  served, containerized inference API
- Model promotion and versioning logic
- Production-shaped monitoring and drift-detection instincts
- Portfolio-level technical communication connecting pipeline, serving,
  and monitoring into one narrative

## Industry Relevance

Fraud Detection, Recommendation Systems, Demand Forecasting. Production ML teams in these sectors need retraining to flow automatically into a served model without manual redeployment, and a live model that silently degrades as real-world data drifts away from training data can cost real money before anyone notices. This capstone's closed loop of training, promotion-on-improvement, containerized serving, and drift monitoring mirrors the full lifecycle an ML engineering team owns once a model is no longer a one-off notebook experiment but a system other parts of the business depend on.
