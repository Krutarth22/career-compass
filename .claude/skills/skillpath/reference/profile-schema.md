# Profile Schema

`profile.yaml` holds a user's skillpath profile: current background, target
role, constraints, and preferences. It lives at the repo root (path resolved
the same way everywhere skillpath touches it — see the merge rule below) and
is gitignored (personal data), so a fresh checkout never has one until a user
creates it. `profile.yaml.example` (created in Task 1) is a filled-in,
plausible example of this exact schema and is checked into git as
documentation/fixture data.

## Schema

```yaml
current_role: string
years_experience: number
current_skills:
  - skill: string
    proficiency: aware | practiced | proficient
    evidence: string   # optional
target_role: string
target_level: string    # optional
location: string         # optional but recommended
industry_preference: string  # optional
weekly_time_budget_hours: number
horizon_weeks: number     # default 12 if unset
constraints:
  - string
last_updated: date
```

Field notes:

- `current_role`, `years_experience`, `target_role`, `weekly_time_budget_hours`
  are required.
- `current_skills` is a list; each entry requires `skill` and `proficiency`.
  `proficiency` is one of exactly three values: `aware`, `practiced`,
  `proficient` (least to most confident). `evidence` is a free-text optional
  field giving a concrete example backing the claimed proficiency.
- `target_level` (e.g. "Senior ML Engineer", "Staff") is optional — when
  present it is used for level-aware resolution (see
  [`track-aliases.md`](./track-aliases.md) for how level words are stripped
  before matching `target_role` to a track).
- `location` and `industry_preference` are optional but recommended; they
  feed into live research queries (job postings, courses relevant to the
  user's region/industry).
- `horizon_weeks` defaults to `12` when unset — code that reads `profile.yaml`
  should apply this default rather than treating a missing value as an
  error.
- `constraints` is a free-text list of things the plan must respect (e.g.
  "must keep current job", "limited budget", "prefer open-source
  resources").
- `last_updated` is a date (ISO 8601, `YYYY-MM-DD`) set whenever
  `profile.yaml` is written.

See `profile.yaml.example` at the repo root for a complete, realistic
instance of this schema.

## Argument / profile merge rule

skillpath can be invoked with CLI arguments that supply some or all profile
fields (e.g. `--target-role`, `--weekly-hours`), and/or an existing
`profile.yaml` may already be on disk. The two interact according to exactly
three cases:

1. **No `profile.yaml` exists.** Always run the profile-creation flow,
   regardless of whether CLI args were supplied. Any supplied args pre-fill
   the relevant fields in that flow (so the user isn't asked to retype
   values they already gave on the command line) rather than skipping the
   flow entirely. `profile.yaml` is written at the end of the run either
   way — a first run always results in a saved profile.

2. **`profile.yaml` exists and args are supplied.** The supplied args are
   treated as a **this-run-only override** on top of the saved profile —
   they are used for the current run's resolution/research/report but the
   saved `profile.yaml` on disk is **never silently overwritten**. After the
   run completes, the user is asked once whether they'd like the override
   values saved permanently; only an explicit "yes" updates `profile.yaml`.

3. **`profile.yaml` exists and no args are supplied.** Use the file as-is —
   no prompts, no overrides, no rewrite.

This rule is implemented in Task 4/6 profile-loading code and orchestrated by
Task 8's `SKILL.md`; it is documented here as the single source of truth for
that behavior so both can be built and tested against the same rule.
