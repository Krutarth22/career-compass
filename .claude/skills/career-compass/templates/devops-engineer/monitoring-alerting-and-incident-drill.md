---
title: "Monitoring, Alerting, and an Incident Drill"
track: "devops-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["observability", "site-reliability-practices", "shell-scripting", "technical-documentation"]
skill_prerequisites: ["linux-cli", "docker"]
project_prerequisites: ["containerize-and-compose-a-stack.md"]
prerequisite_learning_hours: 3
---

# Monitoring, Alerting, and an Incident Drill

## Production Workflow Mirrored
1. Defining service-level indicators and objectives for a service
2. Collecting metrics and logs and building dashboards operators use
3. Writing alerts that page on symptoms, not causes, with runbook links
4. Responding to an incident with a timeline, mitigation, and communication
5. Writing a blameless postmortem with action items

## What You'll Build
An observability and reliability layer for the stack from
`containerize-and-compose-a-stack.md`: Prometheus and Grafana (or the
equivalent) collecting metrics from the app, proxy, and database, a log
aggregation path, a dashboard organized around SLIs, SLOs with error
budgets, alert rules that page on SLO burn with linked runbooks, and a
rehearsed incident where you inject a fault, respond, and write a
postmortem.

## Student-Scope Notes
- Everything runs on one host in docker-compose. A hosted alert
  receiver (email, a chat webhook, or a free-tier pager) is enough.
- Two or three SLIs (availability, latency, error rate) with one SLO
  each. Do not model every metric.
- The incident is self-inflicted and scheduled; the discipline of
  responding and writing it up is what you are practicing.

## Steps
1. Define SLIs for availability and latency at the proxy, and one SLO
   for each with a target and a window. Compute the error budget.
2. Add metrics exporters for the proxy, the database, and the host, and
   scrape them with Prometheus. Add the app's own metrics endpoint.
3. Add a log pipeline (Loki, or a file-based approach with structured
   JSON) so logs are queryable next to metrics.
4. Build a dashboard: SLI panels at the top, error budget remaining,
   then saturation (CPU, memory, connections), then per-service detail.
5. Write alert rules on SLO burn rate (fast and slow windows) plus one
   saturation alert, each annotated with a runbook link. Route them to
   your receiver and confirm delivery.
6. Write the runbooks the alerts link to: what the alert means, how to
   confirm, likely causes, mitigations, escalation.
7. Run the incident drill: inject a fault (fill the disk, kill the
   database, saturate CPU), respond using only the dashboard and
   runbooks, keep a timeline, and restore service.
8. Write a blameless postmortem: timeline, impact against the error
   budget, root cause, what went well, and concrete action items. Then
   implement at least one action item.

## Extension Ideas
- Add distributed tracing and link traces from the dashboard.
- Add synthetic probes from an external location.
- Add an on-call rotation and escalation policy in a free-tier pager.
- Add SLO reporting over a month with a burn-down chart.

## Skills Demonstrated
- SLI, SLO, and error-budget definition
- Metrics, logs, dashboards, and burn-rate alerting
- Runbook authoring and incident response
- Blameless postmortem practice

## Industry Relevance

Cloud Services, Fintech, Streaming Media. Site reliability practices are the hiring bar for SRE and production engineering roles in these sectors, and interviewers ask for a real incident you handled and what changed after. A drill with a dashboard, alerts, and a postmortem gives you that story with evidence.
