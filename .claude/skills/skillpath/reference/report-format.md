# Report Format

This document specifies the human-readable body structure that
`SKILL.md`'s Step 9 composes and passes to `report_state.py`'s
`write_report()` as `body_markdown`. The frontmatter block that precedes
this body is a separate, machine-schema concern documented here only for
cross-reference (it is exactly the schema from Task 3's brief):

```yaml
report_id: <uuid4 string>
generated_at: <UTC ISO8601 timestamp, with colons>
current_state: string
target_state: string
resolved_track: string | null
research_confidence: high | medium | low
target_requirements: [ ... see reference/research-protocol.md ... ]
gap_assessments: [ ... see gap_state.py's reconcile_assessments() shape ... ]
```

## Body section order

The rendered body follows this fixed order:

1. **Header** -- current role, target role/level, location (if given), the
   date this roadmap was generated, and the resolved track name (or a
   plain statement that no track/templates exist yet for this target --
   see `SKILL.md` Step 5).
2. **Role Overview** -- 2-4 sentences on what the target role actually does
   day to day, a short "Core Responsibilities" list, and a short "Essential
   Skills" breakdown split into Technical and Soft, each item tied to a
   `target_requirements` entry (its category/tier) where one exists. Close
   with a brief "Career Progression" paragraph (typical next steps beyond
   this role -- e.g. entry -> mid -> senior, or common lateral/advanced
   moves) if the practitioner sources fetched in Step 3 support it, or a
   clearly-labeled general statement if not. This section is synthesized
   narrative, not a per-sentence-cited claim like `target_requirements` --
   but it must still be grounded in what Step 3 actually found (the
   practitioner articles/postings fetched), not invented from nothing. If
   Step 3's sources are too thin to responsibly write this section, say so
   plainly and keep it short rather than padding it with generic filler.
3. **Since Last Report** -- present only when a prior roadmap exists (Step
   8 in `SKILL.md`; omit this whole section entirely on a first-ever
   roadmap, don't render an empty placeholder). Summarize, in prose: gaps
   that moved from `open` to `practiced` or to `confirmed-closed` since
   the prior roadmap's `gap_assessments`, newly-surfaced gaps not present
   before, and relevant tracker events (projects/courses completed, skills
   confirmed) since the prior roadmap's `generated_at`.
4. **Gap Heatmap** -- the fresh `gap_assessments`, filtered to
   `status in {open, practiced}` (per `SKILL.md` Step 4 -- confirmed-closed
   gaps are resolved and don't need to keep cluttering the roadmap),
   grouped/sorted by `tier` (Critical first) then `status` (open before
   practiced). Render as a table or grouped list: skill, tier, status.
5. **Sequenced Project Plan** -- present only when Step 5 resolved a track
   and Step 6 ran `project_planner.py plan`. Render `plan()`'s `projects`
   list in the sequenced order it was returned (never re-sorted). This is
   the report's main body of substance and should read like a learning
   module, not a one-line summary -- for each project render, from that
   template's own `sections` (never invented, always the exact template
   content):
   - Title, difficulty tier, estimated hours, and which gap skill_ids it
     covers (`covered_gap_skill_ids`).
   - `What You'll Build` in full.
   - `Steps` in full (the numbered task list is the point -- this is what
     makes the plan actionable rather than a title on a list).
   - `Skills Demonstrated` in full.
   - `Industry Relevance` in full -- which real sectors/industries hire for
     this project's skills, so the plan reads as tied to actual jobs rather
     than an abstract exercise.
   - Any unmet `skill_prerequisites` for that project, cross-referenced to
     the Course Resources section below.
   Omit a template section here only if that specific template's
   `sections` dict doesn't contain it -- never fabricate content a
   template doesn't have. Note the `total_hours` vs. `budget_hours` and
   call out `shortfall: true` plainly if set (fewer than 2 core projects
   could be selected within budget) and any `generous_budget_exception:
   true` project. When no track resolved, state plainly that no templates
   exist yet for this target instead of rendering this section.
6. **Course Resources** -- the resource-search results from Step 7 (via
   `modes/find-courses.md`'s procedure), one block per Critical/High gap
   not covered by a selected project and per selected project's unmet
   `skill_prerequisites`: 2-3 resources each (name, URL, one-line reason,
   duration, cost).
7. **Suggested Study Order** -- a short prose sequencing recommendation
   tying sections 5 and 6 together (e.g. close prerequisite skill gaps via
   Course Resources before starting the project that depends on them,
   respecting the Sequenced Project Plan's own order for prerequisite
   chains).
8. **Next Steps** -- a short, concrete closing list: e.g. run
   `/skillpath record-evidence "<skill>" "<evidence>"` in Claude Code or
   `$skillpath record-evidence "<skill>" "<evidence>"` in Codex after finishing a
   course or project to record it, and re-run `/skillpath roadmap` again in N weeks (tie N
   to the profile's `horizon_weeks`/`weekly_time_budget_hours` if useful)
   to get a refreshed roadmap.

## Style notes

- Write the body as plain, direct Markdown a person reads end-to-end --
  headers, short paragraphs, tables/lists where they aid scanning. This is
  the one artifact in the whole skill meant for a human reader, not for
  another script to parse. `report_state.py`'s `write_report()` renders
  this Markdown into the actual deliverable, a Word (`.docx`) document, via
  `scripts/markdown_docx.py` -- stay within the subset it supports:
  `#`-`####` headers, paragraphs with inline `**bold**` / `*italic*` /
  `` `code` `` spans and `[text](url)` links (rendered as real clickable
  hyperlinks), `-`/`*` and `1.` list items, and pipe tables (`| a | b |`
  with a `|---|---|` separator row). No nested lists, code blocks, or
  images -- none of those are needed by anything this report renders
  today, and the converter silently drops constructs it doesn't
  recognize rather than erroring, so an unsupported construct degrades
  quietly instead of blocking the report.
- The body is the deliverable a person reads. The YAML frontmatter above it
  (written by `report_state.py`'s `write_report()`) is machine state for
  cross-run tracking -- gap continuity, since-last-report diffs -- not
  reading material; don't restate it verbatim in the body, and don't treat
  its presence at the top of the file as part of what makes the report
  "intuitive." A person should be able to skip straight past the
  frontmatter block and get a complete, well-organized document from the
  body alone.
- Never fabricate a source, project, or course that wasn't actually
  produced by the corresponding deterministic step or live search -- every
  claim in the body should trace back to `target_requirements`,
  `gap_assessments`, a `project_planner.py plan` result (including that
  template's own `sections` content), or a `find-courses` result. The one
  exception is the Role Overview's synthesized narrative, which is
  explicitly not per-claim-cited -- see its own entry above for how it
  must still stay grounded in what Step 3 actually found.
