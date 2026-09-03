---
name: career-compass
description: Guide a college-to-career journey when the user explicitly invokes `$career-compass` with a command. Commands are `college-plan`, `career-suggestions`, `roadmap`, `find-courses`, and `record-evidence`; bare `$career-compass` prints help. Never invoke it implicitly because most modes write personal roadmap state.
---

# career-compass for Codex

Read `../../../.claude/skills/career-compass/SKILL.md` completely before acting,
then follow its workflow. Its YAML frontmatter contains Claude Code metadata;
the Markdown body contains the shared implementation and explicitly documents
Codex path resolution and `$career-compass <command> ...` argument handling,
including routing to all five commands under `modes/` or the inline
`record-evidence` flow.

Use this directory as `SKILL_DIR`. Its `scripts/`, `reference/`,
`templates/`, and `modes/` entries are symlinks to the canonical
implementation, so do not look for or create a second copy.
