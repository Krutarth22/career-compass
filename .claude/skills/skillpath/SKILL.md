---
name: skillpath
description: This skill should be used when the user explicitly runs "/skillpath", asks to "generate my skill roadmap", "update my career transition plan", "research my target role gaps", or "confirm a skill" via "/skillpath confirm". It researches a target role's current live requirements, reconciles them against a tracked skill-gap history, plans a sequenced set of hands-on projects, finds course resources for remaining gaps, and writes a personal roadmap report to disk. It writes personal files (profile.yaml, tracker/skillpath_tracker.csv, roadmaps/*.md) and must never fire from ambient conversation -- only on an explicit /skillpath invocation.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, AskUserQuestion
---

# skillpath

Research a user's target career role, reconcile it against their tracked
skill-gap history, plan a sequenced set of hands-on projects, surface course
resources for what's left, and write a personal roadmap report to disk.

This is the primary, explicit-invocation-only skillpath skill. It is never
invoked by Claude on its own judgment (`disable-model-invocation: true`) --
only by a user typing `/skillpath ...`. It writes to `profile.yaml`,
`tracker/skillpath_tracker.csv`, and `roadmaps/*.md`, all of which are
personal, gitignored data.

## Resolving paths

Two path roots matter, and they resolve differently -- do not conflate them.

**Bundled resources** (`templates/`, `reference/*`, `scripts/*.py`) are
part of this skill's own package and are addressed with the
`${CLAUDE_SKILL_DIR}` substitution, which expands to the directory
containing this `SKILL.md` file regardless of the invocation's working
directory. Every `Bash` call to one of the scripts below uses
`${CLAUDE_SKILL_DIR}/scripts/<name>.py` -- never a bare `scripts/<name>.py`
relative path, which would only work by accident of cwd.

**Runtime state** (`profile.yaml`, `tracker/skillpath_tracker.csv`,
`roadmaps/`) belongs to the user's project, not this skill's package, and
resolves relative to the **project root**. Determine the project root once
per run:

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
```

From `PROJECT_ROOT`, the runtime paths are:

- `${PROJECT_ROOT}/profile.yaml`
- `${PROJECT_ROOT}/tracker/skillpath_tracker.csv`
- `${PROJECT_ROOT}/roadmaps/`
- `${PROJECT_ROOT}/roadmaps/.tmp/` -- scratch directory (already gitignored)
  for the intermediate JSON files that the CLI-less functions below need as
  file input; create it with `mkdir -p` before first use in a run.

## Bundled scripts used this run

All six scripts are invoked from `${CLAUDE_SKILL_DIR}/scripts/`:

| Script | CLI? | Used for |
|---|---|---|
| `profile_io.py` | `load`, `merge` (no `save` subcommand) | Step 1, 2 |
| `tracker_io.py` | `append`, `read` (also has `last-report`, unused below -- `report_state.py last` is called directly instead) | Step 1, 2, 9 |
| `report_state.py` | `read`, `last` (no `write-report` subcommand) | Step 2, 9 |
| `resolution.py` | `resolve-skill`, `resolve-profile-skills`, `resolve-track` | Step 1, 2, 3, 5 |
| `gap_state.py` | none -- pure function, no `__main__` at all | Step 4 |
| `project_planner.py` | `plan` | Step 6 |

Three of these -- `profile_io.py` saving a profile, `gap_state.py`'s
`reconcile_assessments`, and `report_state.py` writing a report -- have no
CLI wrapper for the operation this skill needs. For those, write the
required input(s) as JSON to `${PROJECT_ROOT}/roadmaps/.tmp/` first (via
the `Write` tool), then invoke the underlying pure function with a one-off
`python3 -c` snippet that adds `${CLAUDE_SKILL_DIR}/scripts` to `sys.path`
and imports it directly. The exact snippets are given inline at each step
below -- do not invent a CLI subcommand for these that doesn't exist.

## Step 1 -- Parse arguments and confirm sub-command

Two invocation shapes:

- **Main flow:** `/skillpath "<current-state>" "<target-state>"` -- `$0` is
  the current-state text, `$1` is the target-state text.
- **Confirm sub-command:** `/skillpath confirm "<skill>" "<evidence>"` --
  `$0` is the literal string `confirm`, `$1` is the skill text, `$2` is
  optional evidence text.

If `$0` is literally `confirm`:

1. Resolve the skill mention to a canonical id:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/resolution.py" resolve-skill "$1"
   ```
   This prints `{"id": "...", "unmapped": true|false}`.
2. If `$2` (evidence) is absent, ask the user once conversationally for
   evidence backing the confirmation before proceeding -- an empty answer
   is fine, do not loop asking.
