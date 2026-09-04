---
title: "Security Logging and Detection Rules"
track: "security-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["security-monitoring", "observability", "network-security", "linux-cli"]
skill_prerequisites: ["linux-cli", "docker"]
project_prerequisites: []
prerequisite_learning_hours: 4
---

# Security Logging and Detection Rules

## Production Workflow Mirrored
1. Deciding which security-relevant events to log and in what shape
2. Centralizing logs from application, host, and network sources
3. Writing detection rules for known attack patterns and tuning them
4. Alerting with enough context to act, and measuring false positives
5. Investigating an alert back to root cause with the logs

## What You'll Build
A small detection stack on a host you control: an application emitting
structured security events (logins, failures, privilege changes, admin
actions), host authentication and process logs, reverse-proxy access
logs, all shipped to a central store (Loki, OpenSearch, or a SIEM's
free tier), with at least six detection rules (brute force, credential
stuffing pattern, privilege escalation, suspicious admin action,
scanner signatures, impossible travel or new-device login), tuned
against benign traffic, and an investigation write-up for one triggered
alert.

## Student-Scope Notes
- Generate attack traffic only against your own host, with simple
  scripts or the training tooling from earlier templates.
- Six rules that are tuned and documented beat thirty copied from a
  rule pack.
- Network logs from a firewall or IDS are an extension; proxy access
  logs are sufficient for the core.

## Steps
1. Define the security event schema for the application (event type,
   actor, target, outcome, source IP, user agent, request id) and emit
   it for every authentication and authorization decision.
2. Ship application, host auth, and proxy logs to the central store with
   consistent timestamps and fields.
3. Generate a baseline of benign traffic (normal use plus automated
   browsing) for at least a day so you can measure false positives.
4. Write the first three rules (brute force, scanner signatures,
   privilege change) as queries, then run your own attack simulations
   to confirm each fires.
5. Write three more rules covering behavioral patterns (many accounts
   from one IP, admin action outside business hours, new-device login),
   and tune thresholds against the benign baseline.
6. Route alerts to a receiver with the full context needed to
   investigate: the triggering events, the actor, and links to the
   query.
7. Trigger one alert, investigate it back to the originating requests,
   and write an investigation report with a timeline and conclusion.
8. Document each rule (intent, logic, threshold, known false positives,
   response) and write up the detection coverage against a framework
   such as MITRE ATT&CK for the relevant techniques.

## Extension Ideas
- Add a host intrusion detection agent and rules on its output.
- Add automated enrichment (GeoIP, threat-intel lookups) to alerts.
- Add a rule-testing harness that replays sample logs in CI.
- Add a weekly detection-coverage report.

## Skills Demonstrated
- Security event logging design
- Log centralization across application, host, and proxy
- Detection rule authoring and tuning
- Alert investigation and documentation

## Industry Relevance

Financial Services, SaaS, Managed Security Providers. Detection engineering is one of the fastest-growing security specialties in these sectors, and candidates are assessed on whether they can write and tune rules against real logs rather than just operate a vendor console. A stack with tuned rules and an investigation write-up is the work sample those teams want.
