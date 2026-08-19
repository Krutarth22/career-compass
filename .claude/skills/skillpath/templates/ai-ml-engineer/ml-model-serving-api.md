---
title: "ML Model Serving API with Monitoring"
track: "ai-ml-engineer"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["model-serving", "api-design", "docker", "ml-monitoring", "python", "mlops-basics"]
skill_prerequisites: ["python", "ml-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# ML Model Serving API with Monitoring

## Production Workflow Mirrored
1. Train/select a model
2. Wrap in a versioned inference API
3. Containerize
4. Input validation & error handling
5. Basic monitoring (latency, request volume, prediction drift signal)
6. Simple load test

## What You'll Build
A trained classification or regression model served behind a REST API,
containerized, with request logging and a basic dashboard showing latency and
prediction distribution over time.

## Student-Scope Notes
- Single-instance Docker container, not a Kubernetes deployment.
- Monitoring is logged-metrics + a local dashboard, not a full observability stack.
- Load test is a basic concurrent-request script, not full performance engineering.

## Steps
1. Train or pick a pretrained model with a clear input/output contract.
2. Build a FastAPI (or similar) inference endpoint with input validation.
3. Containerize with Docker; document how to run it.
4. Add request/response logging (timestamp, latency, input summary, output).
5. Build a small dashboard/script reading the logs: latency over time + prediction
   distribution (a drift proxy).
6. Run a basic load test; record p50/p95 latency.
7. Write up: API contract, how you'd know if the model started behaving badly in
   production.

## Extension Ideas
- Add a shadow-deployment pattern.
- Add real drift detection (e.g. population stability index).
- Add model versioning/rollback support to the API.

## Skills Demonstrated
- Model serving and API design for ML systems
- Containerization
- Basic MLOps monitoring instincts
- Load testing fundamentals
