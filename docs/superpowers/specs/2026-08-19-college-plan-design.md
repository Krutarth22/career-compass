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
curriculum-research pass with its own deterministic matching/sequencing/
diff script, and a course-sequencing report. It does not require a prior
`/skillpath` run or an existing `profile.yaml`; both are used
opportunistically when present, never required.

*Revision note: this is the fifth pass.* Round 1 found four blockers
(filename, Codex packaging, undefined `tier`, no already-enrolled-student
handling). Round 2 found the round-1 fix for that last point was itself
incomplete (a self-contradictory "covered" definition, missing schema
fields, unspecified course matching, sequencing left as prose, and
collected-but-unused learner constraints). Round 3 found: the `## Steps`
section was dropped entirely while still being referenced throughout;
`self_reported_courses` used a different coverage field than
`compute_uncovered()` expected; the proposed matching approach couldn't
actually produce an ambiguous-vs-unmatched distinction or handle course
codes; program-length clamping could silently violate prerequisite order;
`source_stated_year: None` conflated "no year stated" with "sources
disagree"; and an unmatched self-reported course was granted coverage
credit from its title alone, contradicting this same spec's own
no-title-only-coverage rule. All six were fixed in pass four. Round 4
found two remaining implementation-contract gaps: `match_completed_courses`
lost each input course's `completed`/`in_progress` status on the way to its
result, and a course whose prerequisite is itself `"unscheduled"` (from
source disagreement) had no defined behavior for its own placement — plus
one unreachable branch in the clamping logic. All three are fixed below.

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
        └── curriculum_planner.py       # new — see Deterministic Module below
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
└── test_curriculum_planner.py          # new
```

**Why one new script, not zero:** matching a learner's stated course
against the synthesized archetype, placing courses in a prerequisite-safe
year, and computing which requirements remain uncovered are all
deterministic — pure functions over data, not judgment calls — so they
belong in a small, tested Python module, the same way `skillpath` puts
gap-lifecycle and project-sequencing logic in `gap_state.py` /
`project_planner.py` rather than leaving it to prose. `curriculum_planner.py`
holds all three. Everything else genuinely stays live-research synthesis —
no algorithm to extract there, just a reference doc governing that
judgment (`curriculum-research-protocol.md`), the same relationship
`skillpath` has with its own `research-protocol.md`.

## Invocation

- **`/college-plan "<major>" "<target_role>" ["<target_level>"]`** in Claude
  Code, **`$college-plan "<major>" "<target_role>" ["<target_level>"]`** in
  Codex. Zero-indexed positional args: `$0` = major, `$1` = target_role,
  `$2` = optional target_level. **When `$2` is omitted, `target_level`
  defaults to `"entry-level / new graduate"`**, recorded in the frontmatter
  with `target_level_was_defaulted: true` so a reader can see it was
  inferred, not stated.
- **Explicit-invocation only.** Claude Code: `disable-model-invocation:
  true` in this `SKILL.md`'s frontmatter. Codex:
  `codex/skills/college-plan/agents/openai.yaml` sets
  `policy.allow_implicit_invocation: false` — the same two-file
  enforcement `skillpath` already uses, since this skill also writes a
  file to disk.
- **Path resolution — identical convention to `skillpath`:**
  ```bash
  PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  SKILL_DIR="${CLAUDE_SKILL_DIR:-${PROJECT_ROOT}/.agents/skills/college-plan}"
  ```
  Claude Code supplies `CLAUDE_SKILL_DIR` directly. Codex discovers the
  repo-scoped symlink at `.agents/skills/college-plan`, resolving through
  to `codex/skills/college-plan/`, whose `reference/` and `scripts/`
  entries are themselves symlinks into `.claude/skills/college-plan/` —
  exactly one real copy of every file, matching `skillpath`'s and
  `find-courses`'s existing packaging.
- **No required prerequisite state.** Neither `profile.yaml` nor a prior
  `/skillpath` report needs to exist. If `${PROJECT_ROOT}/profile.yaml` is
  present, load it the same way `find-courses` already does and use
  `location` to localize research queries — otherwise proceed identically
  without that refinement.

## Steps (restored — round 3 finding: this section was dropped while still
being referenced throughout the rest of the document)

1. **Parse args.** Apply the `target_level` default above if `$2` is
   absent.
2. **Learner-context intake.** Conversational, per "Learner Context" below:
   degree type, education system, `current_year_number` (asked directly as
   an integer), `current_year_or_semester` (free-text display string),
   `expected_program_length_years`, `course_load_constraints`,
   `completed_courses`/`in_progress_courses` (free text lists). Load
   `profile.yaml` opportunistically for `location`.
3. **Research target-role requirements.** Follow
   `skillpath/reference/research-protocol.md` exactly to produce
   `target_requirements[]`, each with `tier` and per-requirement
   `confidence` (this skill assigns both directly — see "Tiering" below,
   since `research-protocol.md` itself defines neither).
4. **Research curriculum.** Follow this skill's own
   `reference/curriculum-research-protocol.md` to produce raw
   `course_sequence[]` course records (`course_name`, `aliases` —
   real course codes seen at consulted schools, `source_years`,
   `prerequisites`, `covers_skill_ids`, `coverage_evidence`) and
   `electives[]` (single-school, target-aligned courses).
5. **Match learner courses to the archetype.** Build one combined input
   list tagging each of `completed_courses`/`in_progress_courses` from
   Step 2 with its own status (`[{course_name, status: completed |
   in_progress}]`), and run `curriculum_planner.match_completed_courses()`
   (deterministic — see below) once against that list and the raw
   `course_sequence[]` from Step 4. For each `ambiguous` result, ask the
   learner once, conversationally, which candidate they mean. Each
   `unmatched` result becomes a `self_reported_courses[]` entry (schema
   below), with the same `status` it was tagged with — never discarded,
   never guessed into a match.
6. **Sequence.** Run `curriculum_planner.sequence_courses()`
   (deterministic — see below) over the matched/updated `course_sequence[]`
   using `expected_program_length_years` and `current_year_number` from
   Step 2, producing each course's final `year` (or `"unscheduled"`) plus
   any `compressed_from_source_year`, `behind_typical_schedule`, or
   `infeasible_within_program_length` flags.
7. **Diff.** Run `curriculum_planner.compute_uncovered()` (deterministic —
   see below) over `target_requirements[]`, the sequenced
   `course_sequence[]`, and `self_reported_courses[]` to produce
   `uncovered_skills[]`.
8. **Supplemental resources.** For every `uncovered_skills[]` entry, invoke
   `find-courses/SKILL.md`'s existing procedure in-process, inheriting its
   existing search-only sourcing contract (see "Sourcing contract" below).
9. **Apply course-load/co-op advisories.** Per "Applying course-load and
   co-op constraints" below — presentation-only, does not alter any
   `year`.
10. **Compose & save.** Build the frontmatter (schema below), render the
    body, and call `report_state.write_report()` — **entirely
    unmodified** — with `roadmaps_dir =
    "${PROJECT_ROOT}/roadmaps/college-plans"`. The filename is whatever
    `write_report()` already produces from `target_state` (set to
    `target_role`); no new naming logic.
11. **Print the saved path** as the final response.

**Carried-over rules from `skillpath`:** never fabricate a course, source,
or resource; every research-pass claim traces to a real fetched source
(with the one documented `find-courses` exception); be explicit about
confidence; always save the report.

## Learner Context

Collected in Step 2, stored in `learner_context` (schema below), **not**
persisted to `profile.yaml` or any new state file — asked fresh each run
(see Out of Scope). Fields and how each is actually used downstream (round
2 finding: several of these were collected but never applied — fixed):

- `degree_type` / `education_system` — used to **scope which schools count
  toward corroboration** in Step 4's curriculum research (see
  curriculum-research-protocol.md): mixing, say, a 3-year UK curriculum
  with a 4-year US one into one "generic" archetype would be broken, not
  useful.
- `current_year_number` (integer, asked directly — not parsed from free
  text) — the "remaining sequence starts here" cutoff `sequence_courses()`
  uses for behind-schedule reclassification (see below).
  `current_year_or_semester` is a separate free-text display string for
  the report header only; no code reads it.
- `completed_courses` / `in_progress_courses` — free text exactly as the
  learner names them, resolved against the archetype in Step 5 (never
  directly against `covers_skill_ids` — see "Matching learner courses to
  the archetype" below).
- `expected_program_length_years` — the number of year-buckets
  `sequence_courses()` targets; default 4 if unknown.
- `course_load_constraints` — free text, applied only as a post-sequencing
  advisory (Step 9), never as an input to placement itself.

## Matching learner courses to the archetype (fixes round-3 gap 3)

**Round-3 finding:** the prior draft proposed reusing `resolution.py`'s
private `_match_by_phrase()`, which returns a single owner or `None` — it
cannot represent "ambiguous" (multiple candidates) separately from
"unmatched" (zero candidates), and has no notion of course codes. Fixed
with a new, purpose-built function:

- **Course codes as data, not guesswork.** Step 4's curriculum research
  already reads each consulted school's course page for other reasons; it
  additionally records that school's actual course code (e.g. `"CS
  2110"`) into the synthesized course's `aliases: [string]` list, alongside
  the generic `course_name` (e.g. `"Data Structures"`). This is what lets
  a learner who types `"CS 2110"` match the generic entry — matching
  against `course_name` alone could never do this.
