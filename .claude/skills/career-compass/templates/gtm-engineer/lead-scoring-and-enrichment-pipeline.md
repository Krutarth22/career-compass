---
title: "Lead Enrichment and Scoring Pipeline"
track: "gtm-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["data-pipelines", "python", "sql", "crm-platforms", "api-design"]
skill_prerequisites: ["python", "sql"]
project_prerequisites: ["crm-data-model-and-hygiene.md"]
prerequisite_learning_hours: 3
---

# Lead Enrichment and Scoring Pipeline

## Production Workflow Mirrored
1. Enriching new leads with firmographic and technographic data from
   external sources
2. Scoring fit and intent with transparent, adjustable rules
3. Writing scores and enrichment back to the CRM and routing accordingly
4. Handling API limits, costs, and data freshness
5. Measuring whether the score predicts conversion

## What You'll Build
A pipeline that takes new leads from your CRM, enriches them from at
least two external sources (a public company data API, a website
technology detector, a domain lookup), computes a fit score from
documented rules and an intent score from engagement signals, writes
both back with an explanation field, routes leads by score, and a
backtest showing how the score would have predicted historical
conversions in your seeded data.

## Student-Scope Notes
- Use free or trial tiers of enrichment APIs and cache aggressively;
  note the cost per lead you would incur at scale.
- Rules-based scoring is the target; a model is an extension. Sales
  teams need to understand why a lead scored high.
- Backtest on your seeded dataset with synthetic outcomes if you lack
  real history, and say so.

## Steps
1. Define the ideal customer profile with the "sales team" (a peer or
   mentor): industry, size, geography, technology, and role criteria,
   each with a weight.
2. Build the enrichment step: for each new lead, call the sources, cache
   results, handle rate limits and failures, and store the raw payloads.
3. Implement fit scoring from the profile rules with a human-readable
   explanation string per lead.
4. Implement intent scoring from engagement events (page views, email
   opens, product signups) with decay over time.
5. Write scores, enrichment fields, and explanations back to the CRM and
   implement routing (high fit and intent to a named queue, low to
   nurture).
6. Backtest: apply the scoring to historical leads with known outcomes
   and report precision and lift by score band.
7. Schedule the pipeline, add monitoring for failures and enrichment
   coverage, and track cost per lead.
8. Write up the scoring rules, the backtest results, the cost model, and
   how the team adjusts weights.

## Extension Ideas
- Train a simple model on the enriched features and compare to rules.
- Add account-level scoring by aggregating leads per company.
- Add a feedback loop where reps rate lead quality and it adjusts weights.
- Add a data-freshness policy that re-enriches stale records.

## Skills Demonstrated
- External API enrichment with caching and limits
- Transparent scoring logic with explanations
- CRM write-back and routing automation
- Backtesting and cost analysis of a scoring system

## Industry Relevance

B2B SaaS, Fintech, Marketplaces. Lead prioritization decides where sales time goes in these sectors, and go-to-market engineers own the enrichment and scoring plumbing that feeds it. A pipeline with a backtest and a cost model demonstrates both the engineering and the commercial judgment the role demands.
