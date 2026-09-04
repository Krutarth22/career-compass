---
title: "Supply Chain and Pipeline Security Hardening"
track: "security-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["vulnerability-assessment", "ci-cd", "secrets-management", "docker"]
skill_prerequisites: ["git-version-control", "linux-cli"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# Supply Chain and Pipeline Security Hardening

## Production Workflow Mirrored
1. Inventorying dependencies and producing a software bill of materials
2. Scanning dependencies, containers, and infrastructure code in CI
3. Pinning, verifying, and signing artifacts so builds are reproducible
4. Keeping secrets out of repositories and rotating them when leaked
5. Locking down the pipeline's own permissions

## What You'll Build
A hardened CI pipeline for an application repository you own: an SBOM
generated on every build, dependency and container vulnerability
scanning with a severity gate, secret scanning with a pre-commit hook and
a CI check, pinned and hash-verified dependencies and base images,
signed container images verified before deploy, least-privilege pipeline
tokens, and a documented response to a simulated leaked secret.

## Student-Scope Notes
- Use free tooling (Syft/Grype or Trivy, gitleaks, cosign, the CI
  platform's own scanning). Vendor platforms are not required.
- One repository with one deployable is enough.
- The leaked-secret simulation uses a dummy credential you create for
  the purpose.

## Steps
1. Generate an SBOM for the application and its container image and
   store it as a build artifact.
2. Add dependency scanning and container scanning to CI with a gate
   that fails on high or critical findings, then fix or justify each
   current finding.
3. Pin every dependency with a lockfile and hashes, and pin base images
   by digest. Confirm two builds produce identical dependency sets.
4. Add secret scanning as a pre-commit hook and a CI check, then commit a
   dummy secret on a branch and confirm both catch it.
5. Sign the container image in CI and add a verification step to the
   deploy job that refuses unsigned or mismatched images.
6. Audit the pipeline's permissions: minimal token scopes, no
   long-lived cloud keys (use OIDC federation), and protected branches
   with required reviews.
7. Simulate a leaked credential: "discover" the dummy secret in history,
   rotate it, purge it, and document the timeline and steps.
8. Write up the pipeline's security controls as a checklist another
   team could adopt, and note which controls you would add at larger
   scale.

## Extension Ideas
- Add SLSA provenance attestations to the build.
- Add license compliance checks to the SBOM step.
- Add infrastructure-as-code scanning for misconfigurations.
- Add a policy that blocks new dependencies without review.

## Skills Demonstrated
- SBOM generation and dependency, container, and secret scanning
- Reproducible, pinned, and signed builds
- Pipeline permission hardening
- Credential leak response

## Industry Relevance

Software Vendors, Fintech, Government Contractors. Supply chain requirements now flow down from customers and regulators in these sectors, and DevSecOps roles are specifically hired to implement SBOMs, signing, and scanning gates. A pipeline that already has all of them, with a rehearsed leak response, is a direct match.
