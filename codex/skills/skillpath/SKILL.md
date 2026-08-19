---
name: skillpath
description: Use only when the user explicitly invokes `$skillpath` to generate or update a career roadmap, research target-role gaps, or confirm a skill. It researches current requirements, reconciles tracked gaps, plans projects, finds resources, and writes personal roadmap state. Never invoke it implicitly because it writes files.
---

# skillpath for Codex

Read `../../../.claude/skills/skillpath/SKILL.md` completely before acting,
then follow its workflow. Its YAML frontmatter contains Claude Code metadata;
the Markdown body contains the shared implementation and explicitly documents
Codex path resolution and `$skillpath` argument handling.

Use this directory as `SKILL_DIR`. Its `scripts/`, `reference/`, and
`templates/` entries are symlinks to the canonical implementation, so do not
look for or create a second copy.
