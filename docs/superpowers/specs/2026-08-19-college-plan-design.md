# college-plan — a major-to-career course sequencing skill

## Context

`skillpath` already answers "what am I missing to become an X" for someone
who already has work experience and closes gaps via projects and online
courses. It does not answer a different, earlier question: "I'm entering
(or already in) college, majoring in Y — what courses should I actually
take, in what order, to end up qualified for career X?"

That's a genuinely different shape of problem, not a smaller version of the
same one:

- The learner typically has near-zero `current_skills`, so proficiency
  diffing against a profile matters far less than knowing which courses in
  a normal `<major>` curriculum cover which target-role requirements, and
  in what year.
- Gaps get closed by **choosing courses in a multi-year degree sequence**,
  not by building projects or picking arbitrary online resources.
- A learner may already be partway through their degree, with some courses
  done and some in progress — the tool must place them correctly in an
  existing sequence, not always hand back a fresh four-year plan.
- There is no single school's catalog to consult (confirmed with the user
  — this is major-based, not school-based); the result is necessarily a
  **generic curriculum archetype**, not one institution's exact course
  numbers.

`college-plan` is a new, small, explicit-invocation skill that reuses
several pieces of `skillpath` exactly as they exist today — the
target-role research procedure (`reference/research-protocol.md`), the
skill-resolution module (`scripts/resolution.py`), and the report-file
writer (`scripts/report_state.py`) — and adds two new things: a
curriculum-research pass with its own deterministic coverage-diff script,
and a course-sequencing report. It does not require a prior `/skillpath`
run or an existing `profile.yaml`; both are used opportunistically when
present, never required.

*Revision note: this is the second pass. Round 1 review (docs/superpowers/specs
comment) found four blockers — a filename the reused writer can't produce,
missing Codex packaging, a `tier` field referenced but never defined, and no
way to place an already-enrolled student in an existing sequence — plus
several correctness gaps (a contradiction in the course-inclusion rule,
title-only skill tagging, prerequisite-unsafe year placement, uncanonicalized
profile-skill comparison, a sourcing-contract conflict with `find-courses`,
manual-only verification, and evidence hidden in frontmatter only). All are
fixed below.*

## Repo Layout (additions only)

```
.claude/skills/
├── skillpath/                          # unchanged
├── find-courses/                       # unchanged
└── college-plan/
    ├── SKILL.md                        # explicit-invocation only (writes a file)
    ├── reference/
    │   └── curriculum-research-protocol.md
    └── scripts/
        └── coverage_diff.py            # new — see Deterministic Module below
codex/skills/college-plan/
├── SKILL.md                            # thin pointer, same pattern as
│                                        # codex/skills/skillpath/SKILL.md
├── agents/
│   └── openai.yaml                     # allow_implicit_invocation: false
├── reference -> ../../../.claude/skills/college-plan/reference
└── scripts -> ../../../.claude/skills/college-plan/scripts
.agents/skills/college-plan -> ../../codex/skills/college-plan
roadmaps/
└── college-plans/                      # new, gitignored — separate from skillpath's roadmaps/report-*.md
tests/
└── test_coverage_diff.py               # new
```

**Why one new script, not zero:** the round-1 review correctly flagged that
"uncovered skills" (target-role requirements no curriculum course covers)
is a deterministic filter over two lists — this is exactly the kind of
behavior the rest of this repo puts in a tested Python module rather than
model judgment (see `skillpath`'s own `gap_state.py`/`project_planner.py`
precedent). `scripts/coverage_diff.py` is that module: a small, pure,
unit-tested function plus a thin CLI wrapper. Everything else genuinely
stays live-research synthesis (which courses exist, what year they're
typically taken, which requirements each one covers) — no algorithm to
extract there, just a reference doc governing the research judgment
(`curriculum-research-protocol.md`), same as `skillpath`'s own
`research-protocol.md`.

## Invocation

- **`/college-plan "<major>" "<target_role>" ["<target_level>"]`** in Claude
  Code, **`$college-plan "<major>" "<target_role>" ["<target_level>"]`** in
  Codex. Zero-indexed positional args: `$0` = major, `$1` = target_role,
  `$2` = optional target_level.
