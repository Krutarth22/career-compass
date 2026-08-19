# skillpath

skillpath is a project-scoped skill for [Claude Code](https://claude.com/claude-code)
and [Codex](https://learn.chatgpt.com/codex). It plans a career transition by
researching current expectations for
your target role, compares them with your existing skills and evidence, builds
a sequenced portfolio-project plan, finds learning resources for uncovered
gaps, and saves a dated roadmap that evolves as you make progress.

The repository includes two skills. Claude Code uses slash invocation; Codex
uses dollar-sign invocation:

- **`/skillpath` / `$skillpath`** builds and updates the complete career
  roadmap. It only runs when explicitly invoked because it writes personal
  state to the repository.
- **`/find-courses` / `$find-courses`** searches for 2–3 current learning
  resources for one skill. It can run independently or as part of skillpath.

## Requirements

- [Claude Code](https://claude.com/claude-code) or
  [Codex](https://learn.chatgpt.com/codex), installed and authenticated
- Git
- Python 3.11 or newer
- Internet access for target-role and course research

## Installation

Clone the repository and create an isolated Python environment:

```bash
git clone https://github.com/Krutarth22/skillpath.git
cd skillpath
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Start your preferred host from the repository root while the environment is
active:

```bash
# Claude Code
claude

# Codex CLI
codex
```

Claude Code discovers the canonical workflows from `.claude/skills/`. Codex
discovers repo-scoped links from `.agents/skills/` to thin, Codex-compatible
entrypoints under `codex/skills/`. Those entrypoints load the canonical
workflow and link to the same scripts, references, and templates, so the
implementation cannot drift. Keep this repository as the working directory:
bundled resources resolve from the clone, and generated state is stored here.
Codex detects skill changes
automatically; restart it if a newly cloned skill does not appear in `/skills`.

For development, install the test dependency too:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Create your first roadmap by describing your starting point and target role.
Use the command for your host:

```text
# Claude Code
/skillpath "Mechanical engineer, 8 years, strong in Python and CAD" "Senior ML Engineer"

# Codex
$skillpath "Mechanical engineer, 8 years, strong in Python and CAD" "Senior ML Engineer"
```

On the first run, skillpath asks for any missing profile details, such as your
experience, demonstrated skills, location, constraints, and weekly time budget.
Later runs can reuse the saved profile:

```text
# Claude Code
/skillpath

# Codex
$skillpath
```

Arguments supplied on a later run are temporary overrides unless you choose to
save them to the profile.

When you have evidence that you can apply a skill, confirm it so future reports
can close the corresponding gap:

```text
# Claude Code
/skillpath confirm "model deployment"

# Codex
$skillpath confirm "model deployment"
```

To research learning resources without generating a full roadmap:

```text
# Claude Code
/find-courses feature engineering

# Codex
$find-courses feature engineering
```

Each roadmap run creates a timestamped file under `roadmaps/` with:

- sourced target-role requirements;
- a gap assessment and gap lifecycle status;
- a sequenced, time-budgeted project plan when a template track is available;
- courses for gaps not covered by projects; and
- a “Since Last Report” summary of changes from the previous run.

## Implementation

The skill deliberately separates research and conversational judgment from
state handling and planning logic:

1. **Parse and merge the profile.** The active host gathers missing details and
   `profile_io.py` applies the documented merge rules without silently
   overwriting the saved profile.
2. **Load prior state.** The latest roadmap and the append-only tracker are
   loaded so progress carries across runs.
3. **Resolve names.** `resolution.py` maps free-text skills to stable taxonomy
   IDs and maps the target role to a supported template track. Unmapped skills
   remain visible as provisional gaps instead of stopping the run.
4. **Research the target role.** The active host searches current job-market sources,
   records citations, and tiers requirements by importance using the research
   protocol in `reference/research-protocol.md`.
5. **Reconcile gaps.** `gap_state.py` compares requirements with profile
   evidence and tracker events. Gaps move through `open`, `practiced`, and
   `confirmed-closed` states.
6. **Build the project sequence.** For a resolved track,
   `project_planner.py` deterministically selects templates that cover the most
   important gaps within the time budget, expands prerequisites, and places the
   capstone last.
7. **Find remaining resources.** The find-courses workflow searches for current courses
   only for gaps the selected projects do not cover.
8. **Persist the result.** `report_state.py` writes Markdown with YAML
   frontmatter, while `tracker_io.py` appends the report event to the CSV
   history.

Given the same templates, profile, assessments, and budget, the Python planner
produces the same project order. Live role and course research can change as
the underlying sources change.

### State and data files

| Path | Purpose | Version controlled |
| --- | --- | --- |
| `profile.yaml` | Current role, target, skills, evidence, and constraints | No |
| `tracker/skillpath_tracker.csv` | Append-only progress and report events | No |
| `roadmaps/report-*.md` | Generated roadmap history | No |
| `profile.yaml.example` | Example profile schema | Yes |
| `tracker/skillpath_tracker.csv.example` | Example tracker schema | Yes |

The personal files are excluded by `.gitignore`. Do not force-add them to a
commit or publish them from a fork.

### Repository layout

```text
.agents/skills/              # Codex discovery symlinks
├── skillpath -> ../../codex/skills/skillpath
└── find-courses -> ../../codex/skills/find-courses
codex/skills/                # thin Codex-compatible entrypoints
├── skillpath/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── {scripts,reference,templates} -> canonical resources
└── find-courses/
    ├── SKILL.md
    └── agents/openai.yaml
.claude/skills/
├── skillpath/
│   ├── SKILL.md              # main orchestration instructions
│   ├── scripts/              # deterministic state and planning modules
│   ├── reference/            # schemas, taxonomy, aliases, and protocols
│   └── templates/            # track-specific project definitions
└── find-courses/
    └── SKILL.md              # focused course-research workflow
tests/                        # pytest coverage for the Python modules
profile.yaml.example          # safe sample profile
tracker/                      # sample and local event history
roadmaps/                     # local generated reports
```

The initial implementation includes project templates for the
`ai-engineer`, `ml-engineer`, `data-engineer`, `data-analyst`, and
`data-scientist` tracks. `ai-engineer` and `ml-engineer` are kept separate
on purpose — live research shows they're distinct roles (model-building vs.
model-using), not one merged "AI/ML Engineer" track. Other target roles
still receive researched gaps and course recommendations, but project
planning requires a matching track. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the template schema and instructions
for adding taxonomy entries or new tracks.

## Development and verification

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Validate all project templates and their taxonomy references:

```bash
python3 .claude/skills/skillpath/scripts/lint_templates.py \
  .claude/skills/skillpath/templates \
  .claude/skills/skillpath/reference/skill-taxonomy.yaml
```

CI runs both checks on Python 3.11 and 3.12.

## License

This project is available under the [MIT License](LICENSE).
