# Track Aliases

CareerCompass ships a fixed set of career "tracks" (each backed by a directory of
templates under `.claude/skills/career-compass/templates/`). A user's
`target_role` is free text — "ML Engineer", "Senior Machine Learning
Engineer", "AI/ML Engineer II" — and has to be resolved to one of those
track IDs before templates can be selected.

The alias registry itself is data, not prose: it lives in the sibling file
[`track-aliases.yaml`](./track-aliases.yaml) as a plain YAML mapping, so
`resolution.py` (Task 4) can load it directly with
`yaml.safe_load(open(...))` — no Markdown-fence-stripping required.

## Entry schema

`track-aliases.yaml` is a mapping from track ID to an alias list:

```yaml
ml-engineer:
  aliases: ["ml engineer", "machine learning engineer", "mle"]
```

- The top-level key (`ml-engineer` above) is the canonical track ID. It
  matches the name of the corresponding directory under
  `.claude/skills/career-compass/templates/` (e.g.
  `.claude/skills/career-compass/templates/ml-engineer/`).
- `aliases` is a list of lowercase phrasings — written without seniority/level
  words — that should resolve to that track.

## Resolution rule (implemented in Task 4)

Given a `target_role` string, `resolution.py` resolves it to a track ID as
follows:

1. **Normalize.** Lowercase the entire string, then strip level/seniority
   words wherever they appear as whole words (e.g. `junior`, `senior`,
   `mid`, `mid-level`, `staff`, `principal`, `lead`, `i`, `ii`, `iii`) and
   collapse any resulting extra whitespace. For example, `"Senior ML
   Engineer"` normalizes to `"ml engineer"`.
2. **Match.** Compare the normalized string against every track's `aliases`
   list using **exact match or bounded phrase match only** — the normalized
   `target_role` matches a track if it equals an alias, or an alias appears
   as a substring of it (or vice versa, depending on which is more specific;
   the implementation should treat this as "the normalized role contains the
   alias, or the alias contains the normalized role"). A match is accepted
   only when it points to one track. An exact alias intentionally shared by
   multiple tracks resolves to `null`, allowing the host to ask the user which
   one they mean. **No fuzzy or semantic matching** (no edit distance, no
   embeddings, no LLM calls) — this keeps resolution deterministic and testable.
3. **No match.** If nothing matches, resolution fails explicitly rather than
   guessing — the caller (Task 6/8) is responsible for deciding what to do
   next (e.g. asking the user to pick a track, or erroring out).

## Adding a new track

Adding a new track means adding both a new top-level key here (with a
reasonably exhaustive alias list covering common real-world phrasings and
abbreviations) and a matching template directory under
`.claude/skills/career-compass/templates/<track-id>/`. Currently seeded:

- Data & AI: `ai-engineer`, `ml-engineer`, `data-engineer`,
  `data-analyst`, `data-scientist`.
- Software engineering: `backend-engineer`, `frontend-engineer`,
  `full-stack-engineer`, `mobile-engineer`, `devops-engineer`,
  `security-engineer`, `qa-automation-engineer`,
  `embedded-software-engineer`, `game-developer`.

## Ambiguous titles and `track-candidates`

`resolve_track` returns `null` for an exact alias shared by more than one
track. Its companion `track_candidates` (CLI: `resolution.py
track-candidates "<role>"`) returns every track that alias belongs to, so
the host can ask the user to pick instead of guessing. Two title families
are deliberately shared today:

- `ai/ml engineer` -> `ai-engineer`, `ml-engineer` (rationale below).
- `software engineer`, `software developer`, `programmer` ->
  `backend-engineer`, `frontend-engineer`, `full-stack-engineer`. A bare
  "Software Engineer" posting can mean any of the three, and the template
  sets differ substantially (services and databases vs. browser UI vs.
  both plus deployment), so the user is asked. Titles that name the side
  (`backend developer`, `react engineer`, `full stack developer`) resolve
  directly.

Other software tracks are kept distinct on the same evidence basis used
for the data tracks: `devops-engineer` absorbs `sre`, `platform engineer`
and `cloud engineer` because postings for all three center on CI/CD,
infrastructure as code, Kubernetes and observability; `qa-automation-engineer`
absorbs `sdet` and `test engineer`; `embedded-software-engineer` absorbs
`firmware engineer` and `iot engineer`; `security-engineer` is scoped to
application/product security (`appsec`, `devsecops`) -- `security analyst`
and SOC titles are intentionally not aliased because they are
operations-centric roles with a different skill set.

`ai-engineer` and `ml-engineer` are deliberately separate tracks, not one
merged "AI/ML Engineer" track: live research (job postings and
practitioner sources, current as of August 2026) consistently draws the
line as model-building vs. model-using. An ML Engineer builds, trains, and
operates custom models — the model is the product, and the role expects
production coding plus ML fundamentals (feature engineering, training,
deployment, monitoring). An AI Engineer builds product features on top of
existing foundation models via APIs, RAG, and agents — the model is a
dependency, and the role centers on integration, evaluation, and
LLM-application observability rather than training. Someone targeting
"AI/ML Engineer" loosely should be asked (or should pick) which of the two
they actually mean; the aliases below do not merge them.

`business intelligence engineer`/`bi engineer` resolve to `data-engineer`, not
`data-analyst`, on the same evidence basis: live research shows the role
centers on ETL pipelines, data warehouse/model design, and tools like
Airflow/Redshift/BigQuery/Snowflake — data-engineering work. `business
intelligence analyst`/`bi analyst`, by contrast, is SQL + dashboarding
(Tableau/Power BI) + stakeholder reporting — the same day-to-day as
`data-analyst`, so it stays aliased there rather than becoming its own
track; research found no distinct skill set to justify a split. The broader
`business analyst` title is intentionally not aliased because many such roles
center on process, requirements, or operations rather than data analytics.

Likewise, `quantitative analyst` is not treated as a synonym for
`data-scientist`: quant roles commonly require finance-specific mathematics
and modeling that the current data-science templates do not cover.
