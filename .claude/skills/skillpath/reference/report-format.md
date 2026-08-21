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
2. **Since Last Report** -- present only when a prior roadmap exists (Step
   8 in `SKILL.md`; omit this whole section entirely on a first-ever
   roadmap, don't render an empty placeholder). Summarize, in prose: gaps
   that moved from `open` to `practiced` or to `confirmed-closed` since
   the prior roadmap's `gap_assessments`, newly-surfaced gaps not present
   before, and relevant tracker events (projects/courses completed, skills
   confirmed) since the prior roadmap's `generated_at`.
3. **Gap Heatmap** -- the fresh `gap_assessments`, filtered to
   `status in {open, practiced}` (per `SKILL.md` Step 4 -- confirmed-closed
   gaps are resolved and don't need to keep cluttering the roadmap),
   grouped/sorted by `tier` (Critical first) then `status` (open before
   practiced). Render as a table or grouped list: skill, tier, status.
4. **Sequenced Project Plan** -- present only when Step 5 resolved a track
   and Step 6 ran `project_planner.py plan`. Render `plan()`'s `projects`
   list in the sequenced order it was returned (never re-sorted), each
   entry's title, difficulty tier, estimated hours, and which gap
   skill_ids it covers (`covered_gap_skill_ids`). Note the `total_hours`
   vs. `budget_hours` and call out `shortfall: true` plainly if set (fewer
   than 2 core projects could be selected within budget) and any
   `generous_budget_exception: true` project. When no track resolved,
   state plainly that no templates exist yet for this target instead of
   rendering this section.
5. **Course Resources** -- the resource-search results from Step 7 (via
   `modes/find-courses.md`'s procedure), one block per Critical/High gap
   not covered by a selected project and per selected project's unmet
   `skill_prerequisites`: 2-3 resources each (name, URL, one-line reason,
   duration, cost).
6. **Suggested Study Order** -- a short prose sequencing recommendation
   tying sections 4 and 5 together (e.g. close prerequisite skill gaps via
   Course Resources before starting the project that depends on them,
   respecting the Sequenced Project Plan's own order for prerequisite
   chains).
7. **Next Steps** -- a short, concrete closing list: e.g. run
   `/skillpath record-evidence "<skill>" "<evidence>"` in Claude Code or
   `$skillpath record-evidence "<skill>" "<evidence>"` in Codex after finishing a
   course or project to record it, and re-run `/skillpath roadmap` again in N weeks (tie N
   to the profile's `horizon_weeks`/`weekly_time_budget_hours` if useful)
   to get a refreshed roadmap.

## Style notes

- Write the body as plain, direct Markdown a person reads end-to-end --
  headers, short paragraphs, tables/lists where they aid scanning. This is
  the one artifact in the whole skill meant for a human reader, not for
  another script to parse.
- Never fabricate a source, project, or course that wasn't actually
  produced by the corresponding deterministic step or live search -- every
  claim in the body should trace back to `target_requirements`,
  `gap_assessments`, a `project_planner.py plan` result, or a
  `find-courses` result.
