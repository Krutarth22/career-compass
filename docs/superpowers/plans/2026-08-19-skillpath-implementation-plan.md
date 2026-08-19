# skillpath — Implementation Plan

Spec: `/Users/krutarthmajithia/.claude-personal/plans/pure-finding-island.md` (the
approved architecture doc — the binding authority for anything this plan doesn't spell
out explicitly). This plan breaks that architecture into ordered, independently
implementable tasks.

## Global Constraints (apply to every task)

- Python `>=3.11`, stdlib + `pyyaml` only (no other third-party deps in `scripts/`).
  `pytest` for tests.
- All runtime scripts live under `.claude/skills/skillpath/scripts/`. All tests live
  under `tests/` at repo root and import scripts via `sys.path` manipulation or a
  `conftest.py` that adds `.claude/skills/skillpath/scripts/` to `sys.path` — set this
  up once in Task 1 so every later task's tests just `import profile_io` etc.
- No script ever hardcodes a path — every path is a function argument or CLI flag.
  Every CLI entrypoint uses `argparse` and prints results as JSON to stdout (so
  SKILL.md, driven by an LLM via `Bash`, can parse them) and errors to stderr with a
  non-zero exit code.
- Every module is a pure-function library first, CLI wrapper second — write the CLI
  as a thin `if __name__ == "__main__":` block calling the library functions, so tests
  call functions directly, not by shelling out.
- Timestamps: UTC, ISO 8601, always via `datetime.now(timezone.utc)` — never naive
  `datetime.now()`.
- Do not implement `.claude/skills/skillpath/SKILL.md`'s prose/orchestration logic
  early — it is Task 8, after every script and template it calls exists and is tested.
- Commit after each task with a message describing what was added. Run the full test
  suite (`pytest tests/`) before committing and report the pass count.

---

## Task 1: Repo scaffolding

Create the skeleton so every later task has somewhere to put its files.

**Create:**
- `.gitignore` containing (at minimum): `profile.yaml`, `roadmaps/report-*.md`,
  `tracker/skillpath_tracker.csv`, `__pycache__/`, `*.pyc`, `.pytest_cache/`,
  `.venv/`, `roadmaps/.tmp/`. Do **not** ignore the `.example` files or `roadmaps/` /
  `tracker/` directories themselves — only the personal-data files inside them (use
  `roadmaps/report-*.md` not `roadmaps/`, so `roadmaps/.gitkeep` can still be tracked).
- `pyproject.toml` declaring `pyyaml` and `pytest` as dependencies, Python
  `>=3.11`, project name `skillpath`.
- `LICENSE` — MIT license, copyright year 2026.
- `.github/workflows/ci.yml` — a GitHub Actions workflow that on `push`/`pull_request`
  sets up Python 3.11+, installs the project (`pip install -e .` or equivalent using
  `pyproject.toml`), and runs `pytest tests/`.
- `roadmaps/.gitkeep` (empty file, so the directory exists in git despite its contents
  being ignored).
- `tracker/skillpath_tracker.csv.example` with header row:
  `occurred_at,event_type,item_name,related_skill_ids,report_id,notes,confirmed_for_target_role,confirmed_for_target_level`
  and 2-3 example rows showing a `report_generated`, a `project_completed`, and a
  `skill_confirmed` row (the last with the two `confirmed_for_*` columns populated,
  the others with those two columns blank).
