---
title: "Release Pipeline and Store Submission"
track: "mobile-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["app-store-release", "ci-cd", "mobile-development", "automated-testing"]
skill_prerequisites: ["mobile-development", "git-version-control"]
project_prerequisites: ["api-backed-list-detail-app.md"]
prerequisite_learning_hours: 3
---

# Release Pipeline and Store Submission

## Production Workflow Mirrored
1. Managing signing credentials and build configurations safely
2. Building, testing, and versioning the app automatically in CI
3. Distributing beta builds to testers
4. Submitting to the App Store or Play Store with correct metadata
5. Monitoring crashes after release and shipping a hotfix

## What You'll Build
A fully automated release pipeline for the app from
`api-backed-list-detail-app.md`: CI that runs tests, builds a signed
release, bumps the version, and uploads to TestFlight or Play internal
testing on every tag, followed by a real store submission (or a complete
submission-ready package if you choose not to publish), crash reporting,
and a documented hotfix procedure you have rehearsed once.

## Student-Scope Notes
- Requires the relevant developer account. If you do not want to pay
  for one, complete everything up to the store upload and document the
  remaining steps with screenshots of the store console in a sandbox.
- Use fastlane or the platform's official CI tooling; hand-clicking in
  Xcode or Android Studio does not count as a pipeline.
- Signing secrets live in CI secret storage, never in the repo.

## Steps
1. Set up build configurations (debug, staging, release) with different
   API endpoints and bundle identifiers.
2. Put signing credentials (certificates, provisioning profiles, or
   keystore) in CI secret storage and get a signed release build from CI.
3. Add automated version and build number bumping tied to git tags.
4. Run the unit and UI test suites in CI on every pull request, and gate
   the release build on them passing.
5. Upload to TestFlight or Play internal testing from CI and invite at
   least one tester.
6. Prepare store metadata (description, screenshots for required
   sizes, privacy declarations) and submit for review, or assemble the
   complete package if not publishing.
7. Integrate crash reporting, trigger a test crash, and confirm it
   appears with symbolicated stack traces.
8. Rehearse a hotfix: branch from the release tag, fix a bug, run the
   pipeline, and ship a new build. Write the release runbook.

## Extension Ideas
- Add staged rollouts and monitor crash-free rate before expanding.
- Add screenshot automation for every locale and device size.
- Add over-the-air updates for a cross-platform app.
- Add release notes generation from commit history.

## Skills Demonstrated
- Signing, build configurations, and secret handling for mobile
- CI-driven build, test, version, and distribution
- Store submission and compliance metadata
- Crash monitoring and hotfix procedures

## Industry Relevance

Consumer Apps, Banking, Healthcare Apps. Regulated and high-volume app publishers cannot afford manual releases, and store rejections or broken signing cause missed launches. Mobile engineers who can own the release pipeline end to end are valued in any team shipping to millions of devices.
