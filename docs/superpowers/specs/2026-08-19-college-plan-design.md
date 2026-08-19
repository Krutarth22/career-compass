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
- There is no single school's catalog to consult (confirmed with the user
  — this is major-based, not school-based); the result is necessarily a
  **generic curriculum archetype**, not one institution's exact course
  numbers.

`college-plan` is a new, small, explicit-invocation skill that reuses two
pieces of `skillpath` exactly as they exist today — the target-role
research procedure (`reference/research-protocol.md`) and the
skill-resolution module (`scripts/resolution.py`) — and adds one new thing:
a curriculum-research pass plus a course-sequencing report. It does not
require a prior `/skillpath` run or an existing `profile.yaml`; both are
used opportunistically when present, never required.

## Repo Layout (additions only)

```
.claude/skills/
├── skillpath/                          # unchanged
├── find-courses/                       # unchanged
└── college-plan/
    ├── SKILL.md                        # explicit-invocation only (writes a file)
    └── reference/
        └── curriculum-research-protocol.md
roadmaps/
└── college-plans/                      # new, gitignored — separate from skillpath's roadmaps/report-*.md
    └── plan-<timestamp>-<id>-<major-slug>-<target-slug>.md
```

No new Python scripts. `college-plan` calls `skillpath`'s existing
`scripts/resolution.py` (`resolve-skill`, unchanged) and
`scripts/report_state.py` (`write_report`/`read_report`/`get_last_report`,
unchanged) via the same `${CLAUDE_SKILL_DIR}`-relative-path convention
`skillpath` already uses, just from a sibling skill directory
(`${CLAUDE_SKILL_DIR}/../skillpath/scripts/...`) — the same cross-skill
reuse pattern `find-courses/SKILL.md` already uses to load `profile_io.py`.

**Why no new scripts:** the only genuinely new deterministic behavior is
"call `write_report`/`get_last_report` with a different `roadmaps_dir`
argument" — both functions already take that as a parameter, so no code
changes are needed there. Course-to-skill tagging reuses `resolve_skill`
unchanged. Everything else (which courses exist, what year they're
typically taken, which requirements they cover) is live-research synthesis,
same as `skillpath` Step 3/4 today — genuinely the model's job, not a
deterministic algorithm, so it gets a reference doc (this skill's
`curriculum-research-protocol.md`), not a script.

## Invocation

- **`/college-plan "<major>" "<target_role>" ["<target_level>"]`** in Claude
  Code, **`$college-plan "<major>" "<target_role>" ["<target_level>"]`** in
  Codex. Zero-indexed positional args: `$0` = major, `$1` = target_role,
  `$2` = optional target_level.
- **Explicit-invocation only** (the Claude Code equivalent of
  `disable-model-invocation: true`), matching `/skillpath`'s reasoning — it
  writes a personal file to disk, so it must never fire from ambient
  conversation.
- **No required prerequisite state.** Neither `profile.yaml` nor a prior
  `/skillpath` report needs to exist. If `${PROJECT_ROOT}/profile.yaml` is
  present, load it the same way `find-courses` already does (reusing
  `skillpath`'s `profile_io.py`) and use `location` (to localize the
  target-role research queries) and `current_skills` (to note, in the
  report, courses the learner can likely test out of or treat as review) —
  but proceed identically, just without those refinements, when it's
  absent.
- **Resource resolution:** identical convention to `skillpath` —
  `${CLAUDE_SKILL_DIR}`-relative for this skill's own `reference/` files
  and for the sibling `skillpath`/`find-courses` scripts and docs it reuses;
  `${PROJECT_ROOT}`-relative (via `git rev-parse --show-toplevel`, falling
  back to cwd) for `profile.yaml` and the new `roadmaps/college-plans/`
  output directory.

## Steps

1. **Parse args.** `major`, `target_role`, optional `target_level`. Load
   `profile.yaml` opportunistically per Invocation above.
