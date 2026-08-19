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
curriculum-research pass with its own deterministic sequencing/diff script,
and a course-sequencing report. It does not require a prior `/skillpath`
run or an existing `profile.yaml`; both are used opportunistically when
present, never required.

*Revision note: this is the third pass. Round 1 found four blockers — a
filename the reused writer can't produce, missing Codex packaging, a
`tier` field referenced but never defined, and no way to place an
already-enrolled student. Round 2 found the fix for that last point was
itself incomplete — a self-contradictory "covered" definition, missing
schema fields for completed/in-progress courses, unspecified course-name
matching, prerequisite sequencing left as prose instead of tested code, and
captured learner constraints (education system, program length,
course-load, co-op) that were collected but never actually used. All are
fixed below, plus the smaller improvements from round 2 (per-requirement
confidence, explicit coverage evidence, a target-level default, Codex
verification checks, and a lane for valuable single-school electives).*

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

**Why one new script, not zero:** "uncovered skills," "which archetype
course does this learner's completed course actually refer to," and
"what year does prerequisite-safe placement put each course in" are all
deterministic — pure functions over data, not judgment calls — so they
belong in a small, tested Python module, the same way `skillpath` puts
gap-lifecycle and project-sequencing logic in `gap_state.py` /
`project_planner.py` rather than leaving it to prose. `curriculum_planner.py`
holds all three. Everything else genuinely stays live-research synthesis
(which courses exist, what year sources say they're typically taken, which
requirements each one covers) — no algorithm to extract there, just a
reference doc governing that judgment (`curriculum-research-protocol.md`),
same relationship `skillpath` has with its own `research-protocol.md`.

## Invocation

- **`/college-plan "<major>" "<target_role>" ["<target_level>"]`** in Claude
  Code, **`$college-plan "<major>" "<target_role>" ["<target_level>"]`** in
  Codex. Zero-indexed positional args: `$0` = major, `$1` = target_role,
  `$2` = optional target_level. **When `$2` is omitted, `target_level`
  defaults to `"entry-level / new graduate"`** rather than being left null —
  a `college-plan` user is, by definition, not yet in the workforce, so an
  unqualified target role should research entry-level requirements, not an
  ambiguous "any seniority" mix. This default is recorded in the frontmatter
  so a reader can see it was inferred, not stated.
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

## Learner Context (fixes round-1 blocker; schema/usage fixed in round 2)

A freshman and a third-year student both run `/college-plan`, but a
third-year student handed a fresh four-year sequence starting at Year 1 has
been given a useless report. Positional args stay at three — cramming
degree-stage detail into more zero-indexed args doesn't scale — so Step 1
always follows with a short **conversational intake**, the same pattern
`skillpath`'s own profile-creation flow uses for fields that don't fit
cleanly into CLI args. This is **not** persisted to `profile.yaml` or any
new state file — asked fresh each run, recorded only in that run's report
frontmatter (`learner_context`, schema below). A user who re-runs next term
just answers again with updated values; that's an acceptable cost for not
building a second stateful profile system (see Out of Scope).

Collected fields, all stored in `learner_context` (schema below — round 2
found the original draft said completed/in-progress courses would be
stored here but never actually added them to the schema; fixed now):

- `degree_type` and `education_system` (e.g. `"US Bachelor's"`, `"UK
  Bachelor's (Hons)"`, `"Canadian College Diploma"`) — free text, but
  **used, not just displayed**: Step 3's curriculum research restricts its
  ≥3-school corroboration pool to schools within the **same stated
  education system** (see curriculum-research-protocol.md below) — mixing
  a 3-year UK curriculum with a 4-year US one into one "generic" archetype
  would produce a broken sequence, not a useful one. If the learner's
  answer is unclear or unusual (e.g. a mixed/transfer background), the
  report says so and confidence drops accordingly rather than silently
  picking one system.
