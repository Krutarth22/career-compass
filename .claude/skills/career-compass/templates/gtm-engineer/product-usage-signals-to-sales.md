---
title: "Product Usage Signals Routed to Sales"
track: "gtm-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["product-analytics", "data-pipelines", "workflow-automation", "crm-platforms", "python"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: ["crm-data-model-and-hygiene.md"]
prerequisite_learning_hours: 3
---

# Product Usage Signals Routed to Sales

## Production Workflow Mirrored
1. Instrumenting product events that indicate buying or churn intent
2. Defining product-qualified lead and health rules with the revenue team
3. Streaming signals into the CRM and alerting the right owner
4. Suppressing noise so reps trust the alerts
5. Measuring alert-to-action and action-to-outcome rates

## What You'll Build
A product-led signal system: event instrumentation in a sample
application (or a synthetic event stream modeled on one), definitions
for product-qualified leads and account health, a pipeline that
computes signals and writes them to CRM accounts, alerting to owners
through chat or tasks with suppression and batching rules, and a report
on alert volume, action rate, and outcomes.

## Student-Scope Notes
- A small app you or a peer built, with a few users, is enough for real
  events; otherwise generate a realistic synthetic stream and label it
  as such.
- Use a product analytics tool's free tier or your own event table.
- Suppression rules (one alert per account per week, no alerts on
  internal users) are required, not optional.

## Steps
1. Define with the "sales team" the signals that matter: activation
   milestones, usage thresholds, seat growth, feature adoption,
   inactivity. Write the rule for each.
2. Instrument the events (or generate them) with consistent user and
   account identifiers and a schema document.
3. Build the signal computation as scheduled SQL or Python producing an
   account-level table of signal states and scores.
4. Write signal states and scores to CRM account fields with a history
   log.
5. Build the alerting: on state changes, notify the owner via chat or a
   CRM task with context and a suggested action, applying suppression
   and batching.
6. Run it for at least two weeks, tracking alert volume, how many were
   actioned, and what happened.
7. Tune thresholds and suppression from the data and rerun.
8. Write up the signal definitions, the pipeline, the alert metrics
   before and after tuning, and the recommended playbook per signal.

## Extension Ideas
- Add a churn-risk score with a simple model and compare to rules.
- Add in-app messaging triggered by the same signals.
- Add a weekly account digest for customer success.
- Add reverse ETL to sync the warehouse signals to multiple tools.

## Skills Demonstrated
- Product event instrumentation and schema design
- Signal and health rule definition with a revenue team
- Pipeline to CRM with alerting and suppression
- Measuring and tuning alert effectiveness

## Industry Relevance

Product-Led SaaS, Developer Tools, Fintech. Product-led growth motions in these sectors depend on routing usage signals to sales and success teams without drowning them, and go-to-market engineers own that pipeline. A system with measured action rates and tuned suppression shows both the engineering and the judgment.