2. **Research target-role requirements.** Follow
   `skillpath/reference/research-protocol.md` exactly (same query patterns,
   same ≥4-postings + ≥2-practitioner-sources evidence bar, same
   `resolve-skill` resolution, same confidence scoring) to produce
   `target_requirements[]`. This is the one piece intentionally duplicated
   *by reference*, not by re-implementation — the doc is read and followed,
   never copy-pasted.
3. **Research curriculum.** Follow this skill's own
   `reference/curriculum-research-protocol.md` (see below) to produce
   `course_sequence[]`: a generic, year-by-year `<major>` curriculum
   synthesized across multiple real university program pages, with each
   course tagged against `target_requirements[]` via `resolve_skill`.
4. **Diff.** Any `target_requirements[]` entry with `tier` Critical/High/
   Medium that no course in `course_sequence[]` covers becomes an entry in
   `uncovered_skills[]`.
5. **Supplemental resources.** For every `uncovered_skills[]` entry, invoke
   `find-courses/SKILL.md`'s existing procedure in-process (same reuse
   pattern `skillpath` Step 7 already uses) to produce
   `supplemental_resources[]`.
6. **Compose & save.** Build the frontmatter (schema below), render the
   body, and call `report_state.write_report()` with
   `roadmaps_dir = "${PROJECT_ROOT}/roadmaps/college-plans"` — a directory
   `skillpath`'s own `get_last_report()` never globs, since that always
   receives `${PROJECT_ROOT}/roadmaps` directly. This is what keeps the two
   report families from colliding without any change to `report_state.py`.
7. **Print the saved path** as the final response.

**Carried-over rules from `skillpath`:** never fabricate a course, source,
or resource; every `target_requirements`/`course_sequence`/
`supplemental_resources` claim traces to a real fetched source; be explicit
about the confidence level; always save the report.

## `reference/curriculum-research-protocol.md` (new)

- **Queries:** `"<major>" degree requirements course list`,
  `typical "<major>" curriculum by year`, `"<major>" course sequence
  recommended`, run against **at least 3 distinct universities'** own
  program/catalog pages (not aggregator sites), each opened and read via
  `WebFetch` — same "snippet never counts" rule as
  `research-protocol.md`. No current-year filter needed (curriculum
  structure is far more stable than hiring trends), but note each source's
  `accessed_at`.
- **Synthesis, not transcription:** a course only enters `course_sequence[]`
  if it appears, in substance, across multiple consulted programs (e.g.
  "Data Structures" showing up at 3 of 3 schools, even under a different
  course number at each) — this is what makes the result a genuine
  archetype rather than one school's idiosyncratic catalog. A course
  specific to a single consulted school is noted only as a per-source aside
  in that course's entry, never promoted to the generic sequence.
- **Explicit disclaimer, always rendered:** the report states, unconditionally, that this is a generic
  curriculum archetype synthesized from multiple schools' typical
  offerings — not any specific school's actual course catalog — and that
  exact course numbers, prerequisites, and availability must be confirmed
  against the learner's actual school and advisor.
- **Year placement:** use the year/semester the source pages themselves
  state (e.g. "typically taken sophomore year") rather than inferring one;
  when sources disagree, place the course in the earliest year any source
  states and note the disagreement in that course's entry.
- **Confidence scoring:** reuse `research-protocol.md`'s high/medium/low
  definitions, evaluated per curriculum claim the same way (≥3 corroborating
  school sources = high; 2 = medium; 1 or conflicting = low). A low-confidence
  course is still included but flagged in the report, never dropped.

## Report Schema

Frontmatter (written via `report_state.write_report`, same
frontmatter-then-body file shape `skillpath` uses):

