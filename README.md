<div align="center">

# 🧭 CareerCompass

### From college choices to career evidence—one connected journey

Choose the right college courses, explore where your degree can take you, build
a practical career roadmap, close focused skill gaps, and keep proof of every
step—directly inside Claude Code or Codex.

[![CI](https://github.com/Krutarth22/career-compass/actions/workflows/ci.yml/badge.svg)](https://github.com/Krutarth22/career-compass/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Follow the journey](#-your-careercompass-journey) · [Get started](#-quick-start) · [Contribute](CONTRIBUTING.md)

</div>

---

## 🌱 Your CareerCompass journey

CareerCompass is designed as a progression, not a collection of disconnected
tools. Start with your education, turn it into a career direction, and build
evidence that makes each new plan smarter.

```text
🎓 Plan college courses
          ↓
🧭 Explore career possibilities
          ↓
🗺️ Build your career roadmap
          ↓
📚 Find focused courses for remaining gaps
          ↓
🏆 Record evidence of what you accomplished
          └───────────────↺ strengthens your next roadmap
```

### 1. Build your academic foundation

Use `college-plan` to organize required classes, useful electives, and
prerequisites around the direction you are considering. The result is a
year-by-year course sequence you can validate with an academic advisor.

### 2. Discover where your degree can lead

Use `career-suggestions` to explore realistic paths connected to your degree,
interests, and preferences. Pick the direction that feels worth pursuing.

### 3. Turn that direction into a roadmap

Use `roadmap` to compare your current experience with real role expectations.
CareerCompass prioritizes the gaps and sequences hands-on portfolio projects so
you know what to build next—and why.

### 4. Learn exactly what the roadmap requires

Use `find-courses` when a specific gap needs focused instruction. Instead of a
huge course catalog, you get a short, relevant list with fit, duration, and cost
when available.

### 5. Convert progress into proof

Use `record-evidence` after a project, class, course, or meaningful work task.
That evidence is carried into future roadmaps, turning CareerCompass into a
living cycle rather than a one-time report.

You get a dated Word report you can review, edit, and keep—not a disposable chat
answer.

## ✨ What you can do

| Goal | Command | Result |
| --- | --- | --- |
| 1. Plan a degree around a career | `college-plan` | A prerequisite-aware course sequence by year |
| 2. Explore options for a degree | `career-suggestions` | Grounded career paths and a suggested next command |
| 3. Move toward a target role | `roadmap` | Skill gaps, sequenced projects, and learning resources |
| 4. Learn one specific skill | `find-courses` | A short list of current, relevant resources |
| 5. Record proof of progress | `record-evidence` | Evidence saved for future roadmap updates |

If you forget the commands, enter `/career-compass` in Claude Code or
`$career-compass` in Codex to see the built-in help.

## 📦 How it is packaged

| Host | Package in this repository | Invocation |
| --- | --- | --- |
| Claude Code | Installable plugin in `plugins/career-compass/` | `/career-compass …` |
| Codex | Project-local skill in `codex/skills/career-compass/` | `$career-compass …` |

Codex supports plugins, but this repository does not yet contain a
`.codex-plugin/plugin.json` package. Its current Codex distribution is the
project-local skill discovered through `.agents/skills/career-compass`. See the
[official Codex plugin guide](https://learn.chatgpt.com/docs/build-plugins) for
the distinction.

## 🚀 Quick start

### Claude Code plugin

Install CareerCompass once from its marketplace:

```text
/plugin marketplace add Krutarth22/career-compass
/plugin install CareerCompass@career-compass
```

Then begin with your college plan from any project:

```text
/career-compass college-plan "Computer Science" "Data Scientist"
```

The plugin installs its small Python dependencies (`pyyaml` and `python-docx`)
the first time they are needed.

### Codex skill

Clone the repository and install the Python dependencies:

<details open>
<summary><strong>macOS or Linux</strong></summary>

```bash
git clone https://github.com/Krutarth22/career-compass.git
cd career-compass
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
git clone https://github.com/Krutarth22/career-compass.git
cd career-compass
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
codex
```

</details>

From Codex, begin the same journey with:

```text
$career-compass college-plan "Computer Science" "Data Scientist"
```

Keep Codex open in the repository so it can discover the project-local skill.
If CareerCompass does not appear after installation, restart Codex once.

### Requirements

- Claude Code or Codex, installed and signed in
- Git
- Python 3.11 or newer
- Internet access while researching roles, schools, and courses

Check your Python version with `python3 --version` on macOS/Linux or
`python --version` on Windows.

## 🛠️ Walk through the journey

The examples below show Claude Code first and Codex second.

### 1. Plan college courses

```text
/career-compass college-plan "Computer Science" "Data Scientist"
$career-compass college-plan "Computer Science" "Data Scientist"
```

Add a target level as a third argument when needed:

```text
/career-compass college-plan "Computer Science" "Data Scientist" "Senior"
$career-compass college-plan "Computer Science" "Data Scientist" "Senior"
```

CareerCompass asks about your education system, current year, completed classes,
and course-load constraints. The result includes:

- a course sequence organized by year;
- useful single-school electives;
- target skills a typical degree may not cover;
- extra learning resources for those gaps; and
- warnings for prerequisite or scheduling conflicts.

> [!IMPORTANT]
> College plans synthesize patterns across schools; they are not your
> university’s official catalog. Confirm course names, prerequisites, and degree
> requirements with an academic advisor.

### 2. Explore careers for your degree

```text
/career-compass career-suggestions "BS in Mathematics" "more interested in research than industry"
$career-compass career-suggestions "BS in Mathematics" "more interested in research than industry"
```

This command presents several grounded career paths and an exact `roadmap`
command for the option you choose. It does not save a file.

### 3. Create or refresh your career roadmap

```text
/career-compass roadmap "Data analyst with strong SQL" "Data Scientist"
$career-compass roadmap "Data analyst with strong SQL" "Data Scientist"
```

CareerCompass asks about your experience, location, available study time, and other
constraints. You may also provide a PDF or DOCX resume; CareerCompass extracts the
relevant details and asks you to confirm them before saving anything.

A roadmap includes:

- current target-role requirements, grouped by importance;
- gaps between those requirements and your existing evidence;
- portfolio projects in a sensible prerequisite order;
- courses for important gaps the projects do not cover; and
- changes since your previous roadmap.

Run the command without arguments later to refresh it from your saved profile:

```text
/career-compass roadmap
$career-compass roadmap
```

### 4. Find courses for a specific gap

```text
/career-compass find-courses feature engineering
$career-compass find-courses feature engineering
```

CareerCompass returns two or three focused resources, explains the fit, and includes
duration and cost when available.

### 5. Record what you accomplished

```text
/career-compass record-evidence "model deployment" "Deployed a prediction API to AWS and added monitoring"
$career-compass record-evidence "model deployment" "Deployed a prediction API to AWS and added monitoring"
```

Evidence can be a project, work task, course result, portfolio link, or another
concrete example. Your next roadmap uses it to update gap status and recommend
the next best step—closing the loop back to stage three.

## 🗂️ Outputs and privacy

CareerCompass keeps personal working data inside your local repository:

| Path | Contents | Tracked by Git? |
| --- | --- | --- |
| `profile.yaml` | Goals, experience, skills, and preferences | No |
| `tracker/career_compass_tracker.csv` | Progress and report events | No |
| `roadmaps/report-*.docx` | Career-roadmap history | No |
| `roadmaps/college-plans/report-*.docx` | College-plan history | No |
| `*.meta.yaml` beside each report | Cross-run state used by CareerCompass | No |

These paths are ignored by Git to reduce accidental commits. They may still
contain personal information, so review them before sharing or uploading the
repository.

## 🎯 Included project tracks

CareerCompass currently includes deterministic project templates for:

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
.agents/skills/career-compass        # Codex discovery symlink
codex/skills/career-compass/         # Codex-compatible skill entry point
.claude-plugin/marketplace.json # Claude marketplace listing
plugins/career-compass/              # Claude plugin package
.claude/skills/career-compass/       # Canonical workflow and resources
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
`.claude/skills/career-compass/`, so the implementation stays in one place.

</details>

## 🧪 Development

Install development dependencies and run the checks:

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/ -v
python .claude/skills/career-compass/scripts/lint_templates.py \
  .claude/skills/career-compass/templates \
  .claude/skills/career-compass/reference/skill-taxonomy.yaml
```

CI runs the suite on Python 3.11 and 3.12. See [CONTRIBUTING.md](CONTRIBUTING.md)
for the template schema, taxonomy rules, and instructions for adding tracks.

## 📄 License

CareerCompass is available under the [MIT License](LICENSE).
