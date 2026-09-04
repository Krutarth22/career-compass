---
title: "Containerize and Compose a Multi-Service Stack"
track: "devops-engineer"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["docker", "linux-cli", "networking-fundamentals", "shell-scripting"]
skill_prerequisites: ["linux-cli", "git-version-control"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# Containerize and Compose a Multi-Service Stack

## Production Workflow Mirrored
1. Writing production-grade Dockerfiles with small, secure images
2. Composing an application, database, cache, and reverse proxy on one host
3. Wiring service discovery, networks, volumes, and health checks
4. Managing configuration and secrets outside the image
5. Scripting the build, start, stop, and reset lifecycle

## What You'll Build
A docker-compose stack for a sample web application (any open-source app
with a database dependency, or one of your own) consisting of the app, a
Postgres database, Redis, and an nginx reverse proxy with TLS, with
multi-stage Dockerfiles, non-root users, health checks, named volumes
for persistence, an isolated network, environment-based configuration,
and shell scripts for the full lifecycle.

## Student-Scope Notes
- One host, one compose file. Orchestration across hosts is the
  Kubernetes template.
- TLS uses a self-signed certificate or mkcert locally. Public
  certificates come with the deployment template.
- Image size and security matter: compare your final image to a naive
  one and explain the difference.

## Steps
1. Write a multi-stage Dockerfile for the app: build stage, minimal
   runtime stage, non-root user, pinned base image, and a `.dockerignore`.
   Record the image size vs. a single-stage build.
2. Add Postgres and Redis services with named volumes, and confirm data
   survives `docker compose down` and `up`.
3. Add health checks to every service and make the app wait for the
   database to be healthy before starting.
4. Add nginx as a reverse proxy terminating TLS and forwarding to the
   app, with the app no longer publishing its port to the host.
5. Move all configuration to environment variables with an `.env.example`
   and confirm no secret is baked into any image.
6. Put the services on a dedicated network and prove from inside a
   container that only the intended ports are reachable.
7. Write scripts for build, up, down, logs, and a full reset that
   removes volumes, with a confirmation prompt on the destructive one.
8. Scan the images with a vulnerability scanner, fix what you reasonably
   can, and write up the image layering, network layout, and remaining
   findings.

## Extension Ideas
- Add a compose profile for a debug configuration with extra tooling.
- Add a backup sidecar that dumps the database nightly to a volume.
- Add resource limits and observe behavior under memory pressure.
- Add a second app replica and confirm nginx balances between them.

## Skills Demonstrated
- Production Dockerfile authoring and image optimization
- Multi-service composition with networks, volumes, and health checks
- Reverse proxy and TLS termination basics
- Lifecycle scripting and image vulnerability scanning

## Industry Relevance

SaaS, Agencies, Internal Platform Teams. Containers are the unit of deployment almost everywhere now, and the difference between a developer who "uses Docker" and a DevOps engineer is a small, secure image and a stack that comes up cleanly every time. This project is the foundation the rest of the track builds on and a common interview topic.
