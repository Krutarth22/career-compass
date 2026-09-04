---
title: "Deploy and Operate a Full-Stack App"
track: "full-stack-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["cloud-deployment", "docker", "ci-cd", "observability", "secrets-management"]
skill_prerequisites: ["linux-cli", "git-version-control"]
project_prerequisites: ["crud-app-end-to-end.md"]
prerequisite_learning_hours: 4
---

# Deploy and Operate a Full-Stack App

## Production Workflow Mirrored
1. Containerizing client and server with production builds
2. Provisioning a database and managing its credentials as secrets
3. Continuous deployment from the main branch with preview environments
4. HTTPS, custom domain, health checks, and zero-downtime restarts
5. Logs, uptime monitoring, error alerts, and backups

## What You'll Build
The app from `crud-app-end-to-end.md` running at a public HTTPS URL on a
cloud host, deployed automatically by CI on every merge, with preview
deployments for pull requests, a managed or containerized database with
backups, secrets injected from the platform rather than the repo, health
checks, structured logs, uptime monitoring, and an error alert that
reaches you.

## Student-Scope Notes
- Use a platform with a free or cheap tier (Fly.io, Render, Railway, a
  single VPS with Docker). Kubernetes is deliberately out of scope; the
  devops track covers it.
- A custom domain is optional but recommended; a platform subdomain with
  HTTPS is acceptable.
- Backups can be a nightly dump to object storage. Test the restore.

## Steps
1. Write production Dockerfiles for the server and a static build for
   the client, with multi-stage builds and non-root users.
2. Provision the database on the platform, put its URL and every other
   secret in the platform's secret store, and confirm the repo contains
   no secrets.
3. Add a health endpoint that checks the database and configure the
   platform to use it for readiness and restarts.
4. Set up CI to run tests, build images, and deploy to production on
   merge to main, with a preview environment per pull request.
5. Enable HTTPS (platform-managed certificates) and, if using a custom
   domain, configure DNS and confirm the redirect from HTTP.
6. Ship structured logs to the platform's log viewer, add uptime
   monitoring from an external checker, and wire an alert (email or
   chat) for downtime and for server errors.
7. Set up nightly database backups and perform a restore into a scratch
   database to prove the backup works.
8. Deploy a change under light load and confirm no failed requests
   during the restart. Write the runbook: deploy, roll back, rotate a
   secret, restore a backup, read logs.

## Extension Ideas
- Add a staging environment with its own database and promote builds
  through it.
- Add a CDN in front of the client assets.
- Add cost monitoring and a budget alert.
- Add database migrations as a deploy step with a rollback plan.

## Skills Demonstrated
- Containerized production builds and cloud deployment
- Continuous deployment with preview environments
- Secrets management, HTTPS, and health checks
- Basic operations: logs, monitoring, alerts, backups, runbooks

## Industry Relevance

Startups, Agencies, Small SaaS Teams. In organizations without a dedicated platform team, the full-stack engineer is the person who deploys and keeps the app up, and a live URL with CI, monitoring, and a tested backup is what convinces those employers you can be trusted with production.
