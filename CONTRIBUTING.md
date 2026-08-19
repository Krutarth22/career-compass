# Contributing to skillpath

## Adding a project template

Project templates live under
`.claude/skills/skillpath/templates/<track>/*.md` and are what
`project_planner.py` selects from when sequencing a roadmap.

1. Read the schema first:
   [`.claude/skills/skillpath/templates/TEMPLATE.md`](.claude/skills/skillpath/templates/TEMPLATE.md).
   It documents every required frontmatter field (`title`, `track`,
   `difficulty_tier`, `estimated_hours`, `role`, `skill_tags`,
   `skill_prerequisites`, `project_prerequisites`,
   `prerequisite_learning_hours`) and every required `##` body section
   (`Production Workflow Mirrored`, `What You'll Build`, `Student-Scope
   Notes`, `Steps`, `Extension Ideas`, `Skills Demonstrated`).
2. Look at two worked examples in the same directory for what a finished
   template reads like:
   `ai-engineer/rag-pipeline-with-eval.md` and
   `ml-engineer/ml-model-serving-api.md`.
3. Every `skill_tags` and `skill_prerequisites` entry must resolve to an
   `id` that already exists in
   [`skill-taxonomy.yaml`](.claude/skills/skillpath/reference/skill-taxonomy.yaml).
   If the skill you need isn't there yet, add it first (see the taxonomy
   section below) rather than inventing a tag with nowhere to resolve.
4. `project_prerequisites` entries must be exact sibling filenames within
   the same track directory — no dangling references, no cycles, and a
   `core` template must never list the track's `capstone` template as a
   prerequisite (this guarantees the capstone can always be scheduled
   last). Exactly one template per track must have `role: "capstone"`.
5. Run the linter before opening a PR:

   ```bash
   python3 .claude/skills/skillpath/scripts/lint_templates.py \
     .claude/skills/skillpath/templates \
     .claude/skills/skillpath/reference/skill-taxonomy.yaml
   ```

   `lint_templates.py` is the source of truth for what's actually
   enforced — if `TEMPLATE.md`'s prose and the linter's behavior ever
   disagree, the linter wins; open a PR to fix the doc.

## Adding a taxonomy entry

**When:** you notice the same skill mention coming back as
`unmapped: true` across a few *real* research/report runs — not a single
one-off phrasing. `resolution.py` already degrades gracefully for
one-off unmapped mentions (it produces a provisional, slugified entry so
the run isn't blocked), so a new taxonomy entry is for a skill that
clearly recurs and deserves a stable canonical id, not a reaction to
every new phrase research happens to surface.

**Process:** open a PR against
[`skill-taxonomy.yaml`](.claude/skills/skillpath/reference/skill-taxonomy.yaml)
directly — taxonomy entries are never auto-written back from live research
output, only added by a human. Follow the existing conventions (see
[`skill-taxonomy.md`](.claude/skills/skillpath/reference/skill-taxonomy.md)
for the full rationale):

- `id`: lowercase, kebab-case, and specific enough not to collide with a
  near-neighbor (e.g. `mlops-basics` and `ml-monitoring` are kept
  distinct rather than merged). Treat `id` as a stable key once other
  files start referencing it — templates, tracker rows, and generated
  reports may already carry it forward.
- `display_name`: the phrase a person would expect to read in a roadmap
  or report.
- `synonyms`: the phrasings resolution is actually likely to see in the
  wild (matching is case-insensitive, so casing doesn't matter here) —
  include common abbreviations and near-spellings (hyphenated vs. spaced).

Note the two different enforcement levels: a template referencing an
unknown skill id is a **hard lint failure** (templates are fully under our
control, so they must stay in sync with the registry). Live research
output surfacing an unmapped mention is **not** a failure — it degrades to
a provisional entry instead, precisely so a taxonomy PR is a deliberate,
reviewed addition rather than something research auto-generates.

## Adding a new track

Currently seeded: `ai-engineer`, `ml-engineer`, `data-engineer`,
`data-analyst`, `data-scientist`. To add another track, mirror their
structure:

1. Create `.claude/skills/skillpath/templates/<new-track-id>/` and add
   project templates to it following the same rules as above — a `title`,
   `track: "<new-track-id>"` matching the directory name, exactly one
   `role: "capstone"` template, and the rest `role: "core"`.
2. Add a matching entry to
   [`track-aliases.yaml`](.claude/skills/skillpath/reference/track-aliases.yaml):
   a new top-level key `<new-track-id>:` with an `aliases:` list covering
   common real-world phrasings and abbreviations, written lowercase and
   *without* seniority/level words (those are stripped before matching —
   e.g. don't add `"senior data engineer"`, just `"data engineer"`).
   See [`track-aliases.md`](.claude/skills/skillpath/reference/track-aliases.md)
   for the exact resolution rule `resolution.py` uses (normalize, then
   exact/substring match against these aliases — no fuzzy or semantic
   matching).
3. Run the linter (see above) — it walks every directory under
   `templates/`, so a new track's templates are checked automatically.
4. Run the test suite (`pytest tests/ -v`) to confirm nothing that assumed
   a single-track world broke.

## Running the checks locally

```bash
pip install -e ".[dev]"
pytest tests/ -v
python3 .claude/skills/skillpath/scripts/lint_templates.py \
  .claude/skills/skillpath/templates \
  .claude/skills/skillpath/reference/skill-taxonomy.yaml
```

Both should be clean before opening a PR.