3. Load the current profile (see Step 2's `profile_io.py load` call) to
   read its `target_role`/`target_level` for the `confirmed_for_*` fields.
4. Append a tracker row:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/tracker_io.py" append \
     "${PROJECT_ROOT}/tracker/skillpath_tracker.csv" \
     --occurred-at "<current UTC ISO8601 timestamp>" \
     --event-type skill_confirmed \
     --item-name "<resolved skill id or display name>" \
     --related-skill-ids "<resolved skill id>" \
     --report-id "<report_id of the most recent report, or empty string if none>" \
     --notes "<the evidence text, or empty>" \
     --confirmed-for-target-role "<profile.target_role>" \
     --confirmed-for-target-level "<profile.target_level, or empty>"
   ```
5. Report success to the user and **stop** -- do not continue into
   research/report generation for a `confirm` invocation.

Otherwise (main flow), determine the merge mode:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/profile_io.py" merge \
  "${PROJECT_ROOT}/profile.yaml" \
  --current-state "$0" \
  --target-state "$1"
```

(Omit `--current-state`/`--target-state` entirely -- not empty strings --
when `$0`/`$1` are empty, so `merge_profile` sees `None` and falls back to
the conversational flow per the three-branch rule.) This prints
`{"profile": {...}, "mode": "first_run" | "override" | "as_is"}`.

- **`first_run`:** No `profile.yaml` exists yet. Run a short conversational
  profile-creation flow (current role, years of experience, current
  skills with proficiency/evidence, target role, target level, location,
  industry preference, weekly time budget hours, horizon weeks, and any
  constraints -- per `reference/profile-schema.md`), pre-filling
  `current_role`/`target_role` from the printed `profile` object where
  present so the user isn't asked to retype what they already gave on the
  command line. At the end, save via the `python3 -c` snippet under
  Step 2 below -- a first run always ends with a saved `profile.yaml`.
- **`override`:** A saved profile exists and `$0`/`$1` were supplied. Use
  the printed `profile` object (the saved profile with `$0`/`$1` applied
  on top) for this run only -- never overwrite `profile.yaml` silently.
  After the run completes (Step 9), ask once whether to save the override
  permanently; only an explicit yes saves it.
- **`as_is`:** A saved profile exists and no args were supplied. Use it
  unchanged, no prompts.

## Step 2 -- Load state

Load the profile (already available from Step 1's `merge` call as the
`profile` object -- no need to call `load` again unless re-reading after a
conversational edit):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/profile_io.py" load "${PROJECT_ROOT}/profile.yaml"
```

Read tracker rows:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/tracker_io.py" read "${PROJECT_ROOT}/tracker/skillpath_tracker.csv"
```

(Add `--since <ISO date>` or `--event-types a,b` filters only if a
specific narrower read is needed; the unfiltered read is the default for
this step since Step 4's reconciliation needs the full event history.)

Load the prior report's frontmatter, if any:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/report_state.py" last "${PROJECT_ROOT}/roadmaps"
```

Prints the newest report's frontmatter dict, or `null` if none exists (or
the newest one is corrupt) -- treat `null` as "no prior report" throughout
(skip Step 8 entirely, and Step 4's `prior_assessments` is `[]`).

### Step 2b -- Resolve the profile's skills to canonical ids (mandatory)

`profile.yaml`'s `current_skills[].skill` is free text the user typed ("CAD
Design", "Python", "Excel"). Both Step 4's `reconcile_assessments` and Step
6's `project_planner.py plan` match a profile skill against **canonical
taxonomy ids** via each entry's `skill_id` key, and ignore the free-text
`skill` field entirely. **This resolution step is not optional and must run
here, before Step 4 and Step 6** -- skip it and the user's real skills cover
nothing, so genuine strengths are reported as open gaps and already-held
project prerequisites get charged relearning hours.

Write the profile's `current_skills` list (just that list) to
`${PROJECT_ROOT}/roadmaps/.tmp/current_skills_raw.json`, then:

```bash
mkdir -p "${PROJECT_ROOT}/roadmaps/.tmp"
python3 "${CLAUDE_SKILL_DIR}/scripts/resolution.py" resolve-profile-skills \
  --current-skills "${PROJECT_ROOT}/roadmaps/.tmp/current_skills_raw.json" \
  --taxonomy "${CLAUDE_SKILL_DIR}/reference/skill-taxonomy.yaml"
```

This prints the same list of entries with a `skill_id` key added to each
(the canonical id, or a provisional slug when the skill isn't in the
taxonomy); the original `skill` text is preserved for display. Save that
output as `${PROJECT_ROOT}/roadmaps/.tmp/profile_skills.json` -- it is the
exact file Step 6 passes as `--profile-skills`, and the same resolved list
must replace `current_skills` in the profile dict written as
`${PROJECT_ROOT}/roadmaps/.tmp/profile.json` for Step 4. Do **not** write
these resolved ids back into `profile.yaml`; the saved profile stays
human-editable free text and is re-resolved on every run.

## Step 3 -- Research target requirements

Follow `reference/research-protocol.md` in full. This step is the model's
own job (WebSearch plus judgment) -- there is no script for it. Build
queries from the profile's `target_role`, `target_level`, and `location`;
mix current-year market-relevance queries with evergreen canonical-doc
queries; hold every requirement to the ≥4-postings + ≥2-practitioner-source
evidence bar before treating it as validated; score each requirement's
confidence high/medium/low per that reference doc. Resolve each surfaced
skill mention:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/resolution.py" resolve-skill "<free text mention>"
```

Produce the `target_requirements` list in the exact shape documented in
`reference/report-format.md` (matching `report_state.py`'s frontmatter
schema) and an overall `research_confidence` for the report.

## Step 4 -- Tier requirements and reconcile gaps

Tier each requirement Critical/High/Medium/Low by frequency-signal and
centrality to the role -- this is the model's judgment call, not a script's
(per `reference/research-protocol.md`, cap at Medium when a requirement's
own confidence is low regardless of apparent frequency/centrality).

`gap_state.py` has no CLI -- `reconcile_assessments` is a pure Python
function only. Write its four inputs to `${PROJECT_ROOT}/roadmaps/.tmp/` as
JSON (the tiered requirements list as
`[{"skill_id": ..., "tier": ...}, ...]`, the loaded profile dict **with its
`current_skills` replaced by Step 2b's resolved list** -- entries without a
`skill_id` cover nothing -- the prior report's `gap_assessments` list --
`[]` if no prior report -- and the tracker rows list), then:

```bash
mkdir -p "${PROJECT_ROOT}/roadmaps/.tmp"
python3 -c "
import json, sys
sys.path.insert(0, '${CLAUDE_SKILL_DIR}/scripts')
from gap_state import reconcile_assessments

tmp = '${PROJECT_ROOT}/roadmaps/.tmp'
requirements = json.load(open(f'{tmp}/requirements.json'))
profile = json.load(open(f'{tmp}/profile.json'))
prior_assessments = json.load(open(f'{tmp}/prior_assessments.json'))
tracker_events = json.load(open(f'{tmp}/tracker_events.json'))

result = reconcile_assessments(
    requirements=requirements,
    profile=profile,
    prior_assessments=prior_assessments,
    tracker_events=tracker_events,
    target_role='<profile target_role>',
    target_level='<profile target_level, or empty string>',
    this_report_id='<a freshly generated uuid4 string for this run>',
)
print(json.dumps(result))
"
```

This prints the fresh `gap_assessments` list. Print to the terminal the
subset filtered to `status in {open, practiced}` as a heatmap (grouped by
tier, Critical first) so the user sees where they stand before the rest of
the run continues.

## Step 5 -- Resolve a track

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/resolution.py" resolve-track "<profile target_role>"
```

Prints the track id as a JSON string, or `null` if nothing matches. On
`null`: skip Step 6 (project selection) entirely for the rest of this run,
but still deliver the gap heatmap and Step 7's course resources, and state
plainly in the eventual report that no project templates exist yet for
this target (`resolved_track: null` in the frontmatter).

## Step 6 -- Plan projects (only if a track resolved)

`project_planner.py plan` takes its `--gaps` and `--profile-skills`
arguments as **paths to JSON files**, not inline JSON -- write them to
`${PROJECT_ROOT}/roadmaps/.tmp/` first:

- `gaps.json` -- the fresh `gap_assessments` list from Step 4.
- `profile_skills.json` -- Step 2b's **resolved** `current_skills` list
  (just that list, not the whole profile). It must be the resolved list:
  `plan` reads each entry's `skill_id`, never its free-text `skill`.

Then:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/project_planner.py" plan \
  --track "<resolved track id>" \
  --templates-root "${CLAUDE_SKILL_DIR}/templates" \
  --gaps "${PROJECT_ROOT}/roadmaps/.tmp/gaps.json" \
  --profile-skills "${PROJECT_ROOT}/roadmaps/.tmp/profile_skills.json" \
  --budget-hours <weekly_time_budget_hours * horizon_weeks>
```

(`horizon_weeks` defaults to `12` if unset on the profile, per
`reference/profile-schema.md`.) Prints
`{"projects": [...], "total_hours": ..., "budget_hours": ..., "shortfall": ...}`
-- `projects` is already in final sequenced order (topologically sorted,
capstone last); never re-sort it.

## Step 7 -- Course resources for remaining gaps

For each Critical/High-tier gap from Step 4 not covered by any selected
project's `covered_gap_skill_ids`, and for each selected project's unmet
`skill_prerequisites` (an empty `skill_prerequisites` list, or one where
every entry is already held, needs no resource search), run the exact
resource-search procedure defined in `find-courses/SKILL.md`. Read that
file and follow it in-process for this purpose -- it explicitly documents
this in-process usage at its top -- rather than re-describing the search
procedure here. Collect its structured output (name, URL, reason,
duration, cost per resource) instead of printing it, for use in Step 9's
report body.

## Step 8 -- Compose the Since-Last-Report diff

Skip this step entirely if Step 2 found no prior report. Otherwise, this
composition is the model's own job -- turning the structured data already
gathered above into prose -- not a script's: compare the prior report's
`gap_assessments` (loaded in Step 2) against the fresh ones from Step 4
(which gaps moved `open` -> `practiced` or -> `confirmed-closed`, which are
newly surfaced), and note relevant tracker events (from Step 2's `read`
call) that occurred since the prior report's `generated_at`. Follow
`reference/report-format.md`'s "Since Last Report" section for exact
content expectations.

## Step 9 -- Compose and save the report

Compose the report body per `reference/report-format.md`'s fixed section
order (Header, Since Last Report, Gap Heatmap, Sequenced Project Plan,
Course Resources, Suggested Study Order, Next Steps), and the frontmatter
per the schema in that same reference doc.

`report_state.py` has no CLI subcommand for writing a report -- only
`read`/`last`. Write the frontmatter dict and the composed body to
`${PROJECT_ROOT}/roadmaps/.tmp/` first, then:

```bash
python3 -c "
import json, sys
sys.path.insert(0, '${CLAUDE_SKILL_DIR}/scripts')
from report_state import write_report

tmp = '${PROJECT_ROOT}/roadmaps/.tmp'
frontmatter = json.load(open(f'{tmp}/frontmatter.json'))
body = open(f'{tmp}/body.md', encoding='utf-8').read()

path = write_report('${PROJECT_ROOT}/roadmaps', frontmatter, body)
print(path)
"
```

Then append a `report_generated` tracker row:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/tracker_io.py" append \
  "${PROJECT_ROOT}/tracker/skillpath_tracker.csv" \
  --occurred-at "<the same generated_at timestamp used in the frontmatter>" \
  --event-type report_generated \
  --item-name "<target_state text>" \
  --related-skill-ids "<pipe-separated skill ids covered by this run's gap_assessments, optional>" \
  --report-id "<the report_id from the frontmatter>"
```

### Recording completions (the `practiced` lifecycle state)

A gap only reaches `practiced` when a `project_completed` or
`course_completed` tracker row exists for it (or the profile already claims
it at practiced/proficient). Nothing else creates those rows, so record them
explicitly:

**If the user states at ANY point in the conversation -- during the initial
prompt, mid-run, or after the report is delivered -- that they completed a
project or a course, append the matching tracker row immediately.** Do not
wait for Step 9, and do not treat this as implied by report generation.

1. Resolve each skill the completed item covers to a canonical id (for a
   project template, use its `skill_tags` verbatim; otherwise run
   `resolution.py resolve-skill` on each skill the user names):
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/resolution.py" resolve-skill "<free text>"
   ```
2. Append the row, using `project_completed` for a hands-on project and
   `course_completed` for a course:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/tracker_io.py" append \
     "${PROJECT_ROOT}/tracker/skillpath_tracker.csv" \
     --occurred-at "<completion timestamp, UTC ISO8601; now if unstated>" \
     --event-type project_completed \
     --item-name "<the project or course name the user gave>" \
     --related-skill-ids "<pipe-separated resolved skill ids>" \
     --report-id "<report_id of the most recent report, or empty string>" \
     --notes "<what they built/finished, or empty>"
   ```
   (`--confirmed-for-target-role`/`--confirmed-for-target-level` are for
   `skill_confirmed` rows only -- leave them off here.)
3. Tell the user which skill ids the completion was recorded against, so a
   mis-mapped skill can be corrected. To move a skill the rest of the way
   from `practiced` to `confirmed-closed`, they run
   `/skillpath confirm "<skill>" "<evidence>"` (Step 1).

If Step 1 was an `override` run, ask now (once) whether to save the
override permanently; on an explicit yes, save via:

```bash
python3 -c "
import json, sys
sys.path.insert(0, '${CLAUDE_SKILL_DIR}/scripts')
from profile_io import save_profile

tmp = '${PROJECT_ROOT}/roadmaps/.tmp'
save_profile('${PROJECT_ROOT}/profile.yaml', json.load(open(f'{tmp}/profile_to_save.json')))
"
```

(The same `save_profile` snippet, with the freshly-assembled profile dict
from the conversational flow, is what Step 1's `first_run` branch uses to
write `profile.yaml` for the first time.)

Report the saved report's path and a brief summary to the user.
