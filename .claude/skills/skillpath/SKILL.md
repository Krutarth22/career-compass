---
name: skillpath
description: Generate or update your personal career roadmap — research target-role requirements, reconcile tracked skill gaps, plan hands-on projects, and surface course resources. Also routes to the college-plan (course sequencing for a major), find-courses (single-skill resource search), career-suggestions (career paths for a degree), and record-evidence (close a tracked gap) commands. Invoke explicitly with `/skillpath` in Claude Code or `$skillpath` in Codex; it writes profile/tracker/roadmap files, so it never runs on its own.
disable-model-invocation: true
argument-hint: "[roadmap | college-plan | find-courses | career-suggestions | record-evidence]"
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, AskUserQuestion
---

# skillpath

Research a user's target career role, reconcile it against their tracked
skill-gap history, plan a sequenced set of hands-on projects, surface course
resources for what's left, and write a personal roadmap report to disk.

This is the single, explicit-invocation-only entry point for all skillpath
functionality. In Claude Code, invoke it with `/skillpath <command> ...`;
in Codex, invoke it with `$skillpath <command> ...`. Claude's
`disable-model-invocation` frontmatter and Codex's `agents/openai.yaml`
both enforce that policy. It writes to `profile.yaml`,
`tracker/skillpath_tracker.csv`, and `roadmaps/*.docx`, all of which are
personal, gitignored data.

Five commands hang off this one router, each keyed by a mandatory first
word (`$0`) rather than a positional guess -- this removes the ambiguity
of a bare current-state string colliding with a reserved word like
`college-plan`, and lets a bare `/skillpath` print help instead of
silently assuming intent:

- `roadmap` -- builds/updates the full career roadmap (`modes/roadmap.md`).
- `college-plan` -- major-based college course sequencing
  (`modes/college-plan.md`).
- `find-courses` -- single-skill resource search
  (`modes/find-courses.md`).
- `career-suggestions` -- explore career paths for a degree/major
  (`modes/career-suggestions.md`).
- `record-evidence` -- record evidence that closes a tracked gap (Step 1,
  below).

Step 1 routes to whichever command `$0` names; see the linked mode files
for their own step-by-step procedures once routed.

**Behavior change:** `find-courses` previously existed as its own skill
with no `disable-model-invocation` restriction, so a natural-language
request ("find me resources for SQL") could trigger it directly. Now that
it's a mode under `skillpath`, it inherits this skill's
explicit-invocation-only policy -- natural-language requests no longer
auto-trigger a course search; only `/skillpath find-courses <skill>` (or
`$skillpath find-courses <skill>` in Codex) does. This was a deliberate
trade-off in favor of a single entry point, not an oversight.

## Resolving paths

Two path roots matter, and they resolve differently -- do not conflate them.

Determine both roots once per run. Every shell example below assumes these
variables are initialized in the same shell call, or that their absolute
values are substituted directly:

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SKILL_DIR="${CLAUDE_PLUGIN_ROOT:-${CLAUDE_SKILL_DIR:-${PROJECT_ROOT}/.agents/skills/skillpath}}"
```

Claude Code supplies `CLAUDE_PLUGIN_ROOT` when this skill is loaded as a
plugin, or `CLAUDE_SKILL_DIR` when loaded as a standalone `.claude/skills`
entry. Codex discovers the repo-scoped symlink at `.agents/skills/skillpath`;
the last fallback resolves through it to the same canonical resources. Stop
with a clear installation error if `SKILL_DIR` does not contain this
`SKILL.md` and the `scripts/` directory.

**Dependency bootstrap:** the scripts below import `pyyaml` and
`python-docx` (import name `docx`, used by `report_state.py` to render the
roadmap report as a Word document). A checkout run via `pip install -e .`
(see the repo's `README.md`) already has both; a plugin install does not,
since plugin installation doesn't run project setup steps. Run this once,
right after resolving `SKILL_DIR` above and before the first script call
of the run -- it's a fast no-op once both are importable:

```bash
python3 -c "import yaml, docx" 2>/dev/null || \
  python3 -m pip install --quiet --user pyyaml python-docx 2>/dev/null || \
  python3 -m pip install --quiet --user --break-system-packages pyyaml python-docx
