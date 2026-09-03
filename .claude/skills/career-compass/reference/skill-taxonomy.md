# Skill Taxonomy

The skill taxonomy is the canonical registry of skill IDs that CareerCompass uses
to talk about skills consistently across templates, live research output, and
generated roadmaps. The registry itself is data, not prose: it lives in the
sibling file [`skill-taxonomy.yaml`](./skill-taxonomy.yaml) as a plain YAML
list, so `resolution.py` (Task 4) can load it directly with
`yaml.safe_load(open(...))` — no Markdown-fence-stripping required.

## Entry schema

Each entry in `skill-taxonomy.yaml` has the shape:

```yaml
- id: string            # canonical, kebab-case, stable identifier
  display_name: string  # human-readable name shown in reports/roadmaps
  synonyms: [string]    # alternate phrasings that resolve to this id
```

`id` is the only field code should treat as a stable key — `display_name` and
`synonyms` may be edited freely, `id` should not change once other files
(templates, tracker rows, generated roadmaps) reference it.

## Two enforcement levels

The taxonomy is enforced differently depending on where a skill ID comes
from:

1. **Template `skill_tags` / `skill_prerequisites` (hard requirement).**
   Every skill tag or prerequisite ID used in a project template under
   `.claude/skills/career-compass/templates/` **must** resolve to an `id` that
   already exists in `skill-taxonomy.yaml`. Task 5's linter enforces this as
   a **hard failure** — a template referencing an unknown skill ID fails
   linting and cannot ship. This keeps templates from silently drifting out
   of sync with the registry that reports and roadmaps depend on.

2. **Live research output (soft, provisional).** When career-compass resolves
   skill mentions surfaced by live research (e.g. a course description or a
   job posting) and a mention doesn't match any known `id` or `synonym`, it
   is **not** a hard failure. Instead, resolution produces a provisional
   entry marked `unmapped: true` (e.g. `{id: "<slugified-mention>",
   display_name: "<original text>", unmapped: true}`) so the run can still
   proceed and the roadmap can still reference the skill by name. Provisional
   IDs are **never automatically written back** into `skill-taxonomy.yaml` —
   the registry only grows through a human adding an entry via a pull
   request, per the process in `CONTRIBUTING.md`.

This split exists so that the templates CareerCompass ships with are always
internally consistent (hard-checked, since they're fully under our control),
while live research — which talks to the outside world and will always
surface phrasing we haven't seen before — degrades gracefully instead of
blocking a run.

## Seeded entries

`skill-taxonomy.yaml` is seeded with one entry per `skill_tags` /
`skill_prerequisites` value used by Task 7's templates:

`retrieval-augmented-generation`, `vector-databases`, `embeddings`,
`eval-harnesses`, `prompt-engineering`, `python`, `llm-api-basics`,
`model-serving`, `api-design`, `docker`, `ml-monitoring`, `mlops-basics`,
`ml-fundamentals`

plus a reasonable additional set likely to surface in live research:

`statistics`, `sql`, `feature-engineering`, `model-training`,
`lora-finetuning`, `agent-orchestration`, `tool-use`,
`workflow-orchestration`, `data-pipelines`, `ci-cd`

## Adding a new entry

New entries are added by a human via pull request, per `CONTRIBUTING.md`.
When adding one, follow the existing conventions:

- `id` is lowercase, kebab-case, and specific enough not to collide with a
  near-neighbor (e.g. `mlops-basics` vs. `ml-monitoring` are kept distinct
  rather than merged).
- `display_name` is the phrase a person would expect to read in a roadmap or
  report.
- `synonyms` should include the phrasings resolution is actually likely to
  see in the wild (casing does not matter — matching is case-insensitive),
  including common abbreviations (e.g. `rag`, `peft`) and near-spellings
  (hyphenated vs. spaced).
