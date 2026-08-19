# Research Protocol

This document governs Step 3 of `SKILL.md`'s main flow: researching live
target-role requirements. There is no script for this step — it is
genuinely the model's job (WebSearch plus judgment) — so this reference
exists to keep that judgment consistent across runs instead of being
re-invented ad hoc each time.

## Building queries

Derive queries from the loaded profile's `target_role`, `target_level` (if
present), and `location` (if present). Run two kinds of queries:

1. **Current-year market-relevance queries** — job postings and
   "what does an X actually do" discussion threads, filtered or phrased to
   favor the current calendar year (determine "current year" from the
   invocation's actual date, never hardcode a year). These surface what is
   in demand right now, not what was in demand three years ago.
2. **Evergreen canonical-doc queries** — official framework/tool
   documentation, well-established standards, and foundational practitioner
   references. These are exempt from the current-year filter: a canonical
   doc describing how RAG evaluation works, for example, does not go stale
   on a yearly cycle the way a hiring-trend claim does.

When `location` is present, fold it into the market-relevance queries
(e.g. "<target_role> job postings <location> <year>") — regional market
differences are real and the profile schema recommends `location` for
exactly this reason (see `reference/profile-schema.md`).

## Evidence bar

Before a requirement is treated as validated (rather than merely
suggested), it must clear:

- **≥4 real job postings** mentioning it, and
- **≥2 practitioner sources** (blog posts, conference talks, engineering
  team write-ups, well-attended forum threads — not marketing copy or
  SEO-farmed listicles) corroborating it.

A requirement that falls short of this bar is not discarded — it is
recorded with a lower confidence score (see below) rather than silently
dropped, so the tiering step in the main flow can still down-weight it
appropriately.

## Recording sources

For every surfaced requirement, resolve its free-text mention to a
canonical skill id via:

```
python3 "${SKILLPATH_SCRIPTS}/resolution.py" resolve-skill "<free text mention>"
```

which prints `{"id": "...", "unmapped": true|false}` (see `SKILL.md`'s
"Bash invocations" section for the exact `${SKILLPATH_SCRIPTS}` resolution).
An `unmapped: true` result is expected and fine for live research — per
`reference/skill-taxonomy.md`'s "two enforcement levels", live research
output is soft/provisional and is never blocked on taxonomy membership.

Build each `target_requirements` entry per `report_state.py`'s frontmatter
schema (see `reference/report-format.md`):

```yaml
- skill_id: string          # from resolve-skill above
  unmapped: boolean          # from resolve-skill above
  category: hard | tooling | domain | soft | credential
  frequency_signal: number   # count of independent sources mentioning it
  sources:
    - url: string
      type: posting | article | forum | interview-prep | docs
      title: string
      company: string | null
      role_level: string | null
      location: string | null
      posted_at: date | null
      accessed_at: <UTC ISO8601 timestamp>   # when this run fetched it
```

`category` is a judgment call: `hard` for technical/tool skills proper,
`tooling` for a specific product/platform, `domain` for subject-matter
knowledge, `soft` for communication/collaboration skills, `credential` for
degrees/certifications explicitly requested.

## Confidence scoring

Score each requirement's evidence, and roll the set up into the report's
overall `research_confidence`:

- **high** — clears the full evidence bar (≥4 postings + ≥2 practitioner
  sources), and the postings are either current-year or backed by an
  evergreen canonical doc for non-time-sensitive claims.
- **medium** — partial evidence: meets one half of the bar but not the
  other (e.g. 4+ postings but only one practitioner source, or vice
  versa), or evidence is a mix of current and slightly dated sources.
- **low** — thin evidence: a single source, or sources that are stale,
  low-quality, or contradict each other without resolution.

Confidence feeds directly into Step 4's tiering: a requirement scored
**low** confidence is capped at tier **Medium** even if its raw
frequency/centrality would otherwise suggest Critical or High — thin
evidence should never produce a Critical-tier claim in a report someone is
using to plan months of study time.
