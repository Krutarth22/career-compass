# skillpath

SkillPath helps you answer practical career questions:

- What skills am I missing for the job I want?
- What projects should I build, and in what order?
- Which courses are worth taking for a particular skill?
- If I am in college, which classes will best prepare me for my target career?

It researches current role expectations, compares them with your experience,
and creates a step-by-step plan. You do not need to understand the code in
this repository to use it.

SkillPath works inside [Claude Code](https://claude.com/claude-code) and
[Codex](https://learn.chatgpt.com/codex). The examples below show both forms:
Claude Code commands begin with `/skillpath`, while Codex commands begin with
`$skillpath`.

## Choose what you want to do

| I want to… | Command |
| --- | --- |
| Plan a move from my current career to a target role | `roadmap` |
| Plan my college classes around a target career | `college-plan` |
| Find learning resources for one skill | `find-courses` |
| Add proof that I have learned or applied a skill | `record-evidence` |

If you forget the commands, enter `/skillpath` in Claude Code or `$skillpath`
in Codex. SkillPath will show a short help list.

## Requirements

Before installing SkillPath, you need:

- [Claude Code](https://claude.com/claude-code) or
  [Codex](https://learn.chatgpt.com/codex), installed and signed in;
- [Git](https://git-scm.com/downloads);
- [Python 3.11 or newer](https://www.python.org/downloads/); and
- an internet connection while SkillPath researches roles and courses.

If you are unsure whether Python is installed, open Terminal on macOS/Linux or
PowerShell on Windows and enter `python3 --version`. On Windows, try
`python --version` if the first command does not work.

## Installation

You only need to install SkillPath once.

### macOS or Linux

Open Terminal, paste the following commands, and press Enter:

```bash
git clone https://github.com/Krutarth22/skillpath.git
cd skillpath
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

### Windows

Open PowerShell, paste these commands, and press Enter:

```powershell
git clone https://github.com/Krutarth22/skillpath.git
cd skillpath
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

After installation, stay inside the `skillpath` folder and start the assistant
you use:

```bash
# Claude Code
claude

# Codex CLI
codex
```

Keep the assistant open in this folder whenever you use SkillPath. If Codex
does not show SkillPath immediately after installation, close and restart
Codex once.

### Use SkillPath again later

Each time you open a new Terminal or PowerShell window, return to the cloned
folder and reactivate its Python environment before starting Claude Code or
Codex.

On macOS or Linux:

```bash
cd skillpath
source .venv/bin/activate
claude  # or: codex
```

On Windows PowerShell:

```powershell
cd skillpath
.venv\Scripts\Activate.ps1
claude  # or: codex
```

If `cd skillpath` says that the folder cannot be found, first move to the
folder where you originally ran the installation commands.

## Quick start: create a career roadmap

Tell SkillPath where you are now and which job you want. Replace the example
text with your own details.

```text
# Claude Code
/skillpath roadmap "Mechanical engineer, 8 years, strong in Python and CAD" "Senior ML Engineer"

# Codex
$skillpath roadmap "Mechanical engineer, 8 years, strong in Python and CAD" "Senior ML Engineer"
```

SkillPath will ask a few follow-up questions about your experience, skills,
location, available study time, and any constraints. Answer naturally; you do
not need to use a special format.

It then creates a dated roadmap containing:

- the skills commonly expected for your target role;
- the gaps between those expectations and your current experience;
- portfolio projects arranged in a sensible order;
- courses for important gaps that the projects do not cover; and
- changes since your previous roadmap, if you have one.

Your roadmap is saved in the `roadmaps` folder. To refresh it later using your
saved answers, run:

```text
# Claude Code
/skillpath roadmap

# Codex
$skillpath roadmap
```

If you describe a different starting point or target role on a later run,
SkillPath treats it as temporary and asks before replacing your saved profile.

## Record your progress

When you learn or apply a skill, give SkillPath a short description of what you
did. Evidence might be a project, work task, course result, portfolio link, or
another concrete example.

```text
# Claude Code
/skillpath record-evidence "model deployment" "Deployed a prediction API to AWS and added monitoring"

# Codex
$skillpath record-evidence "model deployment" "Deployed a prediction API to AWS and added monitoring"
```

Future roadmaps will use this evidence when updating that skill gap. SkillPath
will not record an empty claim.

## Find courses for one skill

Use this when you want a few focused learning recommendations without creating
a complete career roadmap:

```text
# Claude Code
/skillpath find-courses feature engineering

# Codex
$skillpath find-courses feature engineering
```

SkillPath returns two or three current resources, explains why each one is a
good fit, and includes duration and cost when that information is available.
Multi-word skills such as `feature engineering` do not need quotation marks.

## Plan your college courses

Use `college-plan` if you are entering college or already partway through a
degree. It recommends the kinds of courses to take, and the order to take them,
based on your major and target career.

```text
# Claude Code
/skillpath college-plan "Computer Science" "Data Scientist"

# Codex
$skillpath college-plan "Computer Science" "Data Scientist"
```

SkillPath assumes you are planning for an entry-level or new-graduate role. If
you want to plan toward a different level, add it at the end:

```text
# Claude Code
/skillpath college-plan "Computer Science" "Data Scientist" "Senior"

# Codex
$skillpath college-plan "Computer Science" "Data Scientist" "Senior"
```

It will ask about your degree, country or education system, current year,
course-load limits, and courses you have already taken. These answers are
asked again on every college-plan run rather than being added to your career
profile.

The result is saved in `roadmaps/college-plans` and includes:

- the skills expected for the target career;
- a suggested course sequence organized by year;
- single-school electives worth considering;
- important skills that a typical degree may not cover, with extra learning
  resources; and
- warnings when prerequisites or time limits make part of the plan difficult
  to schedule.

This is a general plan built from several schools, not your university's
official catalog. Always confirm exact course names, prerequisites, and degree
requirements with an academic advisor.

## Your privacy and saved files

SkillPath stores its working information inside this repository on your
computer. It creates:

- `profile.yaml` for your career goals, experience, and preferences;
- `tracker/skillpath_tracker.csv` for progress you record;
- `roadmaps/report-*.md` for career roadmaps; and
- `roadmaps/college-plans/report-*.md` for college plans.

These files are excluded from Git by default, which helps prevent accidental
commits. They still contain personal information, so review them before sharing
the folder or uploading files anywhere.

## Technical details for contributors

The sections below explain SkillPath's internal design. They are not required
for normal use. To work on the code, install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

### Implementation

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
7. **Find remaining resources.** The find-courses command searches for current courses
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
| `roadmaps/report-*.md` | Generated skillpath roadmap history | No |
| `roadmaps/college-plans/report-*.md` | Generated college-plan report history | No |
| `profile.yaml.example` | Example profile schema | Yes |
| `tracker/skillpath_tracker.csv.example` | Example tracker schema | Yes |

The personal files are excluded by `.gitignore`. Do not force-add them to a
commit or publish them from a fork.

### Repository layout

```text
.agents/skills/              # Codex discovery symlink
└── skillpath -> ../../codex/skills/skillpath
codex/skills/                # thin Codex-compatible entrypoint
└── skillpath/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── {scripts,reference,templates,modes} -> canonical resources
.claude/skills/
└── skillpath/
    ├── SKILL.md              # router: parses arguments and dispatches to
    │                          # a mode file; record-evidence stays inline
    ├── scripts/               # deterministic state and planning modules,
    │                          # including curriculum_planner.py (college-plan)
    ├── reference/             # schemas, taxonomy, aliases, and protocols,
    │                          # including curriculum-research-protocol.md
    ├── templates/             # track-specific project definitions
    └── modes/
        ├── roadmap.md         # career-roadmap orchestration procedure
        ├── college-plan.md    # college course-sequencing procedure
        └── find-courses.md    # focused course-research procedure
tests/                        # pytest coverage for the Python modules
profile.yaml.example          # safe sample profile
tracker/                      # sample and local event history
roadmaps/                     # local generated skillpath reports
roadmaps/college-plans/       # local generated college-plan reports
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

### Development and verification

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
