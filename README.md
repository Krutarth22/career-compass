# skillpath

skillpath is a [Claude Code](https://claude.com/claude-code) skill that plans
a career transition. Point it at where you are and where you want to be, and
it researches the target role's *current* live requirements, reconciles them
against a tracked history of skills you've already closed, sequences a set of
hands-on projects to close what's left, surfaces course resources for any
remaining gaps, and writes a dated roadmap report to disk — every time you
run it, not just once.

It ships as two skills that live together in this repo:

- **`skillpath`** — the main, explicit-invocation-only skill. It never fires
  from ambient conversation; only a user typing `/skillpath ...` triggers it,
  because it writes personal files to your project.
- **`find-courses`** — a small, read-only skill that finds 2-3 real learning
  resources for a single skill. It's usable on its own
  (`/find-courses <skill>`) and is also called in-process by `skillpath`
  itself when composing a roadmap.

## Installation

skillpath is **not** a drop-in-anywhere skill you copy into an unrelated
project's `.claude/skills/` folder. It's packaged and versioned as a whole
repository — the same convention as
[career-ops/ai-job-search](https://github.com/career-ops/ai-job-search) — so
that its bundled reference docs, project templates, and skill taxonomy stay
in lockstep with the scripts that read them.

To use it, clone this repository and work from inside it:

```bash
git clone <this-repo-url>
cd career_path_skills
```

Claude Code picks up `.claude/skills/skillpath/` and
`.claude/skills/find-courses/` automatically once you're working inside the
clone. `profile.yaml`, `tracker/skillpath_tracker.csv`, and your generated
roadmaps under `roadmaps/` all get created in this same working copy as you
use the skill — that's also why it needs to be a real clone, not a single
folder pasted into some other project: it needs a stable root to write its
own state relative to.

If you want dependencies installed for running the test suite or the
linter locally:

```bash
pip install -e ".[dev]"
```

(skillpath's runtime scripts only need `pyyaml`; `pytest` is dev-only.)

## Quickstart

Generate (or update) your roadmap:

```
/skillpath "<current-state>" "<target-state>"
```

For example:

```
/skillpath "Mechanical engineer, 8 years, strong in Python and CAD" "Senior ML Engineer"
```

The first time you run this in a fresh clone, skillpath doesn't yet have a
`profile.yaml` and will walk you through a short conversational setup
(current role, years of experience, current skills with proficiency and
evidence, target role/level, location, time budget, etc.). After that, running
`/skillpath` again with no arguments reuses your saved profile as-is; running
it again *with* arguments applies them as a one-off override for that run
only (you're asked afterward whether to save the override permanently).

Confirm a skill you've since demonstrated (via a project, a job, a
certification — whatever counts as real evidence), which reconciles it out of
your open-gap list on the next roadmap run:

```
/skillpath confirm "<skill>"
```

Find learning resources for one specific skill, independent of a full
roadmap run:

```
/find-courses <skill>
```

Each roadmap run writes a new dated report to `roadmaps/report-*.md`,
containing a "Since Last Report" diff against your previous run, a gap
heatmap, a sequenced project plan, and course resources for anything not
covered by a project.

## Privacy note

skillpath's whole point is to work with *your* career data, and that data is
kept out of version control on purpose. The following files are listed in
`.gitignore` and will not be committed as part of normal use:

- `profile.yaml` — your current/target role, skills, proficiencies, evidence,
  constraints, and time budget.
- `roadmaps/report-*.md` — every generated roadmap report, which includes
  your gap assessments and study plan.
- `tracker/skillpath_tracker.csv` — the append-only event history (skills
  confirmed, projects completed, reports generated) that reports are
  reconciled against.

If you fork or clone this repository to use skillpath for yourself, **don't
commit these files** — they're meant to stay local to your machine.
`profile.yaml.example` and `tracker/skillpath_tracker.csv.example` are
checked in as illustrative samples only; they are not your data and are safe
to look at, edit, or leave alone.

## Repository layout

```
.claude/skills/skillpath/       the main skill: SKILL.md, scripts/, reference/, templates/
.claude/skills/find-courses/    the course-finder skill: SKILL.md
tests/                          pytest suite for the six Python modules under scripts/
profile.yaml.example            sample profile (not your data)
tracker/skillpath_tracker.csv.example   sample tracker history (not your data)
roadmaps/                       generated reports land here (gitignored per-report)
```

## Running the tests and linter

```bash
pytest tests/ -v
python3 .claude/skills/skillpath/scripts/lint_templates.py \
  .claude/skills/skillpath/templates \
  .claude/skills/skillpath/reference/skill-taxonomy.yaml
```

See `CONTRIBUTING.md` for how to add a project template, a taxonomy entry, or
a new track.
