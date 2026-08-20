---
name: college-plan
description: Use only when the user explicitly invokes college-plan with `/college-plan` in Claude Code or `$college-plan` in Codex to get a major-based, multi-year college course sequence toward a target career. It researches target-role requirements and a generic multi-school curriculum, matches the learner's own coursework, sequences remaining courses, and writes a personal college-plan report. Never invoke it implicitly because it writes a file.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, AskUserQuestion
---

# college-plan

Answer a different, earlier question than `skillpath` does: "I'm entering
(or already in) college, majoring in `<major>` — what courses should I
actually take, in what order, to end up qualified for `<target_role>`?"

Reuses `skillpath`'s target-role research procedure
(`../skillpath/reference/research-protocol.md`), skill-resolution module
(`../skillpath/scripts/resolution.py`), and report-file writer
(`../skillpath/scripts/report_state.py`) exactly as they exist today. Adds
a new curriculum-research pass and a new deterministic
matching/sequencing/coverage script (`scripts/curriculum_planner.py`).
Does not require a prior `/skillpath` run or an existing `profile.yaml` —
both are used opportunistically when present, never required.

## Resolving paths

Same convention as `skillpath`:

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SKILL_DIR="${CLAUDE_SKILL_DIR:-${PROJECT_ROOT}/.agents/skills/college-plan}"
SKILLPATH_SKILL_DIR="${SKILL_DIR}/../skillpath"
```

Claude Code supplies `CLAUDE_SKILL_DIR` directly. Codex discovers the
repo-scoped symlink at `.agents/skills/college-plan`, resolving through to
`codex/skills/college-plan/`, whose `reference/` and `scripts/` entries
are themselves symlinks into `.claude/skills/college-plan/`.

**Bundled resources** (`reference/*`, `scripts/*.py`, and the same for
`skillpath` via `SKILLPATH_SKILL_DIR`) are addressed with these variables
— never a bare relative path.

**Runtime state** — only `roadmaps/college-plans/` (this skill writes no
`profile.yaml`, no tracker) — resolves relative to `PROJECT_ROOT`. Create
`${PROJECT_ROOT}/roadmaps/.tmp/` (already gitignored, shared with
`skillpath`) with `mkdir -p` before first use in a run, for the
intermediate JSON files the CLI-less pure functions below need as file
input.

## Invocation

`/college-plan "<major>" "<target_role>" ["<target_level>"]` in Claude
Code, `$college-plan "<major>" "<target_role>" ["<target_level>"]` in
Codex. Zero-indexed positional args: `$0` = major, `$1` = target_role,
`$2` = optional target_level.

## Step 1 — Parse args

If `$2` is absent, default `target_level` to `"entry-level / new
graduate"` and record `target_level_was_defaulted: true` in the
frontmatter; otherwise use `$2` and set that flag `false`.

## Step 2 — Learner-context intake

Ask the learner, conversationally, for each field below. Nothing here is
persisted to `profile.yaml` or any new state file — it's asked fresh every
run (see the spec's Out of Scope: no cross-run course-tracking in v1).

- `degree_type` (e.g. "BS", "BA")
- `education_system` (e.g. "United States", "United Kingdom") — scopes
  which schools count toward corroboration in Step 4
- `current_year_number` — ask for this **as an integer directly**, never
  parsed out of free text
- `current_year_or_semester` — a free-text display string for the report
  header only (e.g. "Fall of my sophomore year"); no downstream code reads
  it
- `expected_program_length_years` — default to `4` if the learner doesn't
  know
- `course_load_constraints` — free text, or `null` if none stated
- `completed_courses` — free text list, exactly as the learner names them
- `in_progress_courses` — free text list, exactly as the learner names
  them

Then, opportunistically, check for `${PROJECT_ROOT}/profile.yaml`:

```bash
python3 "${SKILLPATH_SKILL_DIR}/scripts/profile_io.py" load "${PROJECT_ROOT}/profile.yaml"
```

If present, use its `location` field to localize Step 3's research
queries. If absent, proceed without that refinement — this skill never
requires a profile.

## Step 3 — Research target-role requirements

Follow `${SKILLPATH_SKILL_DIR}/reference/research-protocol.md` exactly —
same evidence bar (≥4 fetched postings + ≥2 fetched practitioner sources
per validated requirement), same current-year/evergreen query split.
Resolve each surfaced skill mention:

```bash
python3 "${SKILLPATH_SKILL_DIR}/scripts/resolution.py" resolve-skill "<free text mention>"
```

Unlike `skillpath`, this skill has no `gap_assessments[]` layer, so it
assigns `tier` (Critical/High/Medium/Low, by frequency signal +
centrality, capped at Medium when confidence is low) and a per-requirement
`confidence: high | medium | low` directly on each `target_requirements[]`
entry here, using the identical judgment rule
`research-protocol.md`/`skillpath`'s Step 4 documents. Also roll the set
up into an overall `research_confidence` for the report.

## Step 4 — Research curriculum

Follow `reference/curriculum-research-protocol.md` in full to produce two
lists:

- A raw `course_sequence[]` (not yet placed into years): each entry has
  `course_name`, `aliases` (real course codes seen at consulted schools),
  `source_years`, `prerequisites` (referencing other entries'
  `course_name` values), `covers_skill_ids`, `coverage_evidence`,
  `confidence`, `sources`.
- `electives[]`: single-school, target-aligned courses.

## Step 5 — Match learner courses to the archetype

Build one combined list tagging each of Step 2's `completed_courses` /
`in_progress_courses` with its own status:

```json
[
  {"course_name": "...", "status": "completed"},
  {"course_name": "...", "status": "in_progress"}
]
```

Write that list and the raw `course_sequence[]` from Step 4 to
`${PROJECT_ROOT}/roadmaps/.tmp/`, then:

```bash
python3 "${SKILL_DIR}/scripts/curriculum_planner.py" match \
  --learner-courses "${PROJECT_ROOT}/roadmaps/.tmp/learner_courses.json" \
  --sequence "${PROJECT_ROOT}/roadmaps/.tmp/raw_course_sequence.json"
```

Prints `{"matched": [...], "ambiguous": [...], "unmatched": [...]}`. Then:

- For each `matched` entry, set that archetype course's `status` to the
  matched entry's `status`.
- For each `ambiguous` entry, ask the learner once, conversationally,
  which of `candidates` they mean, then apply it as a match (same as
  above).
- For each `unmatched` entry, add a `self_reported_courses[]` entry with
  that `course_name`/`status` and `covers_skill_ids: []` (see "Coverage
  and self-reported courses" below) — never discarded, never guessed into
  a match.
- Every archetype course **not** matched to anything keeps
  `status: "upcoming"`.

## Step 6 — Sequence

```bash
python3 "${SKILL_DIR}/scripts/curriculum_planner.py" sequence \
  --courses "${PROJECT_ROOT}/roadmaps/.tmp/course_sequence_with_status.json" \
  --program-length <expected_program_length_years> \
  --current-year <current_year_number>
```

Prints the same course list, each entry now carrying `final_year` (int or
`"unscheduled"`), `compressed_from_source_year`, `behind_typical_schedule`,
`infeasible_within_program_length`, `source_disagreement`, and
`blocked_by_unscheduled_prerequisite`. Group by `final_year` for the
report body (Step 10) — `"unscheduled"` is its own final group.

## Step 7 — Diff

```bash
python3 "${SKILL_DIR}/scripts/curriculum_planner.py" diff \
  --requirements "${PROJECT_ROOT}/roadmaps/.tmp/target_requirements.json" \
  --sequence "${PROJECT_ROOT}/roadmaps/.tmp/sequenced_courses.json" \
  --self-reported "${PROJECT_ROOT}/roadmaps/.tmp/self_reported_courses.json"
```

Prints `uncovered_skills[]` (Critical/High/Medium-tier `target_requirements`
not covered by any course/self-reported entry with status in {completed,
in_progress, upcoming}).

## Step 8 — Supplemental resources

For every `uncovered_skills[]` entry, follow
`../find-courses/SKILL.md`'s existing procedure in-process — same
`WebSearch`-only sourcing contract, never claiming to have fetched a page.
Collect its structured output (name, URL, reason, duration, cost) for
Step 10's report body, rather than printing it.

## Step 9 — Apply course-load/co-op advisories

Presentation-only — never mutates any `final_year`:

- If `course_load_constraints` states a per-term cap and a year's course
  count exceeds roughly double that, add an advisory note for that year:
  consider spreading across a summer term or extending the timeline.
- If `course_load_constraints` mentions co-op/alternating work terms, add
  one general advisory note: this sequence models academic years only,
  not co-op gaps — confirm actual calendar placement with a co-op
  coordinator.

## Step 10 — Compose & save

Build the frontmatter (schema in `docs/superpowers/specs/2026-08-19-college-plan-design.md`'s
"Report Schema") and render the body in this fixed order: Header, Target
Role Requirements, Course Sequence by Year, Electives Worth Considering,
Skills Not Covered by a Typical Curriculum + Supplemental Resources, Study
Notes, Next Steps.

**Study Notes canonicalization:** when `profile.yaml` is present, compare
its `current_skills` against `covers_skill_ids` canonically — resolve
`current_skills[].skill` free text via
`resolution.py resolve-profile-skills` first, exactly as `skillpath`
itself does, never compare raw `skill` text directly. List
`self_reported_courses[]` plainly as "reported, but not counted toward
requirement coverage — use `/skillpath confirm` if you can back a specific
skill claim with evidence."

`report_state.py` has no CLI subcommand for writing — write the
frontmatter dict and composed body to `${PROJECT_ROOT}/roadmaps/.tmp/`
first, then:

```bash
python3 -c "
import json, sys
sys.path.insert(0, '${SKILLPATH_SKILL_DIR}/scripts')
from report_state import write_report

tmp = '${PROJECT_ROOT}/roadmaps/.tmp'
frontmatter = json.load(open(f'{tmp}/frontmatter.json'))
body = open(f'{tmp}/body.md', encoding='utf-8').read()

path = write_report('${PROJECT_ROOT}/roadmaps/college-plans', frontmatter, body)
print(path)
"
```

`target_state` in the frontmatter is set to `target_role` — `write_report()`'s
existing filename-slug logic needs no changes.

## Step 11 — Print the saved path

Report the saved path to the user as the final response.

## Coverage and self-reported courses

A `target_requirements[]` entry is covered if *any* `course_sequence[]` or
`self_reported_courses[]` entry with `status in {completed, in_progress,
upcoming}` lists that `skill_id` in `covers_skill_ids`.
`self_reported_courses[]` entries always carry `covers_skill_ids: []` in
v1 — there's no fetchable source to ground a self-reported course's claim
against (the same rule that keeps `course_sequence[]`/`electives[]` from
ever inferring coverage from a bare title). They're listed in the report
for the learner's own record, never for coverage credit.

## Carried-over rules from `skillpath`

Never fabricate a course, source, or resource; every research-pass claim
traces to a real fetched source (with `find-courses`'s one documented
search-only exception); be explicit about confidence; always save the
report.
