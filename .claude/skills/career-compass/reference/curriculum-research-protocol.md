# Curriculum Research Protocol

This document governs `SKILL.md`'s curriculum-research step: synthesizing a
generic `<major>` curriculum archetype from multiple real schools' course
pages. There is no script for this step — it is genuinely the model's job
(`WebSearch` plus `WebFetch` plus judgment) — so this reference exists to
keep that judgment consistent across runs, the same way `career-compass`'s own
`reference/research-protocol.md` governs its target-role research step.

## Queries

Scope every query to the learner's stated `education_system` (from Learner
Context) — mixing curricula from different degree-length systems (e.g. a
3-year UK degree and a 4-year US degree) into one "generic" archetype would
produce nonsense, not a useful approximation.

- `"<major>" degree requirements course list <education system's country/
  system>`
- `typical "<major>" curriculum by year <education system>`
- `"<major>" course sequence recommended`

Run these against **at least 3 distinct universities within that same
education system**. Each candidate school's course/curriculum page must be
opened and read via `WebFetch` — the same "a `WebSearch` snippet never
counts on its own" rule `career-compass/reference/research-protocol.md` applies
to its own evidence bar applies here too.

If the learner's stated education system is unusual or unclear, note this
explicitly in the report and proceed with a wider, lower-confidence pool
of schools rather than blocking the run.

## Recording course codes as `aliases`

While reading each school's course page (already being read for the
grounding purposes below, at zero extra research cost), record that
school's actual course code (e.g. `"CS 2110"`) alongside the generic title
you're synthesizing (e.g. `"Data Structures"`). Add the code to that
synthesized course's `aliases: [string]` list. This is what lets Step 5's
`match_completed_courses()` match a learner who types a real course code
against the generic archetype entry — matching against `course_name`
alone could never do this.

## Course-to-skill grounding

A course enters `covers_skill_ids` only from its **fetched course
description or stated learning outcomes** — never from its title alone.
This mirrors `career-compass`'s own rule against inferring a skill from a bare
job-posting title.

For every skill a course is tagged with, resolve the free-text mention to
a canonical skill id via the same script `career-compass` uses:

```bash
python3 "${SKILL_DIR}/scripts/resolution.py" resolve-skill "<free text mention>"
```

Record the traceable evidence as `coverage_evidence: [{skill_id,
source_urls: [string]}]` — one entry per skill the course is tagged with,
so every specific claim is traceable to the source that backs it.

## Inclusion threshold

A course enters the raw `course_sequence[]` list only if its substance
(not necessarily its exact title or course code) appears at **≥2 of the
≥3 same-education-system schools consulted** — even under different course
codes at each school. Confidence is `medium` at exactly 2 corroborating
schools, `high` at 3 or more.

A course appearing at exactly 1 school is **excluded from
`course_sequence[]`**, but not discarded entirely — see "Target-aligned
electives" below.

## Target-aligned electives

A single-school course whose `covers_skill_ids` (via the same
fetched-description grounding rule above) includes a Critical- or
High-tier `target_requirements[]` skill_id is recorded in `electives[]`:
school name, course name, what it covers, and its evidence. Label it
explicitly as single-school so it is never confused with the generic,
multi-school-corroborated archetype in `course_sequence[]`.

## Recording sources

Each `course_sequence[]`/`electives[]` entry's `sources` list follows the
same shape:

```yaml
sources:
  - url: string
    title: string
    school: string
    accessed_at: <UTC ISO8601 timestamp>   # when this run fetched it
```

## Explicit disclaimer

Always render this disclaimer in the report's Header section: this is a
**generic curriculum archetype** synthesized from multiple schools within
the learner's stated education system — not any specific school's actual
course catalog. Exact course numbers, prerequisites, and availability must
be confirmed against the learner's actual school and academic advisor.
