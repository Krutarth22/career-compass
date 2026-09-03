# Project Template Schema

This document describes the schema that every `.claude/skills/career-compass/templates/<track>/*.md`
project template must follow. It is written for human contributors adding or
editing templates — it is **not** parsed by any script. The linter
(`scripts/lint_templates.py`) is the source of truth for what is actually
enforced; keep this doc in sync with it.

Each template file (except `TEMPLATE.md` itself, which is skipped by the
loader) is a Markdown file with a YAML frontmatter block followed by a body
made of required `##` sections.

## Frontmatter fields (all required)

```yaml
---
title: "Human-readable project title"
track: "ai-ml-engineer"          # must match the directory the file lives in
difficulty_tier: "intermediate"  # one of: beginner | intermediate | advanced
estimated_hours: 15              # positive integer; 10-25 is a reasonable guideline
role: "core"                     # one of: core | capstone
skill_tags: ["python", "..."]    # every entry must resolve in skill-taxonomy.yaml
skill_prerequisites: ["python"]  # every entry must resolve in skill-taxonomy.yaml; [] is valid
project_prerequisites: []        # sibling filenames in this track's directory; [] is valid
prerequisite_learning_hours: 0   # non-negative integer; estimated hours to close skill_prerequisites gaps
---
```

Notes:
- Empty lists (`[]`) are valid for `skill_tags`, `skill_prerequisites`, and
  `project_prerequisites` — but the *key* must always be present. A missing
  key is a lint error even if the intended value is empty.
- `skill_tags` and `skill_prerequisites` values are looked up against the
  canonical ids in `reference/skill-taxonomy.yaml`. If you need a tag that
  doesn't exist yet, add it to that file (append an entry with `id`,
  `display_name`, `synonyms`, following the existing format) rather than
  inventing a tag with nowhere to resolve.
- `project_prerequisites` entries must be exact filenames of sibling
  templates in the same track directory (e.g. `"rag-pipeline-with-eval.md"`).
  References must not dangle and must not form a cycle. A `core` template
  must never list the track's `capstone` template as a `project_prerequisites`
  entry (this guarantees the capstone can always be scheduled last).
- Exactly one template per track must have `role: "capstone"`. All others
  are `role: "core"`.

## Required body sections

The body must contain each of these `##` headings, in any order the author
finds natural (the two worked examples in this directory use the order
below):

- `## Production Workflow Mirrored` — the real-world production steps this
  project condenses, as a numbered list.
- `## What You'll Build` — a short paragraph describing the end artifact.
- `## Student-Scope Notes` — where this project deliberately simplifies vs.
  a real production system (infra, scale, data volume, etc.), and why that's
  still a faithful learning proxy.
- `## Steps` — a numbered, concrete build sequence.
- `## Extension Ideas` — optional stretch goals a student can pursue after
  finishing the core build.
- `## Skills Demonstrated` — a bullet list connecting the finished project
  back to the skills a reader/interviewer would recognize.
- `## Industry Relevance` — 2-4 sentences naming the real industries or
  sectors that hire for the skills this project builds (e.g. "Healthcare
  Insurance, Fraud Detection, Public Health"), and briefly why this kind of
  work matters there. Ground this in the project's actual subject matter and
  skill_tags — don't invent a fictional company or client, and don't pad with
  generic "this is valuable everywhere" filler; name specific sectors.

See `ai-ml-engineer/rag-pipeline-with-eval.md` and
`ai-ml-engineer/ml-model-serving-api.md` for fully worked examples.
