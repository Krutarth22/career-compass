---
title: "Kubernetes Deployment, Scaling, and Rollouts"
track: "devops-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["kubernetes", "docker", "networking-fundamentals", "observability"]
skill_prerequisites: ["docker", "linux-cli"]
project_prerequisites: ["containerize-and-compose-a-stack.md"]
prerequisite_learning_hours: 5
---

# Kubernetes Deployment, Scaling, and Rollouts

## Production Workflow Mirrored
1. Translating a compose stack into Deployments, Services, and Ingress
2. Managing configuration and secrets with ConfigMaps and Secrets
3. Setting resource requests and limits and autoscaling on load
4. Rolling out and rolling back versions without downtime
5. Packaging the application for reuse with Helm or Kustomize

## What You'll Build
The stack from `containerize-and-compose-a-stack.md` running on a local
or managed Kubernetes cluster: Deployments with readiness and liveness
probes, Services, an Ingress with TLS, ConfigMaps and Secrets, a
StatefulSet or managed database for persistence, resource requests and
limits, a Horizontal Pod Autoscaler you have watched scale under load, a
rolling update and rollback you have performed, and a Helm chart or
Kustomize overlay for staging and production.

## Student-Scope Notes
- kind, k3d, or minikube locally is fine; a managed cluster's free tier
  is also fine if you set a billing alarm.
- Persistent database on Kubernetes is acceptable here for learning;
  note in the write-up why many teams use a managed database instead.
- Service mesh, GitOps controllers, and multi-cluster are extensions.

## Steps
1. Write Deployment and Service manifests for the app and Redis, with
   readiness and liveness probes, and confirm pods become Ready.
2. Add a StatefulSet with a PersistentVolumeClaim for Postgres (or point
   at a managed database) and confirm data survives pod deletion.
3. Move configuration into a ConfigMap and secrets into a Secret, and
   mount or inject them. Confirm no secret is in the manifests committed
   to git (use sealed secrets, SOPS, or an external secret store).
4. Add an Ingress controller and an Ingress with TLS, and reach the app
   through it.
5. Set resource requests and limits, then add a Horizontal Pod
   Autoscaler on CPU. Generate load and watch replicas scale up and
   back down.
6. Perform a rolling update to a new image tag with maxUnavailable zero
   under load, confirm zero failed requests, then roll back.
7. Package the manifests as a Helm chart or Kustomize base with staging
   and production overlays that differ in replicas, resources, and
   hostnames.
8. Install a metrics stack (kube-prometheus-stack or the platform
   equivalent), build a dashboard of pod CPU, memory, restarts, and
   request rate, and write up the architecture and the rollout
   procedure.

## Extension Ideas
- Add a GitOps controller (Argo CD or Flux) and deploy from git.
- Add network policies restricting pod-to-pod traffic.
- Add a pod disruption budget and drain a node under load.
- Add a canary rollout with a progressive delivery tool.

## Skills Demonstrated
- Kubernetes workload, networking, and configuration primitives
- Probes, resources, and autoscaling in practice
- Zero-downtime rollouts and rollbacks
- Packaging applications with Helm or Kustomize

## Industry Relevance

Cloud-Native SaaS, Fintech, Telecom. Kubernetes is the default platform for these sectors' services, and DevOps and platform roles there expect hands-on fluency with probes, autoscaling, and rollouts rather than conceptual familiarity. A cluster you have scaled and rolled back under load answers that expectation.
