---
title: "Integration Sample Apps and Customer-Facing Guides"
track: "solutions-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["api-design", "python", "javascript", "technical-documentation", "developer-experience"]
skill_prerequisites: ["python", "javascript", "http-fundamentals"]
project_prerequisites: ["product-demo-environment.md"]
prerequisite_learning_hours: 3
---

# Integration Sample Apps and Customer-Facing Guides

## Production Workflow Mirrored
1. Building the integrations customers ask for most as reusable samples
2. Writing guides that get a customer engineer to a working result fast
3. Handling authentication, pagination, errors, and rate limits properly
   so samples do not teach bad habits
4. Testing samples against the real API so they stay working
5. Publishing where customers and sales can find them

## What You'll Build
Three working integration samples for your product's API in two
languages (for example: bulk import from CSV, a webhook receiver that
syncs to another system, and a reporting extract to a spreadsheet or
warehouse), each with a customer-facing guide, proper auth and error
handling, automated tests against a sandbox, and a published index page
that sales and customers can link to.

## Student-Scope Notes
- Choose the three integrations from what discovery and proof-of-concept
  conversations actually asked for.
- Samples must be small enough to read in minutes and correct enough to
  copy; that tension is the skill.
- Publish on a public repository or an internal wiki, with the guides
  rendered.

## Steps
1. List the integration requests you have heard, pick the top three, and
   write a one-paragraph goal for each in the customer's words.
2. Build the first sample in the primary language with authentication
   from environment variables, pagination, retries on rate limits, and
   clear error messages.
3. Write its guide: prerequisites, setup, run, what to expect, and how
   to adapt it, tested by following it on a clean machine.
4. Port the sample to the second language, keeping structure parallel.
5. Build the second and third samples the same way, sharing a small
   helper module where sensible.
6. Add tests that run each sample against the sandbox in CI on a
   schedule, so an API change breaks the build, not a customer.
7. Publish the index page with a short description, language badges,
   and links, and have a peer follow one guide cold to find gaps.
8. Write up which requests the samples answered, the feedback from the
   cold run, and the maintenance plan.

## Extension Ideas
- Add a Postman or Bruno collection alongside the samples.
- Add a sample for the product's SSO or SCIM integration.
- Record a short walkthrough video for each sample.
- Contribute an improvement to the product's official SDK based on
  friction you found.

## Skills Demonstrated
- Building correct, readable API integration samples
- Customer-facing technical writing tested cold
- Multi-language sample maintenance with automated tests
- Publishing enablement assets that sales and customers use

## Industry Relevance

API-First SaaS, Payments, Developer Platforms. Solutions engineers in these sectors accelerate deals by handing customer engineers working code, and teams keep sample libraries for that reason. Three tested samples with cold-run-validated guides show you can produce assets customers actually integrate with.