- `current_year_number` — asked directly as an integer ("Which year of
  your program are you starting or currently in? 1 for incoming
  freshman."), not parsed from free text, so `curriculum_planner.py` has an
  unambiguous value to place the "remaining sequence starts here" cutoff.
  `current_year_or_semester` is *also* captured as a free-text display
  string (e.g. `"Year 2, Semester 1"`) for the report header, but the
  integer is the only value any code reads.
- `completed_courses` / `in_progress_courses` — free text lists, exactly as
  the learner names them (e.g. `"Intro to Programming"`, `"CS 2110"`).
  These are **not** resolved against `covers_skill_ids` directly (round 2
  finding) — see "Matching learner courses to the archetype" below for the
  actual matching step.
- `expected_program_length_years` — used as the number of year-buckets in
  `course_sequence[]` (see "Program length" under curriculum-research
  usage below), default 4 if the learner doesn't know/hasn't decided.
- `course_load_constraints` — free text (e.g. `"max 3 courses/term"`,
  `"co-op program, alternating work terms"`) — used as an **advisory
  check** after sequencing (see "Applying course-load and co-op
  constraints" below), not a scheduling optimizer.

## Matching learner courses to the archetype (new — fixes round-2 gap 3)

`completed_courses`/`in_progress_courses` are free text the learner typed;
`course_sequence[]` entries have a synthesized generic `course_name`. These
must be reconciled explicitly, in this order, as part of Step 4
(Sequence):

1. **Normalize** both sides the same way `resolution.py`'s
   `_normalize_key` already does (lowercase, whitespace/underscore/hyphen
   collapsed) — reusing that exact helper rather than writing a second
   normalizer.
2. **Match** a learner-stated course against archetype `course_name`
   values using the same bounded whole-word phrase containment
   `resolve_skill` already uses (`_phrase_contains`/`_match_by_phrase`),
   reused directly rather than reimplemented, since it already solves
   "avoid nonsense matches on short tokens."
3. **Unambiguous match** → the archetype course's `status` becomes
   `completed` or `in_progress` per which list it came from.
4. **Ambiguous match** (matches more than one archetype course) → ask the
   learner once, conversationally, which one they mean, the same way
   `resolve_track`'s ambiguous case is surfaced to a user rather than
   guessed.
5. **No match at all** → the course doesn't correspond to any synthesized
   archetype slot (it may be a school-specific or elective course with no
   cross-school equivalent). It is **not discarded**: record it in a new
   top-level `self_reported_courses[]` list (schema below) with its stated
   name and status. Best-effort tag it against the skill taxonomy by
   running `resolve_skill` on the course name itself; if that comes back
   `unmapped`, it's still listed (for the learner's own record) but
   contributes no coverage credit in Step 5's diff — never guessed.

## Sequencing & the "covered" definition (fixes round-2 gaps 1 and 4)

**Round-2 finding:** the prior draft's `compute_uncovered()` only checked
`course_sequence[]` entries with `status in {upcoming, in_progress}` for
coverage, then separately claimed a `completed`-only-covered requirement
was "not uncovered" — those two statements contradict each other under the
stated algorithm. Fixed by defining "covered" once, correctly:

> A `target_requirements[]` entry is **covered** if *any*
> `course_sequence[]` or `self_reported_courses[]` entry with `status in
> {completed, in_progress, upcoming}` lists that `skill_id` in its
> `covers_skill_ids` — all three statuses count. It is **uncovered** only
> if none does.

Coverage doesn't distinguish "already have it" from "will have it" for the
purposes of the diff — a requirement covered by a future course isn't a
gap either. The distinction between "already covered" and "will be covered
later" is a **presentation** detail, made in the report body (Study Notes
surfaces `completed` coverage as a strength; Course Sequence shows
`upcoming`/`in_progress` coverage in place), not a computation detail.