- **`match_completed_courses(learner_courses, course_sequence)`** (new,
  public, in `curriculum_planner.py` — not a reuse of `resolution.py`'s
  private helper, though it reuses `resolution.py`'s `_normalize_key`
  normalization directly by import, since duplicating that exact
  normalization logic would only risk drift). `learner_courses` is
  `[{"course_name": str, "status": "completed" | "in_progress"}]` — status
  travels alongside each entry through the whole function so it survives
  into the result (round-4 finding: an earlier draft's signature carried
  only bare names and silently lost this).
  1. Normalize the learner's stated `course_name` and every candidate
     string (each archetype course's `course_name` plus all its
     `aliases`) the same way.
  2. **Exact normalized match** against any single course's candidate
     strings → that course, done.
  3. Else, **bounded whole-word phrase containment** (same
     `MIN_PHRASE_TOKEN_LEN` guard `resolve_skill` already uses, to stop
     short-token nonsense matches) in either direction against every
     course's candidate strings → collect the **distinct set of courses**
     with any matching candidate string.
  4. **Result, explicitly one of three shapes** (this is what the private
     helper couldn't do): zero distinct courses → `unmatched`; exactly one
     → `matched`; two or more → `ambiguous` **with the actual candidate
     course names returned**, not just `None`.
  - Returns `{"matched": [{"learner_name": str, "course_name": str,
    "status": str}], "ambiguous": [{"learner_name": str, "candidates":
    [str], "status": str}], "unmatched": [{"learner_name": str, "status":
    str}]}` — every entry in every bucket carries the `status` it was
    given, so Step 5 can apply it to `course_sequence[]`/
    `self_reported_courses[]` without re-deriving or re-asking for it.
    `ambiguous`/`unmatched` are surfaced to the conversational flow
    (Step 5) — never resolved by guessing inside this function.
- **Unmatched → `self_reported_courses[]`**, not discarded, carrying the
  same `status` (schema below).

## Sequencing, coverage, and the fixes that make them internally consistent

**"Covered" definition (unchanged from round 2, still correct):** a
`target_requirements[]` entry is covered if *any* `course_sequence[]` or
`self_reported_courses[]` entry with `status in {completed, in_progress,
upcoming}` lists that `skill_id` in `covers_skill_ids` — all three
statuses count; distinguishing "already have it" from "will have it" is a
**report-body presentation** detail, not a computation one.

**Round-3 finding: schema mismatch.** The prior draft's
`self_reported_courses[]` entries carried a single `skill_id`, while
`compute_uncovered()` was specified to read `covers_skill_ids` (a list) —
incompatible shapes. **Fixed: `self_reported_courses[]` entries use
`covers_skill_ids: [string]` for consistency with `course_sequence[]`,
full stop** — one representation, used everywhere `compute_uncovered()`
reads coverage.

**Round-3 finding: title-only coverage credit contradiction.** The prior
draft granted a `self_reported_courses[]` entry coverage credit by running
`resolve_skill` on its bare title — directly contradicting this spec's own
curriculum-research rule that a course never gets `covers_skill_ids` from
its title alone (only from a fetched description/learning-outcomes). There
is no fetchable source for a self-reported course, so title-based
inference can't be grounded the way `course_sequence[]`/`electives[]`
entries are. **Fixed: `self_reported_courses[]` entries always get
`covers_skill_ids: []` in v1** — they're listed for the learner's own
record (so their completed coursework isn't silently omitted from the
report) but contribute **no** coverage credit, and the report body says so
explicitly, pointing at `/skillpath confirm` as the existing, correctly-
evidenced mechanism for claiming a specific skill is actually covered by
something outside the generic archetype.

**Round-3 finding: `source_stated_year: None` was overloaded.** The prior
draft used a single optional field for both "no source stated a year" and
"sources disagree on the year" — but those two cases have different
specified behavior (default-and-place vs. `"unscheduled"`), so collapsing
them into one `None` value made the behavior ambiguous. **Fixed:** each
course carries **`source_years: [integer]`** — every year any consulted
source stated (possibly empty, possibly with duplicates or genuinely
different values), not a single optional value. `sequence_courses()`
branches on it explicitly:
- `len(set(source_years)) == 0` (no source stated a year) → treated as
  unspecified; placement is driven entirely by the prerequisite floor (see
  below), defaulting to year 1 if there are no prerequisites either.
- `len(set(source_years)) == 1` (sources agree, or only one stated a year)
  → that value is the starting point for the prerequisite floor below.
- `len(set(source_years)) > 1` (genuine disagreement) → **always
  `"unscheduled"`**, flagged `source_disagreement: true`. This case is
  never arbitrated by prerequisite math — conflicting explicit source
  claims aren't something a placement algorithm should silently pick a
  winner between.

**Round-3 finding: program-length clamping could violate prerequisite
order.** The prior draft clamped any `final_year > program_length_years`
straight to `program_length_years`, which could push a course to the same
year as (or earlier than) its own prerequisite if that prerequisite had
itself already been clamped to the final year. **Fixed — clamping only
applies when it doesn't break prerequisite order; otherwise the course is
infeasible, not silently misordered:**

Courses are processed in prerequisite-topological order throughout, so
every prerequisite's `final_year` is already resolved (to an integer or to
`"unscheduled"`) by the time a dependent course is placed.

