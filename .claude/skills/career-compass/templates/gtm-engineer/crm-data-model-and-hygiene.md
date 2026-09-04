---
title: "CRM Data Model and Hygiene Automation"
track: "gtm-engineer"
difficulty_tier: "beginner"
estimated_hours: 12
role: "core"
skill_tags: ["crm-platforms", "data-modeling", "data-cleaning", "workflow-automation", "sql"]
skill_prerequisites: ["spreadsheet-analysis"]
project_prerequisites: []
prerequisite_learning_hours: 3
---

# CRM Data Model and Hygiene Automation

## Production Workflow Mirrored
1. Defining the objects, fields, and lifecycle stages a revenue team runs on
2. Auditing an existing CRM for duplicates, missing fields, and stale records
3. Automating deduplication, normalization, and enrichment rules
4. Enforcing data quality at entry with validation and required fields
5. Reporting data health so the team trusts the numbers

## What You'll Build
A cleaned and well-modeled CRM (a free-tier HubSpot or Salesforce
developer org, or an open-source CRM) for a realistic sales motion: a
documented object and field model with lifecycle stages, an audit of a
seeded messy dataset, automated hygiene rules (dedupe, normalize
company names and domains, standardize picklists), validation rules at
entry, and a data-health dashboard with trend over time.

## Student-Scope Notes
- Seed the CRM with a few thousand deliberately messy records (a public
  company list plus injected duplicates and inconsistencies) so the
  hygiene work is real.
- Use the CRM's native automation where it exists and scripts against
  its API where it does not.
- One sales motion (for example inbound SMB) is enough to define the
  model.

## Steps
1. Write the sales motion in one page: how leads arrive, qualify, become
   opportunities, and close, and what each stage means.
2. Design the data model: objects, required fields per stage, picklist
   values, ownership rules, and the lifecycle stage definitions.
3. Load the messy seed data and run an audit: duplicate rate, missing
   required fields, invalid emails and domains, stale records. Record
   the baseline.
4. Build the deduplication logic (matching on normalized domain and
   fuzzy name) and a merge process that preserves activity history.
5. Build normalization rules for company names, domains, countries, and
   job titles, and run them across the dataset.
6. Add validation and required-field rules at the stage transitions so
   bad data cannot enter, and test that they fire.
7. Build the data-health dashboard: the audit metrics over time, by
   owner and source, with a weekly snapshot.
8. Rerun the audit, document the before and after, and write the data
   standards guide the team would follow.

## Extension Ideas
- Add enrichment from a public data source keyed by domain.
- Add an ownership routing rule set (territory, round robin).
- Add a stale-record workflow that prompts owners to update or close.
- Sync the cleaned data to a warehouse with SQL models.

## Skills Demonstrated
- Revenue data modeling and lifecycle design
- CRM auditing, deduplication, and normalization
- Entry-point validation and automation
- Data-health reporting

## Industry Relevance

B2B SaaS, Fintech, Recruiting and Staffing. Revenue teams in these sectors run entirely on CRM data, and go-to-market engineers exist because bad data silently breaks routing, forecasting, and outbound. A documented model with measured hygiene improvement is the foundational GTM engineering artifact.
