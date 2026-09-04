---
title: "Offline-First Notes App with Sync"
track: "mobile-engineer"
difficulty_tier: "intermediate"
estimated_hours: 18
role: "core"
skill_tags: ["offline-first-data-sync", "mobile-development", "relational-databases", "concurrency"]
skill_prerequisites: ["mobile-development", "api-design"]
project_prerequisites: ["api-backed-list-detail-app.md"]
prerequisite_learning_hours: 4
---

# Offline-First Notes App with Sync

## Production Workflow Mirrored
1. Making the local database the source of truth for the UI
2. Queueing changes made offline and replaying them when connectivity
   returns
3. Pulling remote changes incrementally and merging them locally
4. Resolving conflicts when the same record changed on two devices
5. Showing sync status honestly so users trust their data

## What You'll Build
A notes app that works fully offline, persists to a local database
(SQLite, Room, Core Data, Realm, or the framework equivalent), syncs with
a small backend you run (a minimal REST API with a changes-since
endpoint), and handles the same note being edited on two devices with a
documented conflict rule and a visible sync indicator.

## Student-Scope Notes
- The backend is deliberately tiny: create/update/delete notes plus a
  `since` endpoint returning changes after a timestamp or version.
  Running it locally is fine.
- Test "two devices" with a simulator and a physical device, or two
  simulators.
- Last-write-wins with a "conflicted copy" is an acceptable conflict
  rule; per-field merge and CRDTs are extensions.

## Steps
1. Define the note schema with an id generated on the device, a version
   or updated-at, and a deleted flag for tombstones. Define the sync
   protocol in one page.
2. Build the local database layer and make the UI read only from it,
   observing changes reactively.
3. Build the outbox: every local mutation writes to the database and
   appends to a pending-changes queue.
4. Build the push side: when online, replay the outbox to the server in
   order, mark entries done, and handle server rejections.
5. Build the pull side: fetch changes since the last sync cursor, apply
   them locally, and advance the cursor atomically.
6. Implement the conflict rule and reproduce a conflict by editing the
   same note on two devices while one is offline. Confirm no edit is
   silently lost.
7. Add a sync status indicator (synced, pending N changes, offline,
   error) and a manual sync trigger.
8. Write tests for the outbox ordering, the conflict rule, and cursor
   handling, then write up the protocol, the conflict trade-offs, and
   the edge cases you found.

## Extension Ideas
- Add per-field merging for title and body separately.
- Add attachments with resumable uploads.
- Add background sync using the platform's background task APIs.
- Add end-to-end encryption of note bodies.

## Skills Demonstrated
- Local-first data architecture on mobile
- Outbox pattern and incremental sync protocol design
- Conflict detection and resolution
- Reactive UI over a local database

## Industry Relevance

Field Services, Healthcare, Logistics. Apps used by technicians, nurses, and drivers must work without signal and sync safely later, and data loss in these contexts has real consequences. Mobile engineers who have built a sync engine and can explain its conflict rule are sought after in every one of these sectors.
