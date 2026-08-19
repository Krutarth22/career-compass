---
name: find-courses
description: Find and curate current courses or learning resources for a specific skill when the user asks for courses, tutorials, or resources, including explicit `$find-courses` invocation. Read-only; it searches and returns recommendations without writing files.
---

# find-courses for Codex

Read `../../../.claude/skills/find-courses/SKILL.md` completely before acting,
then follow its workflow. Its YAML frontmatter contains Claude Code metadata;
the Markdown body contains the shared implementation and explicitly documents
Codex invocation and path handling.

Use this directory as `SKILL_DIR`. The sibling `skillpath/` entry exposes the
canonical profile loader used for optional personalization.