**Round-2 finding:** prerequisite-aware year placement was prose ("move to
the term immediately after"), not tested code, and referenced a `term`
field the schema didn't have. Fixed by (a) moving placement into a tested
function, and (b) staying at **year-level** placement rather than adding
term granularity — the archetype is already an approximation across
schools with different term systems (semester vs. quarter vs. trimester),
so a `term` field would imply more precision than the underlying research
can actually support. This is a deliberate simplification, not an
oversight — course-load advisory notes (below) are where within-year
term-spreading gets surfaced instead.

## Deterministic Module: `scripts/curriculum_planner.py` (new)

Pure-function library first, CLI wrapper second, matching every other
script's shape in `skillpath/scripts/`. Three functions:

1. **`match_completed_courses(learner_courses, course_sequence) -> dict`**
   — implements "Matching learner courses to the archetype" above.
   Returns `{matched: [{learner_name, course_name, status}], ambiguous:
   [{learner_name, candidates: [course_name]}], unmatched:
   [learner_name]}`. Ambiguous/unmatched results are surfaced to the
   conversational flow (steps 4-5 above), never resolved by guessing
   inside this function.
2. **`sequence_courses(courses, program_length_years, current_year) ->
   list[dict]`** — deterministic prerequisite-safe placement:
   - For each course (already carrying its `source_stated_year` — a single
     year if sources agree, or `None` if they don't/didn't state one — and
     its `prerequisites: [course_name]`), compute `final_year` via a
     topological pass over the prerequisite graph:
     `final_year = max(source_stated_year or 1, 1 + max(final_year of
     each prerequisite, default 0))`.
   - **Cycle detection:** a prerequisite cycle among the synthesized
     courses is a data error, not a schedule to solve — raise/flag it
     rather than looping; this is one of the required test cases.
   - **Program-length clamping:** any `final_year > program_length_years`
     is clamped to `program_length_years` and flagged
     `compressed_from_source_year: <original>` in that course's entry, so
     the report can tell the learner "sources suggest year N, but your
     stated M-year program compresses this — confirm feasibility with your
     advisor," per "Program length" below.
   - **Irreconcilable disagreement:** if sources give conflicting years for
     a course with no prerequisite relationship available to arbitrate
     between them, `final_year = "unscheduled"` instead of guessing.
   - **Behind-schedule reclassification:** if a course's computed
     `final_year < current_year` and it was **not** matched to a
     `completed`/`in_progress` entry in step 1 above, it is not silently
     dropped into a "past" year — it's placed at `current_year` instead
     and flagged `behind_typical_schedule: true`, since the learner
     evidently hasn't taken it yet regardless of when it's "typically"
     taken.
3. **`compute_uncovered(target_requirements, course_sequence,
   self_reported_courses) -> list[dict]`** — implements the single
   "covered" definition above (fixes gap 1) across all three statuses and
   both course lists (`course_sequence[]` and `self_reported_courses[]`).
   Tier-filters to `Critical`/`High`/`Medium` per the existing rule.

CLI: `curriculum_planner.py match --learner-courses <path.json>
--sequence <path.json>`, `curriculum_planner.py sequence --courses
<path.json> --program-length N --current-year N`,
`curriculum_planner.py diff --requirements <path.json> --sequence
<path.json> --self-reported <path.json>` — three subcommands, JSON in/out,
no side effects, mirroring `project_planner.py plan`'s CLI shape.

`tests/test_curriculum_planner.py` covers, at minimum: unambiguous match,
ambiguous match (returned, not resolved), no match; a straight-line
prerequisite chain producing correct year placement; a prerequisite cycle
(raises/flags, doesn't loop); program-length clamping with the
`compressed_from_source_year` flag set; a source-year disagreement with no
resolvable prerequisite → `"unscheduled"`; a required course computed
earlier than `current_year` and not matched to completed/in-progress →
placed at `current_year` with `behind_typical_schedule: true`; coverage by
each of the three statuses individually (all "not uncovered"); coverage via
a `self_reported_courses[]` entry; a Low-tier requirement never appearing
in `uncovered_skills[]` regardless of coverage.

## `reference/curriculum-research-protocol.md` (new)

- **Queries**, scoped to the learner's stated `education_system` (round-2
  fix — captured context must actually constrain the research, not just be
  displayed): `"<major>" degree requirements course list <education
  system's country/system>`, `typical "<major>" curriculum by year
  <education system>`, `"<major>" course sequence recommended`, run against
  **at least 3 distinct universities within that same education system**
  (not aggregator sites), each opened and read via `WebFetch` — same
  "snippet never counts" rule as `research-protocol.md`. If the learner's
  education system is unusual/unclear, note this explicitly and accept a
  wider, lower-confidence pool rather than blocking.
- **Course-to-skill grounding.** A course enters `covers_skill_ids` only on
  the basis of its **fetched course description or stated learning
  outcomes** — never the title alone. **Coverage evidence is recorded
  explicitly per skill** (round-2 smaller-improvement, promoted here
  because it's cheap and directly closes an auditability gap): each course
  carries `coverage_evidence: [{skill_id, source_urls: [string]}]`, one
  entry per skill it's tagged with, rather than relying on an
  undifferentiated course-level `sources[]` list to imply which source
  backed which specific claim.
- **Inclusion threshold.** A course enters `course_sequence[]` only if its
  substance appears at **≥2 of the ≥3 same-education-system schools
  consulted** (even under different course numbers at each); confidence is
  `medium` at exactly 2, `high` at 3+. A course appearing at exactly 1
  school is **excluded from `course_sequence[]`** — but is not discarded:
  see "Target-aligned electives" below (round-2 smaller-improvement,
  promoted to avoid losing genuinely valuable specialized courses).
- **Target-aligned electives (new list, not folded into
  `course_sequence[]`).** A single-school course whose `covers_skill_ids`
  (via the same fetched-description grounding rule) includes a
  Critical/High-tier `target_requirements[]` skill_id is recorded in a new
  top-level `electives[]` list — school name, course name, what it covers,
  its evidence — explicitly labeled low-corroboration/single-school so the
  report never implies it's part of the generic archetype, but the learner
  isn't deprived of a course that happens to be exactly what they need
  just because only one consulted school offers it.
- **Explicit disclaimer, always rendered:** the report states,
  unconditionally, that this is a generic curriculum archetype synthesized
  from multiple schools within the learner's stated education system — not
  any specific school's actual course catalog — and that exact course
  numbers, prerequisites, and availability must be confirmed against the
  learner's actual school and advisor.

## Applying course-load and co-op constraints (fixes round-2 gap 5)

`curriculum_planner.py` does not model term-by-term scheduling (see
"year-level placement" decision above) — `course_load_constraints` is
therefore applied as a **post-sequencing advisory check**, not an input to
the placement algorithm itself:

- After `sequence_courses()` returns, count courses per year. If
  `course_load_constraints` states a per-term course cap (e.g. "max 3
  courses/term") and a year's course count exceeds roughly double that
  (implying more than 2 terms' worth landed in one year), the report body
  adds an advisory note for that year: consider spreading these across a
  summer term or extending the timeline, and confirm with an advisor.
- If `course_load_constraints` mentions a co-op/alternating-work-term
  structure, the report adds one general advisory note (not per-year):
  this sequence models academic years only and does not account for
  co-op/work-term gaps — treat "Year N" as "the Nth academic term block,"
  and confirm actual calendar placement with your co-op coordinator.
- Neither check changes `final_year` — they only change what the report
  body says about a year that's already been computed. This keeps
  `curriculum_planner.py` a pure, easily-tested sequencing function rather
  than a full scheduling engine, which is out of scope for a v1 generic
  archetype tool.

## Tiering and per-requirement confidence

`skillpath/reference/research-protocol.md` deliberately does not assign
`tier` — in `skillpath`, tiering happens in `SKILL.md`'s own Step 4 and
lives on `gap_assessments[]`, which `college-plan` has no equivalent of.
**`college-plan` assigns `tier` directly on each `target_requirements[]`
entry**, using the identical judgment rule `skillpath` Step 4 documents
(frequency signal + centrality; capped at Medium when that entry's own
evidence is thin) — applied once, in this skill's own Step 2.

**Round-2 smaller-improvement:** the prior draft stored only a single
overall `research_confidence` for the whole report, even though tiering
explicitly reasons about each requirement's own corroboration. Each
`target_requirements[]` entry now also carries its own `confidence:
high | medium | low`, computed the same way `research-protocol.md` already
defines per-source confidence; `research_confidence` at the report level
remains a roll-up summary (worst-case or majority, documented in the
report header), not the only granularity available.

## Sourcing contract

Two different evidence standards apply to two different parts of this
report:

- **`target_requirements[]`** and **`course_sequence[]`**/**`electives[]`**
  are this skill's own research passes — both require real `WebFetch`
  reads. No snippet-only sourcing here.
- **`supplemental_resources[]`** is produced by invoking
  `find-courses/SKILL.md`'s existing, unmodified procedure — `WebSearch`
  only, and it explicitly never claims to have fetched a page. `college-plan`
  inherits that weaker contract as-is for this one section, and the report
  body labels it differently from the fetch-backed sections so a reader
  never assumes uniform rigor across the document.

## Study Notes / profile-skill canonicalization

When `profile.yaml` is present, Study Notes compares the learner's
`current_skills` against `covers_skill_ids` **canonically**: reuse
`resolution.py resolve-profile-skills` (exactly as `skillpath` itself does)
to resolve `current_skills[].skill` free text to `skill_id` before
comparing against any course's `covers_skill_ids`. Comparing raw `skill`
text directly would silently match nothing — the exact bug class
`skillpath`'s own schema doc already fixed once; this skill must not
reintroduce it.

## Report Schema

```yaml
report_id: <uuid4>
generated_at: <UTC ISO8601 timestamp>
major: string
target_state: string          # = target_role — reused verbatim so the
                               # unmodified write_report() filename-slug
                               # logic needs no changes
target_level: string          # explicit value, or the entry-level default
                               # (see Invocation) — always populated
target_level_was_defaulted: boolean
research_confidence: high | medium | low   # roll-up; see per-entry confidence below
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
    confidence: high | medium | low     # per-requirement, new in round 2
    frequency_signal: number
    sources: [ ... ]                    # identical shape to skillpath's own field
course_sequence:
  - year: integer | "unscheduled"
    courses:
      - course_name: string
        status: completed | in_progress | upcoming
        prerequisites: [string]
        covers_skill_ids: [string]
        coverage_evidence:              # new in round 2 — replaces implicit sourcing
          - skill_id: string
            source_urls: [string]
        confidence: medium | high        # never low — see inclusion threshold
        compressed_from_source_year: integer | null
        behind_typical_schedule: boolean
        sources:
          - url: string
            title: string
            school: string
            accessed_at: <UTC ISO8601 timestamp>
electives:                       # new in round 2 — single-school, target-aligned
  - course_name: string
    school: string
    covers_skill_ids: [string]
    coverage_evidence: [ ... ]
    sources: [ ... ]
self_reported_courses:           # new in round 2 — learner courses with no archetype match
  - course_name: string          # as stated by the learner
    status: completed | in_progress
    skill_id: string | null      # best-effort resolve_skill result, or null if unmapped
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
   context summary (degree type, education system, current year, program
   length), date generated, and the generic-archetype disclaimer (always
   present).
2. **Target Role Requirements** — `target_requirements[]` grouped by tier
   (Critical first), each with its own confidence and a one-line citation.
3. **Course Sequence by Year** — `course_sequence[]` grouped by year
   (`"unscheduled"` as its own final group), each course marked
   completed/in-progress/upcoming, the skills it covers with citations, and
   any `compressed_from_source_year` / `behind_typical_schedule` flag
   rendered as a plain-language note. Course-load/co-op advisory notes
   (see above) render per-year where triggered.
4. **Electives Worth Considering** — `electives[]`, explicitly labeled
   single-school/low-corroboration, each tied to the target-role skill it
   addresses.
5. **Skills Not Covered by a Typical Curriculum** — `uncovered_skills[]`
   with tier, immediately followed by **Supplemental Resources** (from
   `find-courses`), labeled as web-search-sourced, not fetched-and-verified
   like sections 2-4.
6. **Study Notes** — canonically-resolved `current_skills` overlap (if
   `profile.yaml` present) and a plain summary of `self_reported_courses[]`
   (what the learner already reported completing that fell outside the
   generic archetype).
7. **Next Steps** — confirm exact course numbers/prerequisites with an
   actual advisor/degree audit (especially the "unscheduled" group and any
   `electives[]` entry); re-run in a future term if major, target role, or
   progress changes.

## Privacy

`roadmaps/college-plans/` is added to `.gitignore` alongside the existing
`roadmaps/report-*.md` entry.

## Out of Scope (v1)

- School-specific catalogs (confirmed with the user: major-based, not
  school-based).
- Tracking completed courses across runs / a tracker CSV integration — no
  lifecycle state. Learner context is asked fresh each run (see Learner
  Context above); a report is a point-in-time recommendation.
- Full term-by-term scheduling (only year-level placement; course-load/
  co-op constraints are advisory notes, not a scheduling optimizer — see
  "Applying course-load and co-op constraints").
- Degree-requirement satisfaction (gen-eds, credit hours, graduation
  requirements) — this tool answers "which courses get you career-ready,"
  not "which courses satisfy your degree."

## Verification Plan

**Automated (`pytest`):**
1. `test_curriculum_planner.py` — all cases listed under "Deterministic
   Module" above (match/ambiguous/unmatched, prerequisite chain, cycle
   detection, program-length clamping, unresolvable-disagreement →
   unscheduled, behind-schedule reclassification, coverage via each
   status, coverage via `self_reported_courses[]`, Low-tier exclusion).
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
5. **Codex packaging integrity** (round-2 smaller-improvement): a test
   confirming `codex/skills/college-plan/reference` and `.../scripts`
   resolve (via the symlink chain) to the exact same files as
   `.claude/skills/college-plan/reference`/`scripts`, and that
   `.agents/skills/college-plan` resolves to `codex/skills/college-plan` —
   the same integrity check pattern already implied by `skillpath`'s
   existing packaging, made explicit and automated here.
6. Privacy: `git check-ignore -v roadmaps/college-plans/<a-generated-file>`
   confirms it's actually matched by `.gitignore`.

**Manual / end-to-end:**
7. `/college-plan "Computer Science" "Data Scientist"` for a stated
   freshman (`current_year_number: 1`, no completed courses) — confirm
   both research passes use real `WebFetch` reads; confirm
   `course_sequence[]` courses are corroborated at ≥2 of ≥3 same-education-
   system school sources (or land in `"unscheduled"`); confirm the
   disclaimer renders; confirm the report saves under
   `roadmaps/college-plans/`.
8. Same target role, stated as a third-year student with named
   completed/in-progress courses (including at least one that won't match
   any archetype course, to exercise `self_reported_courses[]`, and one
   ambiguous name to exercise the conversational disambiguation) — confirm
   correct `status` assignment, confirm the remaining sequence starts at
   Year 3, confirm a required-but-not-yet-taken course flags
   `behind_typical_schedule` correctly.
9. State a 3-year program length against curriculum sources describing a
   4-year sequence — confirm clamping and the `compressed_from_source_year`
   note render.
10. State `course_load_constraints: "max 3 courses/term"` against a year
    that ends up with 6+ courses — confirm the advisory note renders;
    confirm it does **not** change `final_year` for any course.
11. Run `/skillpath` afterward (same repo, same session) — confirm its
    diff step is unaffected (covered by test 3, re-confirmed live here).
12. Run with and without `profile.yaml` present — confirm Study Notes
    behaves correctly in both cases via canonical `skill_id` resolution.
13. Confirm `/college-plan` does not fire from ambient conversation in
    Claude Code, and `$college-plan` requires explicit invocation in Codex.

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
