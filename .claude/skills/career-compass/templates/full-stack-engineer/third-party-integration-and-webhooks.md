---
title: "Third-Party Integration with Webhooks"
track: "full-stack-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["api-design", "background-jobs", "authentication-authorization", "automated-testing"]
skill_prerequisites: ["backend-frameworks", "http-fundamentals"]
project_prerequisites: ["crud-app-end-to-end.md"]
prerequisite_learning_hours: 3
---

# Third-Party Integration with Webhooks

## Production Workflow Mirrored
1. Authenticating to an external API with OAuth or API keys kept out of code
2. Calling it reliably with timeouts, retries, and rate-limit handling
3. Receiving webhooks, verifying signatures, and processing them
   idempotently
4. Reflecting external state in your own data model and UI
5. Testing all of it without hitting the real service in CI

## What You'll Build
Integrate the app from `crud-app-end-to-end.md` with one real external
service that offers both an API and webhooks (Stripe test mode, GitHub,
Slack, a calendar provider): the user connects their account, your app
calls the service on their behalf, and incoming webhooks update your
records and the UI. Every external call is resilient and every webhook is
verified and idempotent.

## Student-Scope Notes
- Use the provider's sandbox or test mode. Never use real money or a
  real production account.
- Expose your local webhook endpoint with a tunnel (ngrok, cloudflared,
  or the provider's CLI) during development.
- One integration done properly is the target; a marketplace of
  integrations is not.

## Steps
1. Read the provider's API and webhook docs and write a one-page
   integration design: the connect flow, the calls you make, the webhook
   events you handle, and the data you store.
2. Implement the connect flow (OAuth or API-key entry) with credentials
   stored encrypted or in a secrets store, never in the repo or in plain
   text.
3. Write a client module for the outbound calls with timeouts, retries
   with backoff on 5xx and 429, and structured logging of every call.
4. Implement the webhook endpoint: verify the signature, return 2xx fast,
   and hand the event to a background job for processing.
5. Make webhook processing idempotent using the provider's event id, and
   prove it by replaying the same event twice.
6. Update your data model and UI so the external state is visible (for
   example payment status, sync status, last synced time).
7. Write tests using recorded fixtures or the provider's mock library so
   CI runs without network access, including a test for an invalid
   signature and a duplicate event.
8. Write up the failure modes (provider down, webhook delayed, out-of-
   order events) and how your design handles each.

## Extension Ideas
- Add a reconciliation job that polls the provider to catch missed
  webhooks.
- Handle out-of-order events with the provider's timestamps or sequence.
- Add a disconnect flow that revokes tokens.
- Add a second provider behind a shared interface.

## Skills Demonstrated
- OAuth and secure credential handling for third-party APIs
- Resilient outbound HTTP clients
- Signed, idempotent webhook processing
- Testing external integrations without network access

## Industry Relevance

Fintech, E-commerce, B2B SaaS. Almost every product in these sectors integrates with payments, messaging, or partner platforms, and the incidents that make the news usually come from unverified webhooks or non-idempotent handlers. Full-stack engineers who can ship a clean integration are hired to own those boundaries.