**Unscheduled-prerequisite propagation (round-4 finding: previously
undefined).** Before computing `prereq_floor`, check each prerequisite's
already-resolved `final_year`: if **any** prerequisite's `final_year` is
`"unscheduled"` (whether from `source_disagreement` or from its own
`infeasible_within_program_length`), the dependent course is immediately
`final_year = "unscheduled"` too, flagged
`blocked_by_unscheduled_prerequisite: true` — `max()` over a set containing
a non-numeric `"unscheduled"` value is undefined, and a course can't be
meaningfully placed before a prerequisite that itself has no placement.
This check runs first and short-circuits the rest of this section for that
course; source-disagreement placement (above) and infeasibility placement
(below) both therefore propagate forward through every course that
depends on them, transitively, since each course's own resolved
`final_year` is what the next dependent checks.

For a course with `len(set(source_years)) <= 1` (i.e. not the
disagreement case above) and no unscheduled prerequisite:
1. `prereq_floor = 1 + max(final_year of each prerequisite, default 0)`
   (a cycle among prerequisites is a data error, detected and flagged, not
   looped on).
2. `natural_year = max(source_years[0] if present else 1, prereq_floor)`.
3. If `natural_year <= program_length_years`: `final_year =
   natural_year`. Since `natural_year` is a `max()` that includes
   `source_years[0]` as one of its terms, it can never be *less* than
   `source_years[0]` — so `compressed_from_source_year` is set only when
   `natural_year > source_years[0]` (i.e. the prerequisite floor, not the
   program-length clamp, pushed it later than the source stated; equality
   means no compression happened).
