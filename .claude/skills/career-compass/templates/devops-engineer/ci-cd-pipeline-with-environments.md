---
title: "CI/CD Pipeline with Staging and Production"
track: "devops-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["ci-cd", "docker", "cloud-deployment", "secrets-management", "shell-scripting"]
skill_prerequisites: ["linux-cli", "git-version-control"]
project_prerequisites: ["containerize-and-compose-a-stack.md"]
prerequisite_learning_hours: 3
---

# CI/CD Pipeline with Staging and Production

## Production Workflow Mirrored
1. Building and testing every commit and blocking bad merges
2. Building versioned, immutable artifacts (container images) once
3. Promoting the same artifact through staging to production
4. Deploying with rollback, approvals, and a deployment record
5. Injecting secrets per environment without exposing them

## What You'll Build
A pipeline in GitHub Actions (or GitLab CI) for the stack from
`containerize-and-compose-a-stack.md`: pull requests run lint, tests, and
an image build; merges to main push a tagged image to a registry and
deploy it to a staging host; a manual approval promotes the identical
image to a production host; every deploy is recorded; and rollback to any
previous image is one command.

## Student-Scope Notes
- Staging and production can be two small VMs or two apps on a container
  platform's free tier. They must be separate environments with separate
  secrets.
- Deployment can be SSH plus docker compose pull and up, or the
  platform's deploy API. Simplicity is fine; the promotion model is the
  point.
- Approvals use the CI system's environment protection rules.

## Steps
1. Write the pull-request workflow: checkout, cache dependencies, lint,
   run tests with a database service container, build the image but do
   not push. Make it a required check.
2. Write the main-branch workflow: build the image once, tag it with the
   git SHA and a semantic version, push to a registry, and record the
   digest.
3. Provision staging and production hosts with Docker, and store each
   environment's secrets and host credentials in CI environment secrets.
4. Deploy to staging automatically after the push, using the digest, and
   run a smoke test against the staging URL.
5. Add a production job gated by a manual approval that deploys the
   same digest, never a rebuild.
6. Implement rollback: a workflow input that deploys any previous digest
   from the registry. Rehearse it.
7. Add a deployment record (a release, a changelog entry, or a
   deployment event) with who deployed what when.
8. Break something on a branch and confirm the PR check blocks it; then
   write up the pipeline diagram, the promotion model, and the rollback
   procedure.

## Extension Ideas
- Add image signing and verification before deploy.
- Add a canary step that shifts a fraction of traffic first.
- Add database migrations as a gated pre-deploy step.
- Add pipeline metrics: lead time, deploy frequency, failure rate.

## Skills Demonstrated
- CI workflow design with required checks
- Immutable artifact promotion across environments
- Gated deployments, rollback, and deployment records
- Per-environment secrets handling

## Industry Relevance

SaaS, Fintech, E-commerce. Delivery performance is a measured business metric in these sectors, and DevOps interviews routinely ask how you would promote a build safely through environments and roll it back. A working pipeline with a rehearsed rollback is direct proof.
