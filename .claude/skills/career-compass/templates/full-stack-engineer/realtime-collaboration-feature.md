---
title: "Real-Time Collaboration Feature"
track: "full-stack-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["realtime-communication", "state-management", "backend-frameworks", "concurrency"]
skill_prerequisites: ["javascript", "backend-frameworks"]
project_prerequisites: ["crud-app-end-to-end.md"]
prerequisite_learning_hours: 3
---

# Real-Time Collaboration Feature

## Production Workflow Mirrored
1. Choosing a transport (WebSockets vs. server-sent events) for the use case
2. Broadcasting changes to every connected client for a shared resource
3. Reconciling concurrent edits without losing data
4. Handling disconnects, reconnects, and missed messages
5. Showing presence so users know who else is here

## What You'll Build
Add live collaboration to the app from `crud-app-end-to-end.md`: when two
users view the same record, edits by one appear for the other within a
second, a presence indicator shows who is viewing, and a simple conflict
strategy (last-write-wins with a visible notice, or per-field merging)
prevents silent data loss. Reconnecting clients catch up on what they
missed.

## Student-Scope Notes
- One server process is enough; a pub/sub layer (Redis) for multiple
  server instances is an extension.
- Full operational-transform or CRDT text editing is out of scope. Field
  or record-level sync with a documented conflict rule is the target.
- Test with two browser windows and a throttled network in DevTools.

## Steps
1. Write down the events (record updated, user joined, user left, cursor
   or field focus) and their payloads, and choose WebSockets or SSE with a
   one-paragraph justification.
2. Implement the server side: a connection registry keyed by record id,
   authentication on connect, and broadcast on every write to that record.
3. Implement the client side: subscribe when the record view mounts,
   apply incoming updates to local state, and unsubscribe on unmount.
4. Add presence: broadcast join and leave, render avatars of current
   viewers, and expire stale presence on disconnect.
5. Add a version number to the record and implement your conflict rule.
   Reproduce a conflict with two windows and confirm nothing is silently
   lost.
6. Add reconnection with backoff and a catch-up mechanism (a since-version
   fetch on reconnect) so a client that dropped for ten seconds ends up
   consistent.
7. Write an integration test that opens two client connections, edits
   from one, and asserts the other receives the update.
8. Write up the protocol, the conflict rule and its trade-offs, and what
   you would need to add for multiple server instances.

## Extension Ideas
- Add Redis pub/sub and run two server instances behind a proxy.
- Add per-field locking or a CRDT library for a text field.
- Add typing indicators and live cursors.
- Add offline queueing of edits with replay on reconnect.

## Skills Demonstrated
- WebSocket or SSE transport design and authentication
- Broadcast, presence, and reconnection handling
- Concurrency and conflict reasoning for shared state
- Integration testing of multi-client behavior

## Industry Relevance

Collaboration Software, EdTech, Logistics Dashboards. Live-updating shared views are now table stakes in these sectors, from shared documents to dispatch boards, and full-stack candidates who can explain reconnection and conflict handling are far rarer than those who can call a WebSocket library. This feature is the kind of thing hiring managers ask you to whiteboard.
