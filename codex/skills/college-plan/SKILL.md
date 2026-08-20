---
name: college-plan
description: Use only when the user explicitly invokes `$college-plan` to get a major-based, multi-year college course sequence toward a target career. It researches target-role requirements and a generic multi-school curriculum, matches the learner's own coursework, sequences remaining courses, and writes a personal college-plan state. Never invoke it implicitly because it writes files.
---

# college-plan for Codex

Read `../../../.claude/skills/college-plan/SKILL.md` completely before
acting, then follow its workflow. Its YAML frontmatter contains Claude
Code metadata; the Markdown body contains the shared implementation and
explicitly documents Codex path resolution and `$college-plan` argument
handling.

Use this directory as `SKILL_DIR`. Its `scripts/` and `reference/` entries
are symlinks to the canonical implementation, so do not look for or
create a second copy.