- `profile.yaml.example` — raw YAML (no frontmatter), following this exact schema,
  filled in with a plausible example person (e.g. a mechanical engineer moving into
  data-adjacent AI/ML work):
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
- `tests/conftest.py` that inserts
  `<repo-root>/.claude/skills/skillpath/scripts` at the front of `sys.path` (compute
  the repo root via the file's own location, not cwd) so every test file in `tests/`
  can `import profile_io`, `import resolution`, etc. directly.
- Empty placeholder dirs (via `.gitkeep` or the module files that later tasks will
  add): `.claude/skills/skillpath/scripts/`, `.claude/skills/skillpath/reference/`,
  `.claude/skills/skillpath/templates/ai-ml-engineer/`, `.claude/skills/find-courses/`.

**Verify:** `git status` shows the expected files; `.gitignore` correctly matches
`roadmaps/report-2026-01-01-test.md` and `tracker/skillpath_tracker.csv` (spot-check
with `git check-ignore -v` on made-up paths — no need for real files yet) but does
**not** match `profile.yaml.example` or `roadmaps/.gitkeep`.

---

## Task 2: Reference docs (taxonomy, profile schema, track aliases)

All under `.claude/skills/skillpath/reference/`. These are read by both SKILL.md (as
prose the LLM reads) and by Task 4's `resolution.py` (parsed as YAML), so the YAML
blocks inside each file must be valid, parseable YAML, not just illustrative
Markdown.

**`skill-taxonomy.md`:** a checked-in registry. Format: a YAML list under a fenced
`yaml` code block (so `resolution.py` can load it with
`yaml.safe_load` after stripping the Markdown fence, or store the YAML in a sibling
`skill-taxonomy.yaml` loaded by the doc via include-by-reference — your call, but
`resolution.py` in Task 4 must be able to load it programmatically without
Markdown-parsing tricks, so prefer a plain `skill-taxonomy.yaml` file with `.md` prose
around/above it explaining the two enforcement levels). Each entry:
`{id: string, display_name: string, synonyms: [string]}`. Seed it with **at least**
one entry per `skill_tags`/`skill_prerequisites` value that Task 7's templates will
use: `retrieval-augmented-generation, vector-databases, embeddings, eval-harnesses,
prompt-engineering, python, llm-api-basics, model-serving, api-design, docker,
ml-monitoring, mlops-basics, ml-fundamentals`, plus a reasonable additional set likely
to surface in live research: `statistics, sql, feature-engineering, model-training,
lora-finetuning, agent-orchestration, tool-use, workflow-orchestration,
data-pipelines, ci-cd`. Document inline (prose above the YAML) the two enforcement
levels: template `skill_tags` must resolve to an existing id (hard lint fail
otherwise, enforced in Task 5); live research output that doesn't match becomes a
provisional `unmapped: true` ID and is **never** auto-written back to this file — a
human adds entries via PR per `CONTRIBUTING.md`.

**`track-aliases.md`** (or `.yaal` sibling, same pattern as above — pick one
convention and use it consistently across both files): one track,
```yaml
ai-ml-engineer:
  aliases: ["ai engineer", "ml engineer", "machine learning engineer", "ai/ml engineer", "applied scientist (ai)", "mle"]
```
Document the resolution rule in prose: normalize `target_role` (lowercase, strip
level words like "junior"/"senior"/"mid"), match against alias lists by exact or
substring match only (no fuzzy/semantic matching) — implemented in Task 4.

**`profile-schema.md`:** prose documentation of the `profile.yaml` schema (same schema
as Task 1's `profile.yaml.example`), plus the argument/profile merge rule written out
in full:
- No `profile.yaml` exists → always run the profile-creation flow, regardless of
  whether CLI args were supplied; supplied args pre-fill it; write `profile.yaml` at
  the end either way.
- `profile.yaml` exists and args are supplied → this-run-only override, never
  silently overwritten; ask once after the run whether to save permanently.
- `profile.yaml` exists, no args → use the file as-is.

**Verify:** `python -c "import yaml; yaml.safe_load(open('.claude/skills/skillpath/reference/skill-taxonomy.yaml'))"` (or wherever you put the YAML) parses without error, likewise for the track-aliases YAML.

---

## Task 3: State I/O modules — `profile_io.py`, `tracker_io.py`, `report_state.py`

All three live in `.claude/skills/skillpath/scripts/`. Write full unit tests in
`tests/test_tracker_io.py` and `tests/test_report_state.py` (profile_io gets its
tests in Task 4's `test_resolution.py`, per the plan's original test split — put a
`test_profile_io.py` instead if that split reads more naturally; either is fine as
long as every function below has a covering test).

### `profile_io.py`
- `load_profile(path) -> dict | None` — returns `None` if the file doesn't exist,
  parsed dict otherwise (raw `yaml.safe_load`).
- `save_profile(path, profile: dict) -> None` — writes the dict as YAML, setting
  `last_updated` to today's UTC date.
- `merge_profile(existing: dict | None, args: dict) -> tuple[dict, str]` — implements
  the three-branch merge rule exactly as in Task 2's `profile-schema.md`. `args` is
  `{"current_state": str | None, "target_state": str | None}` (from parsed CLI
  arguments). Returns `(effective_profile_dict, mode)` where `mode` is one of
  `"first_run"`, `"override"`, `"as_is"` — the caller (SKILL.md) uses `mode` to decide
  whether to run the conversational profile-creation flow or ask about saving an
  override. This function does not do any I/O itself — it's pure, given the loaded
  profile and parsed args; `load_profile`/`save_profile` are separate so tests can
  check the merge logic without touching disk.

### `tracker_io.py`
CSV columns (in this order): `occurred_at, event_type, item_name, related_skill_ids,
report_id, notes, confirmed_for_target_role, confirmed_for_target_level`.
`event_type` allowed values: `report_generated, project_started, project_completed,
course_started, course_completed, skill_confirmed`.
- `append_row(csv_path, occurred_at, event_type, item_name, related_skill_ids: list[str], report_id, notes="", confirmed_for_target_role="", confirmed_for_target_level="") -> None`
  — validates `event_type` against the allowed set (raise `ValueError` otherwise),
  joins `related_skill_ids` with `|`, appends via the stdlib `csv` module (never
  string concatenation — this must handle commas/quotes in `notes` correctly), creates
  the file with the header row if it doesn't exist yet.
- `read_rows(csv_path, since: str | None = None, event_types: list[str] | None = None) -> list[dict]`
  — returns rows as dicts (keys = column names, `related_skill_ids` split back into a
  list), filtered by `occurred_at >= since` (ISO string comparison is fine given the
  fixed format) and by `event_type in event_types` when those args are given. Must not
  crash on a hand-edited/malformed row — skip it and continue (log nothing fancy,
  just don't raise).
- `get_last_report_meta(roadmaps_dir) -> dict | None` — delegates to
  `report_state.get_last_report()` (Task 3, same task) for the actual lookup; this
  function exists so tracker-focused callers don't need to import `report_state`
  directly. Returns `None` if no report exists.

### `report_state.py`
Report frontmatter schema (YAML front-matter block at the top of the `.md` file,
followed by the human-readable rendered body):
```yaml
report_id: <uuid4 string>
generated_at: <UTC ISO8601 timestamp, with colons>
current_state: string
target_state: string
resolved_track: string | null
research_confidence: high | medium | low
target_requirements:
  - skill_id: string
    unmapped: boolean
    category: hard | tooling | domain | soft | credential
    frequency_signal: number
    sources:
      - url: string
        type: posting | article | forum | interview-prep | docs
        title: string
        company: string | null
        role_level: string | null
        location: string | null
        posted_at: date | null
        accessed_at: <UTC ISO8601 timestamp>
gap_assessments:
  - skill_id: string
    tier: Critical | High | Medium | Low
    status: open | practiced | confirmed-closed
    first_seen_at: <UTC ISO8601 timestamp>
    first_seen_report_id: <uuid4 string>
```
- `write_report(roadmaps_dir, frontmatter: dict, body_markdown: str) -> str` (returns
  the full path written). Filename:
  `report-<YYYYMMDDTHHMMSS.ffffff>Z-<report_id[:8]>-<target-slug>.md` where the
  timestamp portion is **basic ISO 8601 with microseconds, no colons or dashes**
  (derive it from `frontmatter["generated_at"]`, which itself is stored in full
  human-readable ISO form with colons/dashes — only the filename is compacted).
  `target-slug` = `frontmatter["target_state"]` lowercased, non-alphanumeric runs
  replaced with a single `-`, stripped of leading/trailing `-`. Writes the YAML
  frontmatter between `---` delimiters followed by `body_markdown`.
- `read_report(path) -> dict` — parses a report file, returns its frontmatter dict
  (raises if the file has no valid frontmatter block).
- `get_last_report(roadmaps_dir) -> dict | None` — lists `roadmaps/report-*.md`,
  picks the newest by the embedded filename timestamp (not filesystem mtime), returns
  its parsed frontmatter via `read_report`, or `None` if the directory has no report
  files, **or** if the newest one fails to parse (corrupt file) — log nothing fancy,
  just return `None` so callers degrade to "no diff" gracefully, per the plan's
  explicit "never a crash" rule.

**Verify:** `pytest tests/test_tracker_io.py tests/test_report_state.py -v` — every
function above has at least one passing test, including the malformed-row and
corrupt/missing-report degradation cases explicitly.

---

## Task 4: `resolution.py` + `gap_state.py`

### `resolution.py`
- `resolve_skill(text: str, taxonomy: list[dict]) -> dict` returns
  `{"id": str, "unmapped": bool}`. Normalize `text` (lowercase, strip whitespace).
  Match against each taxonomy entry's `id` and `synonyms` (case-insensitive exact or
  clear-substring match — no fuzzy scoring). On no match, return a **provisional
  ID**: the normalized text with non-alphanumeric runs collapsed to single hyphens,
  and `unmapped: true`. `taxonomy` is the already-loaded list of dicts from Task 2's
  `skill-taxonomy.yaml` (this function does not load the file itself — pass it in, so
  tests can use small synthetic taxonomies).
- `resolve_track(target_role: str, track_aliases: dict) -> str | None` — normalize
  `target_role` (lowercase; strip standalone level words `junior|mid|senior|lead|
  principal|staff` as whole words, not substrings — `"principal"` should not strip
  inside `"principal engineer"` incorrectly... actually it should strip the word
  `"principal"` itself when it appears as a separate word, leaving `"engineer"`; be
  careful only to strip whole-word matches, e.g. `re.sub(r'\b(junior|mid|senior|lead|
  principal|staff)\b', '', text, flags=re.IGNORECASE)`), then match against each
  track's `aliases` list (case-insensitive exact or substring). Returns the track key
  (e.g. `"ai-ml-engineer"`) or `None`. `track_aliases` is the already-loaded dict from
  Task 2's track-aliases YAML.
- Small CLI wrapper: `resolve-track "<target_role>"` and `resolve-skill "<text>"`
  subcommands that load the reference YAML from a `--taxonomy`/`--track-aliases` path
  argument (defaulting to the real reference file paths relative to the script's own
  location via `${CLAUDE_SKILL_DIR}`-equivalent — i.e. `Path(__file__).parent.parent /
  "reference" / "skill-taxonomy.yaml"`) and print the result as JSON.

### `gap_state.py`
Single entrypoint:
```
reconcile_assessments(
    requirements: list[dict],       # this run's target_requirements (Task 3's schema)
    profile: dict,                  # loaded profile.yaml dict
    prior_assessments: list[dict],  # prior report's gap_assessments, or []
    tracker_events: list[dict],     # rows from tracker_io.read_rows()
    target_role: str,
    target_level: str,
) -> list[dict]   # fresh gap_assessments, Task 3's schema
```
Logic, exactly as specified (implement each bullet as a distinct, testable step —
don't collapse into one opaque loop):
1. For each `requirement` in `requirements`: look up a matching entry in
   `prior_assessments` by `skill_id`. If found, carry forward its `first_seen_at` and
   `first_seen_report_id` unchanged; otherwise set both to "now" (pass `now` as an
   optional injectable argument defaulting to `datetime.now(timezone.utc)`, so tests
   are deterministic) and a `report_id` placeholder the caller fills in (accept
   `this_report_id: str` as a parameter too).
2. Compute Pass-1 coverage: does `profile["current_skills"]` contain this `skill_id`
   at `proficiency in {"practiced", "proficient"}`? (Match by exact `skill_id` — the
   caller is responsible for having already resolved profile skill text to IDs via
   `resolution.resolve_skill` before calling this function; `gap_state.py` works
   purely on IDs, no text matching.)
3. Apply `tracker_events`, filtered to `occurred_at >= first_seen_at` for this skill:
   any `project_completed`/`course_completed` event whose `related_skill_ids`
   includes this `skill_id` sets `status = "practiced"` **unless** already
   `confirmed-closed`. The most recent (`max` by `occurred_at`) `skill_confirmed`
   event for this `skill_id` sets `status = "confirmed-closed"` **only if** its
   `confirmed_for_target_role == target_role` and
   `confirmed_for_target_level == target_level` (exact string match); otherwise that
   event does not affect status (it's ignored for status purposes — the caller/report
   layer is responsible for rendering the "confirmed previously for `<old target>`"
   note using the raw tracker row, not this function's output).
4. If none of steps 2-3 produced a status, default to `"open"`.
5. Assign `tier` — **this function does not compute tiering** (that's the LLM's
   frequency/centrality judgment call per the plan); accept `tier` as already present
   on each `requirement` dict (i.e. Step 4 of `/skillpath` passes in requirements that
   already carry a `tier` key it computed) and just copy it through.
6. Return the list of `{skill_id, tier, status, first_seen_at, first_seen_report_id}`
   dicts, one per input requirement, in the same order as `requirements`.

Write `tests/test_resolution.py` covering: `resolve_skill` exact match, synonym
match, and provisional/unmapped fallback; `resolve_track` alias match and no-match
case, including the level-word-stripping edge case (`"senior ai engineer"` and
`"ai engineer"` both resolve to the same track); and `reconcile_assessments` with one
dedicated test per transition — open→practiced (via a `project_completed` event),
practiced→confirmed-closed (via a target-matching `skill_confirmed` event),
confirmed-closed staying closed on a repeat run with no target change,
confirmed-closed **not** carrying forward when `target_role`/`target_level` differ
from the event's `confirmed_for_*` fields (falls back through steps 2-4 instead), and
`first_seen_at`/`first_seen_report_id` carrying forward unchanged across all of the
above (assert the value is literally identical across two calls, not just present).

**Verify:** `pytest tests/test_resolution.py -v` — all listed cases present and
passing.

---

## Task 5: `lint_templates.py` (+ shared template loader)

Create `template_loader.py` in the same `scripts/` directory as a small shared
helper (both this task and Task 6 depend on it):
- `load_template(path) -> dict` — parses a template `.md` file's YAML frontmatter
  (between `---` delimiters) plus its body sections, returns
  `{"frontmatter": {...}, "sections": {"Production Workflow Mirrored": "...", ...}}`
  (sections keyed by their `##` heading text, values = the raw text under that
  heading up to the next `##`).
- `load_track(track_dir) -> list[dict]` — loads every `*.md` file in a track
  directory **except** `TEMPLATE.md`, returns a list of `load_template` results, each
  annotated with `_filename` (basename) for downstream reference.

`lint_templates.py` — checks, each as its own function so `tests/test_lint_templates.py`
can call them individually and assert pass/fail on fixtures:
- `check_frontmatter_valid(template) -> list[str]` (returns a list of error strings,
  empty = pass): YAML parses; required fields present and **correctly typed** —
  `title, track, difficulty_tier, estimated_hours, role, skill_tags,
  skill_prerequisites, project_prerequisites, prerequisite_learning_hours` all
  present (empty lists are valid for `skill_prerequisites`/`project_prerequisites`,
  a **missing** key is not); `difficulty_tier in {beginner, intermediate, advanced}`;
  `role in {core, capstone}`; `estimated_hours` is an int `> 0`;
  `prerequisite_learning_hours` is an int `>= 0`.
- `check_track_matches_directory(template, track_dir_name) -> list[str]`.
- `check_skill_ids_known(template, taxonomy_ids: set[str]) -> list[str]` — every
  `skill_tags` and `skill_prerequisites` entry must be in `taxonomy_ids`.
- `check_sections_present(template) -> list[str]` — required `##` headings:
  `Production Workflow Mirrored, What You'll Build, Student-Scope Notes, Steps,
  Extension Ideas, Skills Demonstrated`.
- `check_project_prerequisites_valid(all_templates: list[dict]) -> list[str]` (a
  whole-track check, not per-template): every `project_prerequisites` entry is a real
  sibling filename; no dangling references; no cycles (build the graph and run a
  cycle check); **no `core` template lists the track's `capstone` template in its own
  `project_prerequisites`** (this is what guarantees the capstone can always be
  placed last).
- `check_exactly_one_capstone(all_templates: list[dict]) -> list[str]` — exactly one
  `role: capstone` in the track, not zero, not two.

`lint_all(templates_root, taxonomy_ids: set[str]) -> list[str]` — orchestrates all of
the above across every track directory under `templates_root`, returns the combined
error list (empty = everything passes). CLI: prints each error on its own line to
stderr and exits 1 if any; exits 0 with "OK" to stdout otherwise.

**Write `tests/test_lint_templates.py`** with fixture templates constructed in-test
(temp files, not depending on Task 7's real templates, which don't exist yet) for
**both the happy path and every failure mode**: an unknown `skill_tag`/
`skill_prerequisite`, a missing-vs-empty-list distinction (empty list passes, missing
key fails), a dangling `project_prerequisite`, a `project_prerequisite` cycle, a core
template listing the capstone as its own prerequisite, a track with zero capstones, a
track with two capstones, a missing required `##` section, `estimated_hours = 0`
(must fail, `> 0` required), `prerequisite_learning_hours = 0` (must pass, `>= 0`
allowed).

**Verify:** `pytest tests/test_lint_templates.py -v` — all fixture cases pass/fail as
specified.

---

## Task 6: `project_planner.py`

Depends on Task 5's `template_loader.py` (import `load_track`) and Task 4's
`gap_state.py` output shape (`gap_assessments`).

Implements the deterministic project-selection algorithm from the spec, as discrete,
individually testable functions — do not collapse into one function that's hard to
unit test:

- `filter_gap_assessments(gap_assessments) -> list[dict]` — keep only
  `status in {"open", "practiced"}` and `tier in {"Critical", "High", "Medium"}`
  (Low-tier never drives selection).
- `gap_weight(gap: dict) -> float` — `tier_weight = {"Critical": 8, "High": 4,
  "Medium": 1}[gap["tier"]]`, `status_multiplier = 0.5 if gap["status"] == "practiced"
  else 1.0`, returns their product.
- `candidate_pool(core_templates: list[dict], filtered_gaps: list[dict]) -> list[dict]`
  — core templates (role == "core") whose `skill_tags` intersect the filtered gaps'
  `skill_id`s.
- `unmet_prerequisite_hours(template, profile_skill_ids_at_or_above_practiced: set[str]) -> int`
  — `template["prerequisite_learning_hours"]` if any of its `skill_prerequisites` is
  **not** in the given set, else `0` (all prerequisites already held → no learning
  time needed). `profile_skill_ids_at_or_above_practiced` is precomputed by the
  caller from the profile (skills at `practiced` or `proficient`).
- `select_core_projects(candidates, filtered_gaps, profile_skill_ids, budget_hours) -> list[dict]`
  — the greedy marginal-coverage loop exactly as specified: repeatedly score every
  remaining candidate by the sum of `gap_weight` for gaps it covers that no
  already-selected candidate covers (marginal coverage — recompute after each pick);
  pick the highest score; tie-break by `(estimated_hours +
  unmet_prerequisite_hours(candidate, profile_skill_ids))` ascending, then by
  `_filename` alphabetically; auto-select the candidate's own `project_prerequisites`
  first (recursively) if not already selected, counting their hours too; stop when
  4 core projects are selected (the default cap) **or** the running hour total would
  exceed `budget_hours` **or** every remaining candidate has marginal score 0 — except
  that once the 4-project cap is hit, allow exactly one more (a 5th) only if the
  unused budget remaining is still `>= 0.5 * budget_hours` and at least one remaining
  candidate has positive marginal score; when that 5th-project exception fires, mark
  it in the return value (e.g. an extra key `"generous_budget_exception": true` on
  that project's dict) so the report layer can state it explicitly. Return value:
  ordered list of selected core-project dicts (selection order, not yet the final
  topological order), each annotated with which gap `skill_id`s it was chosen to
  cover (for report rationale) and its `unmet_prerequisite_hours`.
- `sequence_projects(selected_core: list[dict], capstone: dict | None) -> list[dict]`
  — topologically sorts `selected_core` (plus the capstone's own
  `project_prerequisites`, auto-selected into the core set the same way as above if
  not already present) by `project_prerequisites`, then appends `capstone` itself as
  the final element if one was provided (the resolved track has a capstone) — the
  capstone template itself is always the last item, never reordered by the
  topological sort; raise a clear exception (don't silently resolve) if a cycle is
  detected among the core set — this indicates a Task 5 linter gap, not a runtime
  case to paper over.
- `plan(track_templates: list[dict], gap_assessments: list[dict], profile: dict, budget_hours: float) -> dict`
  — the top-level orchestration calling the above in order; returns
  `{"projects": [...ordered final sequence...], "total_hours": float,
  "budget_hours": float, "shortfall": bool}` — `shortfall` is `true` when fewer than
  2 core projects could be selected within budget (the report layer uses this to
  render the "budget supports N of the usual 2-4 core projects" note).

CLI: `plan --track <name> --gaps <path.json> --profile-skills <path.json>
--budget-hours N` loads a track via `template_loader.load_track`, reads the two JSON
files (`gaps.json` = a `gap_assessments`-shaped list, `profile-skills.json` = the
profile's `current_skills` list), calls `plan(...)`, prints the result as JSON.

**Write `tests/test_project_planner.py`** (or fold into `test_resolution.py` if you
prefer one file for all deterministic-module tests — either is fine, just cover
everything): marginal-coverage scoring picks the multi-gap-covering template over two
single-gap templates when scores warrant it; the documented tie-break
(hours-then-filename) resolves a constructed tie deterministically and repeatably
(run the selection twice on identical input, assert identical output); a
`project_prerequisites` auto-inclusion case; a case where a `skill_prerequisite` is
already satisfied by the profile and does **not** add its `prerequisite_learning_hours`
to the running total; the 4-core-project cap; the 5th-project generous-budget
exception firing only when `>= 50%` of budget remains and not firing otherwise; a
0-1-core-project shortfall case with `shortfall: true` in the result; the capstone
always last regardless of the core set's topological order; a cycle among core
`project_prerequisites` raising rather than silently resolving.

**Verify:** `pytest tests/test_project_planner.py -v` (or wherever you put these) —
every case above passing.

---

## Task 7: Project templates

`.claude/skills/skillpath/templates/TEMPLATE.md` — the schema doc (frontmatter
fields + required body sections, as documented in Task 5's checks), meant for human
contributors, not parsed by code.

`.claude/skills/skillpath/templates/ai-ml-engineer/` — 7 templates. Two are fully
specified below verbatim (use exactly this content); author the remaining 5
following the same schema and the pattern these two set (Production Workflow
Mirrored / What You'll Build / Student-Scope Notes / Steps / Extension Ideas / Skills
Demonstrated), each core, difficulty `beginner` or `intermediate`, `estimated_hours`
in the 10-25 range, with real `skill_tags` (all present in Task 2's taxonomy — add any
you need to `skill-taxonomy.yaml` in this task if the taxonomy is missing something
plausible, since Task 2 seeded it generously but not exhaustively) and sensible
`skill_prerequisites`/`prerequisite_learning_hours` (don't leave every remaining
template's prerequisites empty — at least 2 of the 5 should declare a
`skill_prerequisites` entry, so Task 6's "unmet prerequisite hours" logic has real
data to exercise beyond the two worked examples).

### `rag-pipeline-with-eval.md` (verbatim)

```markdown
---
title: "RAG Pipeline with Evaluation Harness"
track: "ai-ml-engineer"
difficulty_tier: "intermediate"
estimated_hours: 20
role: "core"
skill_tags: ["retrieval-augmented-generation", "vector-databases", "embeddings", "eval-harnesses", "prompt-engineering", "python"]
skill_prerequisites: ["python", "llm-api-basics"]
project_prerequisites: []
prerequisite_learning_hours: 8
---

# RAG Pipeline with Evaluation Harness

## Production Workflow Mirrored
1. Document ingestion & preprocessing
2. Chunking strategy
3. Embedding & indexing into a vector store
4. Retrieval (top-k, reranking)
5. Generation (prompt construction, LLM call)
6. Evaluation harness (retrieval precision/recall, answer faithfulness)
7. Basic deploy (simple API endpoint) & lightweight monitoring (latency, failure logging)

## What You'll Build
A question-answering system over a document set of your choice that retrieves
relevant chunks and generates grounded answers, with a small evaluation suite that
scores the system on a hand-built question set so you can quantify quality, not just
eyeball it.

## Student-Scope Notes
- Local/open-source vector store (Chroma, FAISS) instead of a managed production
  service — same retrieval concepts, no infra cost or ops overhead.
- Eval set is ~20-30 hand-labeled Q&A pairs, not a large annotated benchmark.
- "Deploy" means a local FastAPI/Flask endpoint hit with curl, not a scaled cloud
  deployment — the API-boundary and monitoring concepts are the point, not infra
  (that's a separate template).

## Steps
1. Pick a document set (10-50 documents) relevant to a domain you care about.
2. Build ingestion + chunking (try 2 strategies, compare).
3. Embed chunks and index into a vector store.
4. Build retrieval (plain top-k, then add reranking).
5. Build generation: grounded prompt from retrieved chunks, call an LLM.
6. Hand-write 20-30 Q&A pairs with expected answers/source chunks.
7. Build an eval script scoring retrieval hit-rate and answer faithfulness.
8. Wrap in a minimal API endpoint; log latency and failures to a file.
9. Write up: chunking/retrieval choices and why, eval results, what you'd change for scale.

## Extension Ideas
- Add hybrid search (keyword + vector).
- Add a feedback loop flagging low-confidence answers for human review.
- Swap the local vector store for a managed one and note the tradeoffs.
- Add basic cost/latency tracking dashboards.

## Skills Demonstrated
- Retrieval-augmented generation system design
- Vector database usage and embedding pipelines
- Building an evaluation harness for a generative system
- Prompt engineering for grounded generation
- Basic API deployment and monitoring instincts
```

### `ml-model-serving-api.md` (verbatim)

```markdown
---
title: "ML Model Serving API with Monitoring"
track: "ai-ml-engineer"
difficulty_tier: "intermediate"
estimated_hours: 15
role: "core"
skill_tags: ["model-serving", "api-design", "docker", "ml-monitoring", "python", "mlops-basics"]
skill_prerequisites: ["python", "ml-fundamentals"]
project_prerequisites: []
prerequisite_learning_hours: 10
---

# ML Model Serving API with Monitoring

## Production Workflow Mirrored
1. Train/select a model
2. Wrap in a versioned inference API
3. Containerize
4. Input validation & error handling
5. Basic monitoring (latency, request volume, prediction drift signal)
6. Simple load test

## What You'll Build
A trained classification or regression model served behind a REST API,
containerized, with request logging and a basic dashboard showing latency and
prediction distribution over time.

## Student-Scope Notes
- Single-instance Docker container, not a Kubernetes deployment.
- Monitoring is logged-metrics + a local dashboard, not a full observability stack.
- Load test is a basic concurrent-request script, not full performance engineering.

## Steps
1. Train or pick a pretrained model with a clear input/output contract.
2. Build a FastAPI (or similar) inference endpoint with input validation.
3. Containerize with Docker; document how to run it.
4. Add request/response logging (timestamp, latency, input summary, output).
5. Build a small dashboard/script reading the logs: latency over time + prediction
   distribution (a drift proxy).
6. Run a basic load test; record p50/p95 latency.
7. Write up: API contract, how you'd know if the model started behaving badly in
   production.

## Extension Ideas
- Add a shadow-deployment pattern.
- Add real drift detection (e.g. population stability index).
- Add model versioning/rollback support to the API.

## Skills Demonstrated
- Model serving and API design for ML systems
- Containerization
- Basic MLOps monitoring instincts
- Load testing fundamentals
```

### Remaining 5 templates (author these)

- `llm-finetuning-lora.md` — core. Fine-tuning an open LLM with LoRA on a small
  custom dataset; skill_tags should include something like `lora-finetuning`,
  `model-training`, `python`; reasonable `skill_prerequisites` (e.g. `python`,
  `ml-fundamentals`) and non-zero `prerequisite_learning_hours`.
- `feature-store-lite.md` — core. A minimal feature store / feature-engineering
  pipeline (offline batch features + a simple online lookup); tags around
  `feature-engineering`, `data-pipelines`, `python`.
- `ml-pipeline-orchestration.md` — core. Orchestrating a multi-step ML pipeline
  (e.g. with a lightweight tool or plain Python DAG) with retries/logging; tags
  around `workflow-orchestration`, `data-pipelines`, `ci-cd`.
- `llm-agent-tool-use.md` — core. An LLM agent that calls tools/functions to
  accomplish a task; tags around `agent-orchestration`, `tool-use`,
  `prompt-engineering`. This one should NOT be a `project_prerequisites` of the
  capstone (the capstone's prerequisites are fixed to the two templates below) — it's
  referenced only in the capstone's own Extension Ideas, per the spec.
- `production-ai-system-capstone.md` — **`role: capstone`**, the only one in the
  track. `project_prerequisites: ["rag-pipeline-with-eval.md",
  "ml-model-serving-api.md"]` (fixed, AND semantics — do not attempt an OR/either-or
  framing). Requires deploying the RAG pipeline behind the serving API, adding
  monitoring/drift-detection as one required stage (not the whole project), and a
  portfolio write-up connecting the pieces end-to-end. Its Extension Ideas section
  should mention wiring in the agent-tool-use project as an alternative/addition to
  the RAG pipeline for readers who want to go further.

**Verify:** run Task 5's linter against this directory —
`python .claude/skills/skillpath/scripts/lint_templates.py` (or equivalent invocation
per how you wrote its CLI) — must report zero errors, confirming: all 7 templates
valid, exactly one capstone, no dangling/cyclic `project_prerequisites`, no core
template lists the capstone as its own prerequisite, every `skill_tags`/
`skill_prerequisites` value resolves in the taxonomy from Task 2 (add missing taxonomy
entries in this task if needed — don't invent a skill tag with nowhere to resolve).

---

## Task 8: `SKILL.md` files

### `.claude/skills/skillpath/SKILL.md`

Frontmatter: explicit-invocation only (find and use Claude Code's actual
current mechanism for this — the equivalent of `disable-model-invocation: true` —
check current Claude Code slash-command/skill docs conventions if unsure; this
skill writes personal files to disk and must never fire from ambient conversation).
Argument handling: Claude Code positional arguments are zero-indexed — `$0` = first
argument, `$1` = second. `/skillpath "<current-state>" "<target-state>"` → `$0` =
current-state, `$1` = target-state. `/skillpath confirm "<skill>" "<evidence>"` →
`$0` = the literal `confirm`, `$1` = skill, `$2` = evidence (optional — if absent,
ask conversationally once for evidence before appending the tracker row, an empty
answer is fine). If the expected positional arguments are empty for either form,
fall back to a conversational flow.

Every reference to bundled resources (`templates/`, `reference/*`, the six
`scripts/*.py`) uses `${CLAUDE_SKILL_DIR}`-relative paths. Runtime state paths
(`profile.yaml`, `tracker/skillpath_tracker.csv`, `roadmaps/`) resolve relative to
the **project root**, defined as the output of `git rev-parse --show-toplevel`,
falling back to the invocation's cwd if that command fails. Every `Bash` call to one
of the six scripts uses its resolved `${CLAUDE_SKILL_DIR}/scripts/...` path — never a
bare `scripts/...` relative path.

Write the orchestration prose covering these 9 steps (this is the model-facing
instruction document — write it as clear imperative prose an LLM will follow, calling
out exactly which script/CLI command to run at each deterministic step, consistent
with every function signature and CLI flag defined in Tasks 3-6):

1. Parse args (`$0`/`$1`, or `confirm` sub-command with `$0=confirm, $1, $2`).
   For `confirm`: call `resolution.py resolve-skill`, then `tracker_io.py`'s
   append-row CLI with `event_type=skill_confirmed` and the profile's current
   `target_role`/`target_level` as `confirmed_for_*`; report success and stop — do
   not continue to research/report generation.
   For the main flow: call `profile_io.py`'s merge logic (via its CLI) to get
   `mode` (`first_run` / `override` / `as_is`); if `first_run`, run the
   conversational profile-creation flow, then save via `profile_io.py`.
2. Load state: `profile_io.py load`, `tracker_io.py read-rows`,
   `report_state.py get-last-report`.
3. Research target requirements per the research protocol (see
   `reference/research-protocol.md` — **write this reference file now if it doesn't
   already exist**: queries incorporating `target_role`/`target_level`/`location`
   from the profile, current-year market queries + evergreen-exempt canonical docs,
   ≥4 real postings + ≥2 practitioner sources evidence bar, confidence scoring
   high/medium/low). This step's *research* is genuinely the LLM's job (WebSearch +
   judgment) — there is no script for it.
4. Tier each requirement (Critical/High/Medium/Low by frequency + centrality, capped
   at Medium when confidence is low — LLM judgment), then call
   `gap_state.py reconcile_assessments` (via its CLI, passing the tiered requirements,
   loaded profile, prior report's `gap_assessments`, and tracker rows) to get the
   fresh `gap_assessments`. Print the `status in {open, practiced}` filtered heatmap
   to the terminal.
5. Call `resolution.py resolve-track` on `target_role`. No match → skip project
   selection, still deliver the heatmap and course resources, state plainly no
   templates exist yet for this target.
6. If a track resolved: call `project_planner.py plan` with the track's templates,
   the fresh `gap_assessments`, the profile's skills, and
   `weekly_time_budget_hours * horizon_weeks` as the budget.
7. For each Critical/High gap not covered by a selected project, and each selected
   project's unmet `skill_prerequisites`, run the resource-search procedure defined
   in `find-courses/SKILL.md` (reference it explicitly, don't re-describe it here).
8. Compose the Since-Last-Report diff from the prior and fresh `gap_assessments` plus
   tracker events (skip entirely if no prior report) — this composition (turning
   structured data into report prose) is the LLM's job; the underlying data all came
   from deterministic calls above.
9. Compose and save the report via `report_state.py write-report`; append a
   `report_generated` row via `tracker_io.py`.

Also write `reference/report-format.md` now if it doesn't already exist, documenting
the human-readable report body structure (header → since-last-report → gap heatmap →
sequenced project plan → course resources → suggested study order → next steps),
consistent with the frontmatter schema from Task 3.

### `.claude/skills/find-courses/SKILL.md`

Normally invocable (no explicit-invocation restriction — read-only, writes nothing).
`/find-courses <skill>`: WebSearch the skill (current year for market-relevance
queries, no year filter for canonical docs), select 2-3 real resources — preference
order hands-on/project-based > official docs (tooling gaps) > structured courses >
articles. Each entry: name, URL, one-line reason, estimated duration, cost (only
"free" when the fetched resource itself confirms it). Add a tailored study-direction
line if `profile.yaml` is available (resolve it the same way `/skillpath` does — via
`git rev-parse --show-toplevel`). Print to terminal only — never writes a file. State
explicitly at the top of this SKILL.md that `/skillpath`'s Step 7 invokes this exact
procedure in-process for its own use, collecting structured output instead of
printing.

**Verify:** both files exist, are valid enough that a real Claude Code session can
load them without a parse error (check via whatever local validation is available —
at minimum confirm the frontmatter is valid YAML and required SKILL.md frontmatter
fields are present per current Claude Code conventions).

---

## Task 9: README, CONTRIBUTING, final wiring check

- `README.md`: what skillpath is, install (clone the repo — this is v1's explicitly
  repo-scoped packaging model, same convention as career-ops/ai-job-search, not a
  drop-in-anywhere skill), quickstart (`/skillpath "<current>" "<target>"`,
  `/find-courses <skill>`, `/skillpath confirm "<skill>"`), and an explicit **privacy
  note**: `profile.yaml`, `roadmaps/report-*.md`, and `tracker/skillpath_tracker.csv`
  are gitignored — don't commit your own career data if you fork this.
- `CONTRIBUTING.md`: how to add a template (schema link, run the linter), how to add
  a taxonomy entry (when: seeing the same `unmapped: true` skill across a few real
  reports; process: PR to `skill-taxonomy.yaml`), how to add a new track (mirror
  `ai-ml-engineer/`'s structure, add its aliases to `track-aliases`).
- Run the **full test suite**: `pytest tests/ -v`. Fix anything broken by later tasks
  touching earlier ones (e.g. if Task 7 added taxonomy entries Task 4's tests didn't
  anticipate — that's fine, just make sure everything is green together).
- Run the linter one more time against the full `templates/` tree to confirm nothing
  regressed.
- Sanity-check `.gitignore` end-to-end: create a throwaway `profile.yaml` and a
  throwaway `roadmaps/report-test-file.md`, confirm `git status --porcelain` stays
  clean and `git check-ignore -v` matches both, then delete the throwaway files
  (don't commit them).

**Verify:** `pytest tests/ -v` all green; linter clean; gitignore sanity check passes
and throwaway files are removed before the final commit.