```yaml
report_id: <uuid4>
generated_at: <UTC ISO8601 timestamp>
major: string
target_state: string          # = target_role; reused verbatim as the field
                               # name write_report() already expects for its
                               # filename-slug logic
target_level: string | null
research_confidence: high | medium | low
target_requirements:          # identical shape to skillpath's own field —
  - ...                       # see skillpath/reference/report-format.md
course_sequence:
  - year: integer              # 1-4; a course spanning ambiguous years uses
                                # the earliest per the protocol above
    courses:
      - course_name: string    # generic title, e.g. "Data Structures"
        covers_skill_ids: [string]
        confidence: high | medium | low
        sources:
          - url: string
            title: string
            school: string
            accessed_at: <UTC ISO8601 timestamp>
uncovered_skills:
  - skill_id: string
    tier: Critical | High | Medium | Low
supplemental_resources:        # find-courses output per uncovered_skills entry
  - skill_id: string
    resources: [ ... ]         # same shape find-courses already returns
```

`target_requirements[]` reuses the exact schema `skillpath` already
documents in `reference/report-format.md` — not a new format.

## Report Body

Fixed section order, mirroring `skillpath`'s own `report-format.md` style
(plain Markdown, headers, tables where they aid scanning):

1. **Header** — major, target role/level, date generated, and the
   generic-archetype disclaimer (always present, not conditional).
2. **Course Sequence by Year** — `course_sequence[]` grouped by year,
   each course with the target-role skills it covers.
3. **Skills Not Covered by a Typical Curriculum** — `uncovered_skills[]`
   with their tier, immediately followed by **Supplemental Resources** for
   each (from `find-courses`).
4. **Study Notes** — if `profile.yaml` was available, which listed courses
   the learner's existing `current_skills` likely cover already (framed as
   "you may be able to test out of / treat as review," never as a claim
   they should skip a required course).
5. **Next Steps** — confirm exact course numbers/prerequisites with your
   actual school's advisor/degree audit; re-run in a future term if your
   major or target role changes.

## Privacy

`roadmaps/college-plans/` is added to `.gitignore` alongside the existing
`roadmaps/report-*.md` entry — same reasoning (generated reports reflect a
real person's academic/career plan).

## Out of Scope (v1)

- School-specific catalogs (confirmed with the user: major-based, not
  school-based).
- Tracking completed courses / a tracker CSV integration — no lifecycle
  state, no `skill_confirmed` events. A `college-plan` report is a
  point-in-time recommendation; re-running it produces a fresh one. Adding
  progress tracking is a natural fast-follow but is not required for this
  to be useful, and pulls in `skillpath`'s tracker schema, which is scoped
  to *its* gap-lifecycle model — not a good fit to force onto a course
  sequence without a dedicated design pass.
- Degree-requirement satisfaction (gen-eds, credit hours, graduation
  requirements) — this tool answers "which courses get you career-ready,"
  not "which courses satisfy your degree," which is registrar/advisor
  territory.

## Verification Plan

1. `/college-plan "Computer Science" "Data Scientist"` — confirm both
   research passes run with real `WebFetch` reads (inspect transcript);
   confirm `course_sequence[]` courses are corroborated across ≥3 real
   school sources each (or flagged low-confidence when not); confirm the
   generic-archetype disclaimer renders; confirm the report saves under
   `roadmaps/college-plans/` and not `roadmaps/`.
2. Run `/skillpath` afterward (same repo, same session) — confirm its
   `get_last_report()` / Since-Last-Report diff is unaffected by the
   college-plan report's existence (it never globs `college-plans/`).
3. Run with a `profile.yaml` present that lists `current_skills` — confirm
   the Study Notes section correctly cross-references them; run again with
   no `profile.yaml` — confirm the section is simply omitted, no crash, no
   placeholder text.
4. Confirm `/college-plan` does not fire from ambient conversation (explicit
   invocation only), same check already used for `/skillpath`.
5. Privacy check: `git check-ignore -v roadmaps/college-plans/<a-generated-file>`
   confirms it's actually matched, not just absent from `git status`.

## Critical Files to Create

- `.claude/skills/college-plan/SKILL.md`
- `.claude/skills/college-plan/reference/curriculum-research-protocol.md`
- `.gitignore` — add `roadmaps/college-plans/`