```

`--user` installs land in the default user site-packages directory, which
Python already searches on every subsequent call -- no `PYTHONPATH` needs to
be threaded through, which matters because each script invocation below is
a separate shell call and does not inherit exported variables from prior
ones. The `--break-system-packages` fallback covers PEP 668-locked system
Pythons (e.g. Homebrew's).

**Bundled resources** (`templates/`, `reference/*`, `scripts/*.py`) are
part of this skill's own package and are addressed with the
`${SKILL_DIR}` variable. Every shell call to one of the scripts below uses
`${SKILL_DIR}/scripts/<name>.py` -- never a bare `scripts/<name>.py` relative
path, which would only work by accident of cwd.

**Runtime state** (`profile.yaml`, `tracker/skillpath_tracker.csv`,
`roadmaps/`) belongs to the user's project, not this skill's package, and
resolves relative to the **project root** determined above.

From `PROJECT_ROOT`, the runtime paths are:

- `${PROJECT_ROOT}/profile.yaml`
- `${PROJECT_ROOT}/tracker/skillpath_tracker.csv`
- `${PROJECT_ROOT}/roadmaps/`
- `${PROJECT_ROOT}/roadmaps/.tmp/` -- scratch directory (already gitignored)
  for the intermediate JSON files that the CLI-less functions below need as
  file input; create it with `mkdir -p` before first use in a run.

This root file only parses arguments and routes (Step 1, below). Each
command's own scripts, reference docs, and step-by-step procedure are
documented in its mode file (`modes/roadmap.md`, `modes/college-plan.md`,
`modes/find-courses.md`, `modes/career-suggestions.md`) or, for
`record-evidence`, inline in Step 1 itself, since that command is short
enough not to need its own file.

## Step 1 -- Parse arguments and route

Six logical invocation shapes, all keyed off a mandatory first word,
`$0`, naming the command:

- **Bare invocation (help):** `/skillpath` / `$skillpath` with no
  arguments at all.
- **`roadmap`:** `/skillpath roadmap "<current-state>" "<target-state>"`
  in Claude Code, or `$skillpath roadmap "<current-state>" "<target-state>"`
  in Codex -- builds/updates the full career roadmap (`modes/roadmap.md`).
  Both state arguments are optional (see below).
- **`college-plan`:** `/skillpath college-plan "<major>" "<target_role>"
  ["<target_level>"]`.
- **`find-courses`:** `/skillpath find-courses <skill>`.
- **`career-suggestions`:** `/skillpath career-suggestions "<degree>"
  ["<interests-or-context>"]` -- explores career paths for a degree/major.
- **`record-evidence`:** `/skillpath record-evidence "<skill>" "<evidence>"`
  -- records evidence that closes a tracked gap.

Claude Code exposes positional arguments as `$0`, `$1`, `$2`, `$3`. Codex
does not; parse the text following the `$skillpath` mention into the
equivalent logical values. Below, `$0`/`$1`/`$2`/`$3` mean those parsed
values when running under Codex, not literal shell parameters.

Requiring `roadmap` as an explicit first word (rather than treating a bare
`<current-state>` as the default flow) is deliberate: it removes the
ambiguity of a current-state string that happens to collide with a
reserved command word like `college-plan` or `find-courses`, and it lets
bare `/skillpath` show help instead of silently guessing what the user
wants.

**If `$0` is empty** (bare invocation), print a short command list and
stop -- do not guess a command or fall into any flow below:

```text
skillpath -- career roadmap and course-planning commands

  /skillpath roadmap ["<current-state>" "<target-state>"]
      Build or update your full career roadmap. Reuses your saved
      profile.yaml when no arguments are given. You can share a resume
      (PDF, DOCX, or pasted text) at any point to pre-fill or refresh
      your current role/experience/skills instead of answering one by
      one.

  /skillpath college-plan "<major>" "<target-role>" ["<target-level>"]
      Sequence college coursework for a major toward a target career.

  /skillpath find-courses <skill>
      Search for 2-3 current learning resources for one skill.

  /skillpath career-suggestions "<degree>" ["<interests-or-context>"]
      Explore career paths that a degree/major opens up, with a
      grounded rationale for each. Read-only -- prints suggestions and
      a suggested next command, saves nothing.

  /skillpath record-evidence "<skill>" "<evidence>"
      Record evidence that closes a tracked skill gap.
```

(Substitute `$skillpath` for `/skillpath` when printing this under Codex.)

If `$0` is literally `college-plan`, read and follow
`${SKILL_DIR}/modes/college-plan.md` in full for the rest of this run, with
that file's own `$0`/`$1`/`$2` mapped to this invocation's `$1` (major),
`$2` (target_role), `$3` (target_level) respectively. Stop following this
file once routed -- the mode file is self-contained end to end, including
its own report-saving step.

If `$0` is literally `find-courses`, read and follow
`${SKILL_DIR}/modes/find-courses.md` in full for the rest of this run,
with that file's own `$0` (skill) mapped to **all of this invocation's
remaining words joined back together with single spaces** -- `$1` plus any
further `$2`, `$3`, etc. A skill name is very often more than one word
(e.g. "feature engineering", "SQL window functions"); mapping only `$1`
silently truncates it, so never do that. Use its direct-invocation "Print
results" behavior (this is not the in-process case). Stop following this
file once routed.

If `$0` is literally `career-suggestions`:

- **`$1` (degree) is required.** If it's absent or blank, ask the user
  once conversationally for the degree/major before routing -- never
  guess one. Once obtained, proceed with routing.
- Read and follow `${SKILL_DIR}/modes/career-suggestions.md` in full for
  the rest of this run, with that file's own `$0`/`$1` mapped to this
  invocation's `$1` (degree) and `$2` (interests-or-context, optional).
  Stop following this file once routed -- the mode file is self-contained
  end to end (it prints results and stops; it never writes a file).

If `$0` is literally `record-evidence`:

1. Resolve the skill mention to a canonical id:
   ```bash
   python3 "${SKILL_DIR}/scripts/resolution.py" resolve-skill "$1"
   ```
   This prints `{"id": "...", "unmapped": true|false}`.
2. **Evidence is required -- `record-evidence` never closes a gap on an
   empty claim.** If `$2` (evidence) is absent or blank, ask the user once
   conversationally for evidence backing the claim. If their answer is
   still empty or is a non-answer ("none", "not sure", "just trust me"),
   **do not append a tracker row** -- tell them evidence is required to
   record progress on this skill, and stop. Do not loop asking a second
   time; a declined request simply doesn't get recorded.
3. Load the current profile (see `modes/roadmap.md` Step 2's
   `profile_io.py load` call) to read its `target_role`/`target_level`
   for the `confirmed_for_*` fields.
4. Append a tracker row:
   ```bash
   python3 "${SKILL_DIR}/scripts/tracker_io.py" append \
     "${PROJECT_ROOT}/tracker/skillpath_tracker.csv" \
     --occurred-at "<current UTC ISO8601 timestamp>" \
     --event-type skill_confirmed \
     --item-name "<resolved skill id or display name>" \
     --related-skill-ids "<resolved skill id>" \
     --report-id "<report_id of the most recent report, or empty string if none>" \
     --notes "<the evidence text>" \
     --confirmed-for-target-role "<profile.target_role>" \
     --confirmed-for-target-level "<profile.target_level, or empty>"
   ```
   (The `skill_confirmed` event type and `--confirmed-for-*` flag names
   are the tracker's existing schema and stay as-is -- only the slash
   command that reaches this step is named `record-evidence` now.)
5. Report success to the user and **stop** -- do not continue into
   research/report generation for a `record-evidence` invocation.

If `$0` is literally `roadmap`, read and follow `${SKILL_DIR}/modes/roadmap.md`
in full for the rest of this run, with that file's own `$0`/`$1` mapped to
this invocation's `$1` (current-state) and `$2` (target-state)
respectively. Stop following this file once routed -- the mode file is
self-contained end to end, including its own report-saving step.

If `$0` is anything else (an unrecognized word), print the same help text
as the bare-invocation case above, noting that `$0` wasn't a recognized
command, and stop.