- **Explicit-invocation only.** Claude Code: `disable-model-invocation:
  true` in this `SKILL.md`'s frontmatter. Codex: `codex/skills/college-plan/
  agents/openai.yaml` sets `policy.allow_implicit_invocation: false` — the
  exact same two-file enforcement `skillpath` already uses, since this skill
  also writes a file to disk.
- **Path resolution — identical convention to `skillpath`, not a
  simplified one:**
  ```bash
  PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  SKILL_DIR="${CLAUDE_SKILL_DIR:-${PROJECT_ROOT}/.agents/skills/college-plan}"
  ```
  Claude Code supplies `CLAUDE_SKILL_DIR` directly. Codex discovers the
  repo-scoped symlink at `.agents/skills/college-plan`, which resolves
  through to `codex/skills/college-plan/`, whose `reference/` and
  `scripts/` entries are themselves symlinks into
  `.claude/skills/college-plan/` — there is exactly one real copy of every
  file, matching `skillpath`'s and `find-courses`'s existing packaging
  exactly. `codex/skills/college-plan/SKILL.md` is a thin pointer ("read
  `../../../.claude/skills/college-plan/SKILL.md` completely, then follow
  it"), same as the other two skills' Codex entrypoints.
- **No required prerequisite state.** Neither `profile.yaml` nor a prior
  `/skillpath` report needs to exist. If `${PROJECT_ROOT}/profile.yaml` is
  present, load it the same way `find-courses` already does (reusing
  `skillpath`'s `profile_io.py` from `${SKILL_DIR}/../skillpath/scripts/`)
  and use `location` (to localize the target-role research queries) — but
  proceed identically, just without that refinement, when it's absent.

## Learner Context (new — fixes blocker: already-enrolled students)

A freshman and a third-year student both run `/college-plan`, but a
third-year student who gets handed a fresh four-year sequence starting at
Year 1 has been given a useless report. Positional args stay at three
(major, target role, level) — cramming degree-stage detail into more
zero-indexed args doesn't scale — so Step 1 always follows with a short
**conversational intake**, the same pattern `skillpath`'s own
profile-creation flow already uses for fields that don't fit cleanly into
CLI args:

- Degree type and country/education system (e.g. "US Bachelor's," "UK
  Bachelor's (Hons)," "Canadian College Diploma") — curriculum year
  conventions differ across systems.
- Current year or semester in the program (e.g. "starting Year 1," "just
  finished Year 2, Semester 1").
- Completed and in-progress courses (free text; resolved against
  `covers_skill_ids` in Step 4 below, not stored as a canonical list).
- Expected total program length (default 4 years if the learner doesn't
  know / hasn't decided).
- Course-load or scheduling constraints (e.g. "can only take 3 courses/
  term," "co-op program with alternating work terms").

This is **not** persisted to `profile.yaml` or any new state file — it is
asked fresh each run and recorded only in that run's report frontmatter
(`learner_context`, schema below), consistent with the Out of Scope
decision below (no lifecycle tracking). A user who re-runs the skill next
term just answers the intake again with updated answers; that's an
acceptable cost for not building a second stateful profile system.
`course_sequence[]` (Step 3) places completed/in-progress courses as
`status: completed | in_progress` entries and begins the *remaining*
sequence at the learner's stated current year, never re-recommending
courses already reported done.

## Steps

1. **Parse args, run learner-context intake** (see above). Load
   `profile.yaml` opportunistically for `location`.
2. **Research target-role requirements.** Follow
   `skillpath/reference/research-protocol.md` exactly (same query patterns,
   same ≥4-postings + ≥2-practitioner-sources evidence bar, same
   `resolve-skill` resolution, same confidence scoring) to produce
   `target_requirements[]`, **including `tier`** — see "Tiering" below,
   which fixes the round-1 blocker where `tier` was referenced but never
   defined for this skill's requirements list.
3. **Research curriculum.** Follow this skill's own
   `reference/curriculum-research-protocol.md` (see below) to produce
   `course_sequence[]`: a generic, year-by-year `<major>` curriculum
   synthesized across multiple real university program pages, each course
   tagged against `target_requirements[]` via `resolve_skill`, and marked
   `completed`/`in_progress`/`upcoming` per the learner context from Step 1.
4. **Diff.** Run `scripts/coverage_diff.py` (deterministic — see below)
   over `target_requirements[]` and `course_sequence[]` to produce
   `uncovered_skills[]`: every Critical/High/Medium-tier requirement no
   `upcoming` or `in_progress` course covers. (A requirement covered only
   by an already-`completed` course is *not* uncovered — the learner
   already has it.)
5. **Supplemental resources.** For every `uncovered_skills[]` entry, invoke
   `find-courses/SKILL.md`'s existing procedure in-process (same reuse
   pattern `skillpath` Step 7 already uses, **including its existing
   sourcing contract** — see "Sourcing contract" below).
6. **Compose & save.** Build the frontmatter (schema below), render the
   body, and call `report_state.write_report()` with
   `roadmaps_dir = "${PROJECT_ROOT}/roadmaps/college-plans"`. The **filename
   is whatever `write_report()` already produces unmodified** — see
   "Filename" below, which fixes the round-1 blocker.
7. **Print the saved path** as the final response.

**Carried-over rules from `skillpath`:** never fabricate a course, source,
or resource; every claim traces to a real fetched source (with the one
documented exception in "Sourcing contract" below); be explicit about
confidence; always save the report.

## Filename (fixes blocker 1)

`report_state.write_report()` is reused **entirely unmodified** — no new
naming parameter, no `major` in the filename. It already produces
`report-<timestamp>-<report_id[:8]>-<target-slug>.md` from
`frontmatter["target_state"]`, and this spec's frontmatter schema sets
`target_state = target_role` specifically so that existing logic works
without modification. The `report-` prefix is generic and harmless here —
directory placement (`roadmaps/college-plans/`, never `roadmaps/`) is what
actually distinguishes a college-plan report from a skillpath roadmap, not
the filename prefix. `major` is not in the filename; it's in the
frontmatter and the report header, which is where a human or script
actually needs it. This keeps the "no changes to `report_state.py`"
property from the original design intact.

## Tiering (fixes blocker 3)

`skillpath/reference/research-protocol.md` deliberately does not assign
`tier` — in `skillpath`, tiering happens in `SKILL.md`'s own Step 4 (a
documented judgment call: frequency signal + centrality, capped at Medium
when `research_confidence` is low) and lives on `gap_assessments[]`, not on
`target_requirements[]`. `college-plan` has no gap-lifecycle
(`gap_assessments` doesn't exist here — see Out of Scope), so there's
nowhere else for `tier` to live: **`college-plan` assigns `tier` directly
on each `target_requirements[]` entry**, using the identical judgment rule
`skillpath` Step 4 already documents (frequency signal + centrality;
capped at Medium when that entry's own source corroboration is low) —
applied once, at research time, in this skill's Step 2, not deferred to a
later step the way `skillpath` defers it. This is called out explicitly so
a future reader doesn't go looking for a `gap_assessments`-shaped structure
that was never built for this skill.

## `reference/curriculum-research-protocol.md` (new)

- **Queries:** `"<major>" degree requirements course list`,
  `typical "<major>" curriculum by year`, `"<major>" course sequence
  recommended`, run against **at least 3 distinct universities'** own
  program/catalog pages (not aggregator sites), each opened and read via
  `WebFetch` — same "snippet never counts" rule as
  `research-protocol.md`. No current-year filter needed (curriculum
  structure is far more stable than hiring trends), but note each source's
  `accessed_at`.
- **Course-to-skill grounding (fixes correctness gap: title-only tagging).**
  A course enters `covers_skill_ids` only on the basis of its **fetched
  course description or stated learning outcomes** — never from the course
  title alone ("Data Structures" is suggestive, not evidence). Each
  `covers_skill_ids` entry records the specific source URL its coverage
  claim came from, in the same per-course `sources[]` list already in the
  schema — this is not a separate list, just a requirement that every
  coverage claim be traceable to one of those entries.
- **Inclusion threshold (fixes correctness gap: self-contradiction).** A
  course enters `course_sequence[]` **only if its substance appears at ≥2
  of the ≥3 schools consulted** (even under different course numbers at
  each). A course appearing at exactly 1 of the consulted schools is
  **excluded entirely** — noted, if useful, only as a per-source aside on
  a related course's entry, never promoted into the sequence on its own.
  This replaces the earlier draft's contradictory "single-school courses
  excluded" vs. "low-confidence single-source courses included" rule with
  one rule: 2+ schools to appear at all; confidence then scales with how
  many of the consulted schools corroborate it (2 of 3 = medium, 3+ = high).
- **Prerequisite-aware year placement (fixes correctness gap: "earliest
  year" could violate prerequisites).** Record each course's stated
  prerequisites (by name) from its source pages. Placement rule, in order:
  1. If sources state a year, and no stated prerequisite of this course is
     placed at that year or later, use the stated year.
  2. If a stated prerequisite would end up at the same year or later,
     move this course to the term immediately after its latest
     prerequisite — sources describing typical timing don't override a
     hard prerequisite chain.
  3. If sources disagree on year with no resolvable prerequisite ordering
     between the conflicting placements, or state no year at all, place
     the course in an explicit `year: "unscheduled"` bucket rendered
     separately in the report body, flagged for advisor confirmation —
     never silently guessed into a specific year.
- **Confidence scoring:** reuse `research-protocol.md`'s high/medium/low
  definitions, evaluated per curriculum claim using the 2-of-3 / 3+-of-3
  corroboration counts from the inclusion threshold above (2 corroborating
  schools = medium, 3+ = high). There is no valid "low" curriculum-course
  confidence under this threshold, because anything with only 1
  corroborating school is excluded outright, not included at low
  confidence — this is what makes the inclusion rule and the confidence
  rule consistent with each other now.
- **Explicit disclaimer, always rendered:** the report states,
  unconditionally, that this is a generic curriculum archetype synthesized
  from multiple schools' typical offerings — not any specific school's
  actual course catalog — and that exact course numbers, prerequisites, and
  availability must be confirmed against the learner's actual school and
  advisor.

## Deterministic Module: `scripts/coverage_diff.py` (new — fixes verification gap)

Pure-function library first, CLI wrapper second, same shape as every other
script in `skillpath/scripts/`:

- `compute_uncovered(target_requirements, course_sequence) -> list[dict]` —
  for each `target_requirements[]` entry with `tier in {Critical, High,
  Medium}`, check whether any `course_sequence[]` course with `status in
  {upcoming, in_progress}` lists that `skill_id` in `covers_skill_ids`. If
  none does, the requirement is uncovered. A requirement covered *only* by
  a `status: completed` course is **not** uncovered (the learner already
  has it) but also isn't re-listed as a strength anywhere new — Study Notes
  (Step 8 below) is where completed-course coverage gets surfaced.
- CLI: `coverage_diff.py compute --requirements <path.json> --sequence
  <path.json>`, prints `uncovered_skills[]` as JSON — mirrors
  `project_planner.py plan`'s CLI shape (JSON in, JSON out, no side
  effects).
- `tests/test_coverage_diff.py` covers: a requirement covered by an
  `upcoming` course (not uncovered), a requirement covered only by a
  `completed` course (not uncovered, but doesn't crash or duplicate), a
  requirement with no covering course at all (uncovered), a Low-tier
  requirement with no covering course (never listed — tier filter), and a
  requirement covered by an `in_progress` course (not uncovered).

## Sourcing contract (fixes correctness gap: conflict with `find-courses`)

Two different evidence standards apply to two different parts of this
report, and the report must not blur them:

- **`target_requirements[]`** (Step 2) and **`course_sequence[]`** (Step 3)
  are this skill's *own* research passes — both require real `WebFetch`
  reads, per `research-protocol.md` and `curriculum-research-protocol.md`
  respectively. No snippet-only sourcing here.
- **`supplemental_resources[]`** (Step 5) is produced by literally invoking
  `find-courses/SKILL.md`'s existing, unmodified procedure — which
  performs `WebSearch` only and explicitly never claims to have fetched a
  page (see `find-courses/SKILL.md`'s "Record each resource" step: "never
  claim to have opened the resource — this skill searches, it does not
  fetch pages"). `college-plan` inherits that contract as-is for this one
  section rather than overriding it, and the report body labels this
  section's sourcing standard differently from the other two (see Report
  Body, section 4) so a reader never assumes uniform rigor across the whole
  document.

## Study Notes / profile-skill canonicalization (fixes correctness gap)

When `profile.yaml` is present, Study Notes (Step 8 of the flow, body
section 5) compares the learner's `current_skills` against
`covers_skill_ids` — and must do so **canonically**, not as raw text. Reuse
`resolution.py resolve-profile-skills` (exactly as `skillpath` itself does
and as `profile-schema.md` mandates) to resolve `current_skills[].skill`
free text to `skill_id` before comparing against any course's
`covers_skill_ids`. Comparing raw `skill` text directly against canonical
IDs would silently match nothing — the exact bug class `skillpath`'s own
schema doc already calls out and fixed once; this skill must not
reintroduce it.

## Report Schema

Frontmatter (written via `report_state.write_report`, unmodified — see
Filename above):

```yaml
report_id: <uuid4>
generated_at: <UTC ISO8601 timestamp>
major: string
target_state: string          # = target_role — reused verbatim so the
                               # unmodified write_report() filename-slug
                               # logic needs no changes (see Filename)
