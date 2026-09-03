# career-suggestions mode

Answer a different, earlier question than either `roadmap` or
`college-plan` does: "I have (or am completing) a degree in `<degree>` --
what career paths does that actually open up?" Exploratory and
lightweight, like `find-courses`: it searches, prints suggestions, and
stops -- it never writes a file and never touches `profile.yaml` or the
tracker.

Reached from `SKILL.md` Step 1 when `$0` is literally `career-suggestions`
(`/career-compass career-suggestions "<degree>" ["<interests-or-context>"]` in
Claude Code, `$career-compass career-suggestions "<degree>" [...]` in Codex).
This file's own `$0`/`$1` below refer to that routed invocation's
degree/interests (i.e. the outer `$1`/`$2`) -- the caller has already
mapped them.

## Resolving paths

`SKILL_DIR` and `PROJECT_ROOT` are already resolved by `SKILL.md`'s own
"Resolving paths" section before routing here -- reuse them as-is. This
mode writes nothing to disk, so no runtime-state paths are needed.

## Step 1 — Intake

`$0` (degree) is required -- `SKILL.md`'s routing step already asks the
user for it conversationally if it was omitted, so by the time this file
runs it is always present.

Determine `degree_level` (`undergraduate` or `graduate`):

- Infer it from `$0`'s own text when unambiguous -- e.g. "MS", "MA",
  "PhD", "MBA", "MEng" imply graduate; "BS", "BA", "BEng" imply
  undergraduate.
- Only when genuinely ambiguous (e.g. a bare "Mathematics" or "Computer
  Science" with no level marker), ask once, conversationally, which it is.
  Don't ask when the text already answers it.

`$1` (interests-or-context), if given, is free-text used only to steer
which paths get emphasized and how the rationale is written (e.g. "more
interested in research than industry," "want to stay hands-on with code").
It is never required and never guessed at when absent -- if `$1` is blank,
proceed without it rather than asking a follow-up question for it.

## Step 2 — Research

Run WebSearch queries mixing two kinds, the same current-year/evergreen
split `find-courses.md` and `reference/research-protocol.md` use --
determine "current year" from the invocation's actual date, never hardcode
one:

- Current-year market-relevance queries, e.g. "career paths for `<degree>`
  graduates `<year>`", "what jobs can you get with a `<degree>` degree
  `<year>`".
- No-year-filter queries for canonical sources, e.g. a university career
  center page, professional association, or labor-statistics style source
  for `<degree>` graduates.

If `degree_level` is graduate, bias queries toward outcomes that assume
the graduate credential specifically (not just the underlying subject),
since a graduate degree often opens meaningfully different paths than the
undergraduate version of the same field.

## Step 3 — Synthesize 4-8 named career paths

For each path, write:

- **Name** of the path/role family (e.g. "Data Scientist," "Actuary,"
  "Quantitative Analyst," not a vague category like "business").
- A **1-2 sentence rationale** tying it back to the degree specifically --
  what about this degree makes it a real fit -- and to `$1`'s stated
  interests, when given.
- Optionally, one line naming the most load-bearing additional skill or
  credential this path typically needs beyond the degree itself, when the
  research surfaced one (e.g. "usually also expects SQL and a portfolio
  project"; skip this line rather than guessing when nothing concrete
  surfaced).

**Evidence bar (lighter than `research-protocol.md`'s, by design -- these
are exploratory suggestions, not validated requirements):** every path
must trace back to at least one search result actually returned in Step
2 -- never invent a path that didn't come up in the research. If Step 2's
results are thin for a given degree, say so plainly and return fewer,
better-grounded paths rather than padding the list to hit a target count
-- the same honesty rule `reference/report-format.md`'s Role Overview
section already applies to synthesized narrative.

## Step 4 — Print results and offer a handoff

Print, to the terminal as the final response (never to a file):

1. The path list from Step 3, in a sensible order (broadest/most-common
   fit first is a reasonable default, but adjust for what `$1`'s stated
   interests actually argue for).
2. One closing line offering the handoff into the main flow, naming the
   exact next command -- e.g.:

   ```text
   Want a full roadmap toward one of these? Run:
   /career-compass roadmap "recent <degree> graduate" "<chosen path>"
   ```

   (`$career-compass roadmap ...` in Codex.) Use a reasonable current-state
   guess drawn from the degree/context actually given (e.g. "recent
   `<degree>` graduate," or "`<degree>` student, expected graduation
   `<year>`" if that came up) -- never fabricate specifics (employer,
   years of experience) that weren't stated.

**Stop here.** Do not auto-invoke `roadmap` -- the user runs that command
themselves if they want it. This mode never writes `profile.yaml`, never
writes a report file, and never appends a tracker row.
