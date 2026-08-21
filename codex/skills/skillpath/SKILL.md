---
name: skillpath
description: Use only when the user explicitly invokes `$skillpath` to generate or update a career roadmap, research target-role gaps, confirm a skill, plan college coursework, or find course resources. It researches current requirements, reconciles tracked gaps, plans projects, finds resources, and writes personal roadmap state. Never invoke it implicitly because it writes files.
---

# skillpath for Codex

Read `../../../.claude/skills/skillpath/SKILL.md` completely before acting,
then follow its workflow. Its YAML frontmatter contains Claude Code metadata;
the Markdown body contains the shared implementation and explicitly documents
Codex path resolution and `$skillpath` argument handling, including routing
to the `college-plan` and `find-courses` modes under `modes/`.

Use this directory as `SKILL_DIR`. Its `scripts/`, `reference/`,
`templates/`, and `modes/` entries are symlinks to the canonical
implementation, so do not look for or create a second copy.