4. If `natural_year > program_length_years`:
   - If `prereq_floor <= program_length_years` (there's still room to
     place it without breaking prerequisite order): `final_year =
     program_length_years`, flagged `compressed_from_source_year:
     <source_years[0]>`.
   - If `prereq_floor > program_length_years` (even the earliest
     prerequisite-safe slot doesn't fit): `final_year = "unscheduled"`,
     flagged `infeasible_within_program_length: true` — the report states
     plainly that this course's prerequisite chain requires more years
     than the stated program length allows, rather than silently
     misordering it. (This is the case that can propagate forward per the
     unscheduled-prerequisite rule above.)
5. **Behind-schedule reclassification** (unchanged from round 2): if the
   resulting `final_year < current_year_number` and the course was **not**
   matched to a `completed`/`in_progress` entry in Step 5, it is placed at
   `current_year_number` instead and flagged `behind_typical_schedule:
   true`.

**Year-level, not term-level, placement** remains a deliberate
simplification (unchanged from round 2) — the archetype already
approximates across schools with different term systems; course-load
advisories (Step 9) are where within-year spreading gets surfaced instead
of a `term` field implying more precision than the research supports.

## Deterministic Module: `scripts/curriculum_planner.py`

Pure-function library first, CLI wrapper second, matching every other
script's shape in `skillpath/scripts/`. Three functions, per the sections
above:

1. **`match_completed_courses(learner_courses, course_sequence) -> dict`**
   — see "Matching learner courses to the archetype."
2. **`sequence_courses(courses, program_length_years, current_year) ->
   list[dict]`** — see "Sequencing, coverage, and the fixes..." above for
   the exact branching on `source_years`, unscheduled-prerequisite
   propagation, prerequisite floor, clamping vs. infeasibility, and
   behind-schedule reclassification. Processes courses in
   prerequisite-topological order; raises/flags a cycle rather than
   looping.
3. **`compute_uncovered(target_requirements, course_sequence,
   self_reported_courses) -> list[dict]`** — the single "covered"
   definition above, across all three statuses, reading
   `covers_skill_ids` uniformly from both `course_sequence[]` and
   `self_reported_courses[]` (the latter always `[]` in v1, per the
   title-only-coverage fix — included for schema uniformity and so the
   function needs no special-casing per source list). Tier-filters to
   `Critical`/`High`/`Medium`.

CLI: `curriculum_planner.py match --learner-courses <path.json>
--sequence <path.json>`, `curriculum_planner.py sequence --courses
<path.json> --program-length N --current-year N`,
`curriculum_planner.py diff --requirements <path.json> --sequence
<path.json> --self-reported <path.json>` — JSON in/out, no side effects.

`tests/test_curriculum_planner.py` covers, at minimum:
- Matching: exact match, course-code alias match, ambiguous (two distinct
  courses, candidates returned), unmatched (empty), confirming these are
  three distinct result shapes, not two.
- Sequencing: a straight-line prerequisite chain producing correct
  placement; a cycle (raises/flags, doesn't loop); `source_years` empty
  (unspecified, prereq-floor-driven); `source_years` single-valued;
  `source_years` multi-valued (`"unscheduled"`, `source_disagreement:
  true`, regardless of any prerequisite relationship); clamping that
  succeeds without violating prerequisite order
  (`compressed_from_source_year` set); clamping that would violate order →
  `infeasible_within_program_length: true` instead of a silently-wrong
  year; a required course computed earlier than `current_year` and not
  matched to completed/in-progress → placed at `current_year` with
  `behind_typical_schedule: true`; a course whose prerequisite resolved to
  `"unscheduled"` (via `source_disagreement`) → the dependent course is
  also `"unscheduled"` with `blocked_by_unscheduled_prerequisite: true`;
  a two-hop chain where the propagation carries through a second dependent
  course as well (transitivity).
- Coverage: each of the three statuses individually covers a requirement;
  a `self_reported_courses[]` entry (with its always-empty
  `covers_skill_ids`) contributes nothing; a Low-tier requirement never
  appears in `uncovered_skills[]` regardless of coverage.

## `reference/curriculum-research-protocol.md`

- **Queries**, scoped to the learner's stated `education_system`:
  `"<major>" degree requirements course list <education system's country/
  system>`, `typical "<major>" curriculum by year <education system>`,
  `"<major>" course sequence recommended`, run against **at least 3
  distinct universities within that same education system**, each opened
  and read via `WebFetch` — same "snippet never counts" rule as
  `research-protocol.md`. If the learner's education system is unusual/
  unclear, note this explicitly and accept a wider, lower-confidence pool
  rather than blocking.
- **Course codes, recorded as `aliases`.** While reading each school's
  course page, record its actual course code alongside the generic title
  — this is what Step 5's matching needs (see above), gathered at zero
  extra research cost since the page is already being read.
- **Course-to-skill grounding.** A course enters `covers_skill_ids` only
  from its **fetched course description or stated learning outcomes** —
  never the title alone. Each course carries `coverage_evidence:
  [{skill_id, source_urls: [string]}]`, one entry per skill it's tagged
  with, so every specific claim is traceable to the source that backs it.
- **Inclusion threshold.** A course enters `course_sequence[]` only if its
  substance appears at **≥2 of the ≥3 same-education-system schools
  consulted** (even under different course codes at each); confidence is
  `medium` at exactly 2, `high` at 3+. A course appearing at exactly 1
  school is **excluded from `course_sequence[]`** but not discarded — see
  "Target-aligned electives."
- **Target-aligned electives.** A single-school course whose
  `covers_skill_ids` (via the same fetched-description grounding rule)
  includes a Critical/High-tier `target_requirements[]` skill_id is
  recorded in `electives[]` — school name, course name, what it covers,
  its evidence — explicitly labeled single-school so it's never confused
  with the generic archetype.
- **Explicit disclaimer, always rendered:** this is a generic curriculum
  archetype synthesized from multiple schools within the learner's stated
  education system — not any specific school's actual course catalog —
  and exact course numbers, prerequisites, and availability must be
  confirmed against the learner's actual school and advisor.

## Applying course-load and co-op constraints

Applied in Step 9, as a **post-sequencing advisory check** only —
`sequence_courses()` itself never reads `course_load_constraints`:

- If `course_load_constraints` states a per-term course cap and a year's
  course count exceeds roughly double that (implying more than 2 terms'
  worth landed in one year), the report adds an advisory note for that
  year: consider spreading across a summer term or extending the
  timeline.
- If `course_load_constraints` mentions co-op/alternating work terms, the
  report adds one general advisory note: this sequence models academic
  years only, not co-op gaps — treat "Year N" as "the Nth academic term
  block" and confirm actual calendar placement with a co-op coordinator.
- Neither check changes any `final_year` — advisory only.

## Tiering and per-requirement confidence

`college-plan` assigns `tier` directly on each `target_requirements[]`
entry in Step 3, using the identical judgment rule `skillpath`'s Step 4
documents (frequency signal + centrality; capped at Medium when evidence
is thin) — `skillpath`'s own `research-protocol.md` defines neither `tier`
nor per-requirement confidence, since in `skillpath` those live on
`gap_assessments[]`, which `college-plan` has no equivalent of. Each
`target_requirements[]` entry also carries its own `confidence: high |
medium | low`; the report-level `research_confidence` remains a roll-up
summary, not the only granularity available.

## Sourcing contract

- **`target_requirements[]`** and **`course_sequence[]`**/**`electives[]`**
  require real `WebFetch` reads — no snippet-only sourcing.
- **`supplemental_resources[]`** is produced by invoking
  `find-courses/SKILL.md`'s existing, unmodified procedure —
  `WebSearch`-only, never claiming to have fetched a page.
  `college-plan` inherits that contract as-is for this one section, and
  the report body labels it differently from the fetch-backed sections.

## Study Notes / profile-skill canonicalization

When `profile.yaml` is present, Study Notes compares the learner's
`current_skills` against `covers_skill_ids` **canonically**: reuse
`resolution.py resolve-profile-skills` (exactly as `skillpath` itself
does) to resolve `current_skills[].skill` free text to `skill_id` before
comparing — never compare raw `skill` text directly.

## Report Schema

```yaml
report_id: <uuid4>
generated_at: <UTC ISO8601 timestamp>
major: string
target_state: string          # = target_role — write_report()'s existing
                               # filename-slug logic needs no changes
target_level: string          # explicit value, or the entry-level default
target_level_was_defaulted: boolean
research_confidence: high | medium | low   # roll-up; see per-entry confidence
learner_context:
  degree_type: string
  education_system: string
  current_year_number: integer
  current_year_or_semester: string      # display only
  expected_program_length_years: number
  course_load_constraints: string | null
  completed_courses: [string]           # as stated by the learner
  in_progress_courses: [string]         # as stated by the learner
target_requirements:
  - skill_id: string
    unmapped: boolean
    category: hard | tooling | domain | soft | credential
    tier: Critical | High | Medium | Low
    confidence: high | medium | low
    frequency_signal: number
    sources: [ ... ]                    # identical shape to skillpath's own field
course_sequence:
  - year: integer | "unscheduled"
    courses:
      - course_name: string
        aliases: [string]               # real course codes seen at consulted schools
        status: completed | in_progress | upcoming
        prerequisites: [string]
        source_years: [integer]         # every year any source stated; see Sequencing
        covers_skill_ids: [string]
        coverage_evidence:
          - skill_id: string
            source_urls: [string]
        confidence: medium | high        # never low — see inclusion threshold
        compressed_from_source_year: integer | null
        behind_typical_schedule: boolean
        infeasible_within_program_length: boolean
        source_disagreement: boolean
        blocked_by_unscheduled_prerequisite: boolean
        sources:
          - url: string
            title: string
            school: string
            accessed_at: <UTC ISO8601 timestamp>
electives:
  - course_name: string
    school: string
    covers_skill_ids: [string]
    coverage_evidence: [ ... ]
    sources: [ ... ]
self_reported_courses:
  - course_name: string          # as stated by the learner
    status: completed | in_progress
    covers_skill_ids: []         # always empty in v1 — see title-only-coverage fix
uncovered_skills:
  - skill_id: string
    tier: Critical | High | Medium | Low
supplemental_resources:
  - skill_id: string
    resources: [ ... ]           # same shape find-courses already returns
```

## Report Body

Fixed section order, mirroring `skillpath`'s own `report-format.md` style:

1. **Header** — major, target role/level (noting if defaulted), learner
   context summary, date generated, and the generic-archetype disclaimer
   (always present).
2. **Target Role Requirements** — `target_requirements[]` grouped by tier
   (Critical first), each with its own confidence and a one-line citation.
3. **Course Sequence by Year** — `course_sequence[]` grouped by year
   (`"unscheduled"` as its own final group), each course marked
   completed/in-progress/upcoming, skills covered with citations, and any
   `compressed_from_source_year` / `behind_typical_schedule` /
   `infeasible_within_program_length` / `source_disagreement` /
   `blocked_by_unscheduled_prerequisite` flag rendered as a plain-language
   note. Course-load/co-op advisories render per-year where triggered.
4. **Electives Worth Considering** — `electives[]`, labeled single-school.
5. **Skills Not Covered by a Typical Curriculum** — `uncovered_skills[]`
   with tier, immediately followed by **Supplemental Resources** (from
   `find-courses`), labeled web-search-sourced.
6. **Study Notes** — canonically-resolved `current_skills` overlap (if
   `profile.yaml` present) and `self_reported_courses[]` listed plainly as
   "reported, but not counted toward requirement coverage — use `/skillpath
   confirm` if you can back a specific skill claim with evidence."
7. **Next Steps** — confirm exact course numbers/prerequisites with an
   actual advisor/degree audit (especially "unscheduled" and
   `electives[]` entries); re-run in a future term if major, target role,
   or progress changes.

## Privacy

`roadmaps/college-plans/` is added to `.gitignore` alongside the existing
`roadmaps/report-*.md` entry.

## Out of Scope (v1)

- School-specific catalogs (major-based, not school-based).
- Tracking completed courses across runs / a tracker CSV integration — no
  lifecycle state; learner context is asked fresh each run.
- Full term-by-term scheduling (year-level placement only; course-load/
  co-op constraints are advisory notes, not a scheduling optimizer).
- Degree-requirement satisfaction (gen-eds, credit hours, graduation
  requirements).
- Automatic coverage credit for `self_reported_courses[]` — always
  `covers_skill_ids: []` in v1 (title-only inference is explicitly
  disallowed by this spec's own grounding rule, and there's no fetchable
  source for a self-reported course); the report points at `/skillpath
  confirm` as the existing, correctly-evidenced path for claiming a
  specific skill some other way.

## Verification Plan

**Automated (`pytest`):**
1. `test_curriculum_planner.py` — all cases under "Deterministic Module"
   above.
2. A round-trip test: synthetic frontmatter matching this skill's schema,
   written via the unmodified `report_state.write_report()` into a tmp
   `roadmaps/college-plans/` directory, read back, content round-trips
   exactly.
3. Directory-isolation test: with both a `roadmaps/report-*.md`
   (skillpath) and a `roadmaps/college-plans/report-*.md` (college-plan)
   file present, confirm `report_state.get_last_report(roadmaps_dir=
   "roadmaps")` returns only the skillpath one.
4. `resolve-profile-skills` reuse: confirm Study Notes' documented
   invocation matches `resolution.py`'s actual current CLI.
5. Codex packaging integrity: confirm `codex/skills/college-plan/reference`
   and `.../scripts` resolve, via the symlink chain, to the exact same
   files as `.claude/skills/college-plan/reference`/`scripts`, and that
   `.agents/skills/college-plan` resolves to `codex/skills/college-plan`.
6. Privacy: `git check-ignore -v roadmaps/college-plans/<a-generated-file>`
   confirms it's actually matched by `.gitignore`.

**Manual / end-to-end:**
7. `/college-plan "Computer Science" "Data Scientist"` for a stated
   freshman (`current_year_number: 1`, no completed courses) — confirm
   both research passes use real `WebFetch` reads; confirm
   `course_sequence[]` courses are corroborated at ≥2 of ≥3
   same-education-system school sources (or land in `"unscheduled"`);
   confirm the disclaimer renders; confirm the report saves under
   `roadmaps/college-plans/`.
8. Same target role, stated as a third-year student with named
   completed/in-progress courses, including one stated by course code
   (exercising `aliases` matching), one that won't match any archetype
   course (exercising `self_reported_courses[]`), and one ambiguous name
   (exercising conversational disambiguation) — confirm correct `status`
   assignment, the remaining sequence starting at Year 3, and a
   required-but-not-yet-taken course correctly flagging
   `behind_typical_schedule`.
9. State a 3-year program length against curriculum sources describing a
   4-year sequence, including at least one course whose prerequisite chain
   alone requires 4 years — confirm the compressible courses get
   `compressed_from_source_year` while the truly-too-long chain gets
   `infeasible_within_program_length: true` instead of a silently-wrong
   year.
10. Construct a course with genuinely conflicting `source_years` — confirm
    `"unscheduled"` + `source_disagreement: true`, regardless of any
    prerequisite relationship.
11. State `course_load_constraints: "max 3 courses/term"` against a year
    with 6+ courses — confirm the advisory note renders and no
    `final_year` changes.
12. Run `/skillpath` afterward (same repo, same session) — confirm its
    diff step is unaffected (covered by test 3, re-confirmed live here).
13. Run with and without `profile.yaml` present — confirm Study Notes
    behaves correctly in both cases via canonical `skill_id` resolution.
14. Confirm `/college-plan` does not fire from ambient conversation in
    Claude Code, and `$college-plan` requires explicit invocation in
    Codex.

## Critical Files to Create

- `.claude/skills/college-plan/SKILL.md`
- `.claude/skills/college-plan/reference/curriculum-research-protocol.md`
- `.claude/skills/college-plan/scripts/curriculum_planner.py`
- `codex/skills/college-plan/SKILL.md`
- `codex/skills/college-plan/agents/openai.yaml`
- `codex/skills/college-plan/reference` (symlink)
- `codex/skills/college-plan/scripts` (symlink)
- `.agents/skills/college-plan` (symlink)
- `tests/test_curriculum_planner.py`
- `.gitignore` — add `roadmaps/college-plans/`
