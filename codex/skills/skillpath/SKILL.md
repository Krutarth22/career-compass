---
name: skillpath
description: Use only when the user explicitly invokes `$skillpath <command> ...` -- commands are `roadmap` (generate or update a career roadmap), `college-plan` (plan college coursework), `find-courses` (find course resources), and `record-evidence` (record evidence that closes a tracked gap). Bare `$skillpath` prints command help. It researches current requirements, reconciles tracked gaps, plans projects, finds resources, and writes personal roadmap state. Never invoke it implicitly because it writes files.
---

# skillpath for Codex

Read `../../../.claude/skills/skillpath/SKILL.md` completely before acting,
then follow its workflow. Its YAML frontmatter contains Claude Code metadata;
the Markdown body contains the shared implementation and explicitly documents
Codex path resolution and `$skillpath <command> ...` argument handling,
including routing to the `college-plan` and `find-courses` commands under
`modes/`.

Use this directory as `SKILL_DIR`. Its `scripts/`, `reference/`,
`templates/`, and `modes/` entries are symlinks to the canonical
implementation, so do not look for or create a second copy.
