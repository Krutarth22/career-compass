---
title: "Platform Delivery Capstone"
track: "devops-engineer"
difficulty_tier: "advanced"
estimated_hours: 26
role: "capstone"
skill_tags: ["infrastructure-as-code", "kubernetes", "ci-cd", "observability", "site-reliability-practices", "secrets-management", "technical-documentation"]
skill_prerequisites: ["linux-cli", "docker", "git-version-control"]
project_prerequisites: ["ci-cd-pipeline-with-environments.md", "kubernetes-deployment-and-scaling.md"]
prerequisite_learning_hours: 5
---

# Platform Delivery Capstone

## Production Workflow Mirrored
1. Provisioning a cluster and its dependencies from code
2. Delivering applications to it through a GitOps or pipeline-driven flow
3. Baking in observability, secrets, and policy so every service gets them
4. Operating it: SLOs, alerts, on-call runbooks, and a game day
5. Documenting the platform so a developer can self-serve a new service

## What You'll Build
A small internal platform: a Kubernetes cluster provisioned by
infrastructure as code, a CI/CD flow that takes a service from
repository to staging to production on that cluster, a golden path (a
template repository or Helm chart) that gives any new service ingress,
TLS, secrets, metrics, logs, and alerts by default, SLOs and dashboards
for the platform itself, and developer documentation proven by
onboarding a second sample service without your help.

## Student-Scope Notes
- A managed cluster's free tier or a local cluster is acceptable; if
  managed, set a billing alarm and destroy it when done.
- Two sample services (one you built earlier, one new) are enough to
  prove the golden path.
- GitOps (Argo CD or Flux) is recommended but a pipeline-driven deploy is
  acceptable if the promotion model is preserved.

## Steps
1. Write the platform design: cluster topology, environments, the
   delivery flow, what the golden path provides, and the SLOs for the
   platform.
2. Provision the cluster, its network, and its registry with
   infrastructure as code, reusing `infrastructure-as-code-environment.md`
   patterns if you built it.
3. Install the platform components: ingress controller with TLS,
   external secrets or sealed secrets, the metrics and log stack, and a
   policy engine with at least two rules (no privileged pods, resource
   limits required).
4. Build the golden path: a service template or chart that includes
   Deployment, Service, Ingress, probes, resources, a ServiceMonitor, and
   default alerts.
5. Wire the delivery flow: build and push on merge, deploy to staging,
   promote to production with an approval, roll back with one command.
6. Onboard your first service through the golden path and confirm it
   gets metrics, logs, TLS, and alerts without extra work.
7. Run a game day: inject two faults (node drain, bad deploy), respond
   with the dashboards and runbooks, and write a postmortem.
8. Write the developer documentation, then have someone else (or you,
   following only the docs) onboard the second service. Fix every gap
   the docs revealed and publish the portfolio README.

## Extension Ideas
- Add multi-tenancy with namespaces, quotas, and RBAC per team.
- Add cost visibility per namespace.
- Add preview environments per pull request.
- Add a backup and restore drill for cluster state.

## Skills Demonstrated
- Cluster and dependency provisioning from code
- End-to-end delivery flow with promotion and rollback
- Golden-path platform engineering with observability and policy defaults
- Operating a platform with SLOs, game days, and self-serve documentation

## Industry Relevance

Cloud-Native SaaS, Fintech, Large Enterprises. Platform engineering teams in these sectors exist to give product developers a paved road to production, and a candidate who has built one end to end, complete with policy, observability, and documentation another person used successfully, matches the job description almost line for line.