target_level: string | null
research_confidence: high | medium | low
learner_context:
  degree_type: string
  education_system: string
  current_year_or_semester: string
  expected_program_length_years: number
  course_load_constraints: string | null
target_requirements:          # skillpath's own shape, PLUS tier (see Tiering)
  - skill_id: string
    unmapped: boolean
    category: hard | tooling | domain | soft | credential
    tier: Critical | High | Medium | Low
    frequency_signal: number
    sources: [ ... ]          # identical shape to skillpath's own field
course_sequence:
  - year: integer | "unscheduled"
    courses:
      - course_name: string    # generic title, e.g. "Data Structures"
        status: completed | in_progress | upcoming
        prerequisites: [string]        # course_name values, may be empty
        covers_skill_ids: [string]
        confidence: medium | high      # never low — see inclusion threshold
        sources:
          - url: string
            title: string
            school: string
            accessed_at: <UTC ISO8601 timestamp>
uncovered_skills:              # scripts/coverage_diff.py output, unmodified
  - skill_id: string
    tier: Critical | High | Medium | Low
supplemental_resources:        # find-courses output per uncovered_skills entry
  - skill_id: string
    resources: [ ... ]         # same shape find-courses already returns
```

## Report Body

Fixed section order, mirroring `skillpath`'s own `report-format.md` style
(plain Markdown, headers, tables where they aid scanning) — and now
surfacing research evidence directly in the body, not only in frontmatter
(fixes correctness gap: evidence was frontmatter-only in the prior draft):

1. **Header** — major, target role/level, learner context summary (degree
   type, current year), date generated, and the generic-archetype
   disclaimer (always present, not conditional).
2. **Target Role Requirements** — `target_requirements[]` grouped by tier
   (Critical first), each with a one-line citation (source title + URL) —
   this is the section the round-1 review found missing entirely.
3. **Course Sequence by Year** — `course_sequence[]` grouped by year
   (`"unscheduled"` rendered as its own final group, flagged for advisor
   confirmation), each course marked completed/in-progress/upcoming, the
   target-role skills it covers, and a citation per course (source title +
   URL) alongside it, not just in frontmatter.
4. **Skills Not Covered by a Typical Curriculum** — `uncovered_skills[]`
   with their tier, immediately followed by **Supplemental Resources** for
   each (from `find-courses`) — labeled explicitly as web-search-sourced
   recommendations, not fetched-and-verified like sections 2-3 (see
   Sourcing contract).
5. **Study Notes** — if `profile.yaml` was available, which listed courses
   the learner's canonically-resolved `current_skills` likely already
   cover (framed as "you may be able to test out of / treat as review,"
   never as a claim they should skip a required course).
6. **Next Steps** — confirm exact course numbers/prerequisites with your
   actual school's advisor/degree audit (especially anything in the
   "unscheduled" group); re-run in a future term if your major, target
   role, or progress changes (learner context is asked fresh each run, per
   the Learner Context section above).

## Privacy

`roadmaps/college-plans/` is added to `.gitignore` alongside the existing
`roadmaps/report-*.md` entry — same reasoning (generated reports reflect a
real person's academic/career plan).

## Out of Scope (v1)

- School-specific catalogs (confirmed with the user: major-based, not
  school-based).
- Tracking completed courses across runs / a tracker CSV integration — no
  lifecycle state, no `skill_confirmed` events. Learner context (including
  completed courses) is asked fresh each run, not persisted (see Learner
  Context above). A `college-plan` report is a point-in-time
  recommendation; re-running it produces a fresh one. Adding progress
  tracking is a natural fast-follow but pulls in `skillpath`'s tracker
  schema, which is scoped to *its* gap-lifecycle model — not a good fit to
  force onto a course sequence without a dedicated design pass.
- Degree-requirement satisfaction (gen-eds, credit hours, graduation
  requirements) — this tool answers "which courses get you career-ready,"
  not "which courses satisfy your degree," which is registrar/advisor
  territory.

## Verification Plan

**Automated (`pytest`):**
1. `test_coverage_diff.py` — the five cases listed under "Deterministic
   Module" above.
2. A round-trip test: build a synthetic frontmatter matching this skill's
   schema, write it via the unmodified `report_state.write_report()` into a
   tmp `roadmaps/college-plans/` directory, read it back, and confirm the
   filename/content round-trip exactly (reusing `report_state.py`'s
   existing, already-tested behavior — no new writer code to test, just
   this skill's use of it).
3. Directory-isolation test: with both a `roadmaps/report-*.md` (skillpath)
   and a `roadmaps/college-plans/report-*.md` (college-plan) file present,
   confirm `report_state.get_last_report(roadmaps_dir="roadmaps")` returns
   only the skillpath one — proving the two families can't collide via
   `skillpath`'s own diff step, without any change to that function.
4. `resolve-profile-skills` reuse: confirm Study Notes' documented
   invocation matches `resolution.py`'s actual current CLI (already
   covered by `skillpath`'s own test suite; this is a documentation-drift
   check, not new coverage).
5. Privacy: `git check-ignore -v roadmaps/college-plans/<a-generated-file>`
   confirms it's actually matched by `.gitignore`, not just absent from
   `git status`.

**Manual / end-to-end:**
6. `/college-plan "Computer Science" "Data Scientist"` for a stated
   freshman — confirm both research passes run with real `WebFetch` reads
   (inspect transcript); confirm every `course_sequence[]` course is
   corroborated at ≥2 of ≥3 real school sources (or lands in
   `"unscheduled"`, never guessed); confirm the generic-archetype
   disclaimer renders; confirm the report saves under
   `roadmaps/college-plans/` and not `roadmaps/`.
7. Same target role, but stated as a third-year student with named
   completed/in-progress courses — confirm those courses render as
   `completed`/`in_progress` and are excluded from `uncovered_skills[]`
   coverage checks in the wrong direction (i.e. still credited), and that
   the remaining sequence starts at their actual current year, not Year 1.
8. Run `/skillpath` afterward (same repo, same session) — confirm its
   `get_last_report()` / Since-Last-Report diff is unaffected (covered
   automatically by test 3, re-confirmed live here).
9. Run with a `profile.yaml` present listing `current_skills` — confirm
   Study Notes correctly cross-references them via canonical `skill_id`
   resolution, not raw text; run again with no `profile.yaml` — confirm the
   section is omitted, no crash, no placeholder text.
10. Confirm `/college-plan` does not fire from ambient conversation in
    Claude Code, and confirm `$college-plan` likewise requires explicit
    invocation in Codex (`allow_implicit_invocation: false` respected).
11. Confirm a prerequisite conflict in curriculum sources (construct one via
    a targeted search, or synthetically) correctly triggers the "move to
    the term after the prerequisite" rule rather than the source-stated
    year, and that an unresolvable disagreement lands in `"unscheduled"`.

## Critical Files to Create

- `.claude/skills/college-plan/SKILL.md`
- `.claude/skills/college-plan/reference/curriculum-research-protocol.md`
- `.claude/skills/college-plan/scripts/coverage_diff.py`
- `codex/skills/college-plan/SKILL.md`
- `codex/skills/college-plan/agents/openai.yaml`
- `codex/skills/college-plan/reference` (symlink)
- `codex/skills/college-plan/scripts` (symlink)
- `.agents/skills/college-plan` (symlink)
- `tests/test_coverage_diff.py`
- `.gitignore` — add `roadmaps/college-plans/`
