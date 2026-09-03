<div align="center">

# 🧭 SkillPath

### Turn a career goal into an evidence-backed learning plan

Research current role expectations, find your skill gaps, and build a practical
roadmap of projects, courses, and college classes—directly inside Claude Code or
Codex.

[![CI](https://github.com/Krutarth22/skillpath/actions/workflows/ci.yml/badge.svg)](https://github.com/Krutarth22/skillpath/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Get started](#-quick-start) · [Explore commands](#-what-you-can-do) · [Contribute](CONTRIBUTING.md)

</div>

---

## Why SkillPath?

Career advice is often broad. SkillPath turns it into a sequence you can act on:

1. Research the skills employers currently expect for your target role.
2. Compare those expectations with your experience and evidence.
3. Prioritize the gaps that matter most.
4. Select portfolio projects in prerequisite-safe order.
5. Recommend focused courses only where projects are not enough.
6. Carry your progress into the next roadmap.

You get a dated Word report you can review, edit, and keep—not a disposable chat
answer.

## ✨ What you can do

| Goal | Command | Result |
| --- | --- | --- |
| Move toward a target role | `roadmap` | Skill gaps, sequenced projects, and learning resources |
| Plan a degree around a career | `college-plan` | A prerequisite-aware course sequence by year |
| Learn one specific skill | `find-courses` | A short list of current, relevant resources |
| Explore options for a degree | `career-suggestions` | Grounded career paths and a suggested next command |
| Record proof of progress | `record-evidence` | Evidence saved for future roadmap updates |

If you forget the commands, enter `/skillpath` in Claude Code or `$skillpath`
in Codex to see the built-in help.

## 📦 How it is packaged

| Host | Package in this repository | Invocation |
| --- | --- | --- |
| Claude Code | Installable plugin in `plugins/skillpath/` | `/skillpath …` |
| Codex | Project-local skill in `codex/skills/skillpath/` | `$skillpath …` |

Codex supports plugins, but this repository does not yet contain a
`.codex-plugin/plugin.json` package. Its current Codex distribution is the
project-local skill discovered through `.agents/skills/skillpath`. See the
[official Codex plugin guide](https://learn.chatgpt.com/docs/build-plugins) for
the distinction.

## 🚀 Quick start

### Claude Code plugin

Install SkillPath once from its marketplace:

```text
/plugin marketplace add Krutarth22/skillpath
/plugin install skillpath@skillpath
```

Then create your first roadmap from any project:

```text
/skillpath roadmap "Mechanical engineer, 8 years, strong in Python and CAD" "Senior ML Engineer"
```

The plugin installs its small Python dependencies (`pyyaml` and `python-docx`)
the first time they are needed.

### Codex skill

Clone the repository and install the Python dependencies:

<details open>
<summary><strong>macOS or Linux</strong></summary>

```bash
git clone https://github.com/Krutarth22/skillpath.git
cd skillpath
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
codex
```

</details>

<details>
<summary><strong>Windows PowerShell</strong></summary>

```powershell
git clone https://github.com/Krutarth22/skillpath.git
cd skillpath
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
codex
```

</details>

From Codex, run:

```text
$skillpath roadmap "Mechanical engineer, 8 years, strong in Python and CAD" "Senior ML Engineer"
```

Keep Codex open in the repository so it can discover the project-local skill.
If SkillPath does not appear after installation, restart Codex once.

### Requirements

- Claude Code or Codex, installed and signed in
- Git
- Python 3.11 or newer
- Internet access while researching roles, schools, and courses

Check your Python version with `python3 --version` on macOS/Linux or
`python --version` on Windows.

## 🛠️ Usage

The examples below show Claude Code first and Codex second.

### Create or refresh a career roadmap

```text
/skillpath roadmap "Data analyst with strong SQL" "Data Scientist"
$skillpath roadmap "Data analyst with strong SQL" "Data Scientist"
```

SkillPath asks about your experience, location, available study time, and other
constraints. You may also provide a PDF or DOCX resume; SkillPath extracts the
relevant details and asks you to confirm them before saving anything.

Run the command without arguments later to refresh the roadmap from your saved
profile:

```text
/skillpath roadmap
$skillpath roadmap
```

A roadmap includes:

- current target-role requirements, grouped by importance;
- gaps between those requirements and your existing evidence;
- portfolio projects in a sensible prerequisite order;
- courses for important gaps the projects do not cover; and
- changes since your previous roadmap.

### Record evidence

```text
/skillpath record-evidence "model deployment" "Deployed a prediction API to AWS and added monitoring"
$skillpath record-evidence "model deployment" "Deployed a prediction API to AWS and added monitoring"
```

Evidence can be a project, work task, course result, portfolio link, or another
concrete example. Future roadmaps use it when updating your gap status.

### Find courses for one skill

```text
/skillpath find-courses feature engineering
$skillpath find-courses feature engineering
```

SkillPath returns two or three focused resources, explains the fit, and includes
duration and cost when available.

### Explore careers for a degree

```text
/skillpath career-suggestions "BS in Mathematics" "more interested in research than industry"
$skillpath career-suggestions "BS in Mathematics" "more interested in research than industry"
```

This command prints several grounded career paths and an exact `roadmap` command
for your preferred option. It does not save a file.

### Plan college courses

```text
/skillpath college-plan "Computer Science" "Data Scientist"
$skillpath college-plan "Computer Science" "Data Scientist"
```

Add a target level as a third argument when needed:

```text
/skillpath college-plan "Computer Science" "Data Scientist" "Senior"
$skillpath college-plan "Computer Science" "Data Scientist" "Senior"
```

SkillPath asks about your education system, current year, completed classes, and
course-load constraints. The result includes:

- a course sequence organized by year;
- useful single-school electives;
- target skills a typical degree may not cover;
- extra learning resources for those gaps; and
- warnings for prerequisite or scheduling conflicts.

> [!IMPORTANT]
> College plans synthesize patterns across schools; they are not your
> university’s official catalog. Confirm course names, prerequisites, and degree
> requirements with an academic advisor.

## 🗂️ Outputs and privacy

SkillPath keeps personal working data inside your local repository:

| Path | Contents | Tracked by Git? |
| --- | --- | --- |
| `profile.yaml` | Goals, experience, skills, and preferences | No |
| `tracker/skillpath_tracker.csv` | Progress and report events | No |
| `roadmaps/report-*.docx` | Career-roadmap history | No |
| `roadmaps/college-plans/report-*.docx` | College-plan history | No |
| `*.meta.yaml` beside each report | Cross-run state used by SkillPath | No |

These paths are ignored by Git to reduce accidental commits. They may still
contain personal information, so review them before sharing or uploading the
repository.

## 🎯 Included project tracks

SkillPath currently includes deterministic project templates for:

- AI Engineer
- ML Engineer
- Data Engineer
- Data Analyst
- Data Scientist

Other target roles still receive researched gaps and course recommendations.
Project sequencing requires a matching template track.

## 🧩 How it works

```text
Profile or resume
      ↓
Current role research → skill resolution → gap reconciliation
                                           ↓
                         project selection + course research
                                           ↓
                           DOCX roadmap + progress metadata
```

The assistant handles research and conversational judgment. Small Python modules
handle deterministic state, matching, planning, sequencing, and report output.
Given the same profile, requirements, templates, evidence, and time budget, the
planner produces the same project order. Live research can change as its sources
change.

<details>
<summary><strong>Repository layout</strong></summary>

```text
.agents/skills/skillpath        # Codex discovery symlink
codex/skills/skillpath/         # Codex-compatible skill entry point
.claude-plugin/marketplace.json # Claude marketplace listing
plugins/skillpath/              # Claude plugin package
.claude/skills/skillpath/       # Canonical workflow and resources
├── SKILL.md                    # command router
├── modes/                      # command procedures
├── scripts/                    # deterministic Python modules
├── reference/                  # schemas, taxonomy, aliases, protocols
└── templates/                  # track-specific portfolio projects
tests/                          # pytest suite
tracker/                        # example and local event history
roadmaps/                       # generated reports and metadata
```

The Claude plugin and Codex entry point link back to the canonical tree under
`.claude/skills/skillpath/`, so the implementation stays in one place.

</details>

## 🧪 Development

Install development dependencies and run the checks:

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
python .claude/skills/skillpath/scripts/lint_templates.py \
  .claude/skills/skillpath/templates \
  .claude/skills/skillpath/reference/skill-taxonomy.yaml
```

CI runs the suite on Python 3.11 and 3.12. See [CONTRIBUTING.md](CONTRIBUTING.md)
for the template schema, taxonomy rules, and instructions for adding tracks.

## 📄 License

SkillPath is available under the [MIT License](LICENSE).
