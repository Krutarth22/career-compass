---
name: find-courses
description: This skill should be used when the user asks to "find courses for X", "find a course on X", "resources to learn X", "/find-courses X", or wants curated learning resources for a specific skill. Read-only -- it never writes any file, only searches and prints resource recommendations.
allowed-tools: WebSearch, Read, Bash(git rev-parse:*)
---

# find-courses

Search for and recommend 2-3 real learning resources for a single skill.
This skill is read-only: it never writes a file, only prints recommended
resources to the terminal.

**Normally invocable.** Unlike `skillpath`, this skill has no
`disable-model-invocation` restriction -- Claude may invoke it on its own
judgment when a user asks for learning resources on a skill, in addition to
explicit `/find-courses <skill>` invocation.

**Used in-process by `/skillpath`.** `skillpath/SKILL.md`'s Step 7 invokes
this exact procedure in-process for its own use, once per Critical/High
gap not covered by a selected project and once per selected project's
unmet `skill_prerequisites` -- collecting the structured resource list
programmatically instead of printing it to the terminal. When following
this file from that context, skip the "Print results" step below and
return the structured list to the caller instead.

## Procedure

Given a skill (from `$0` on direct invocation, or passed in directly when
invoked in-process by `/skillpath`):

1. **Search.** Run WebSearch queries for the skill, mixing two kinds:
   - Current-year market-relevance queries (e.g. "<skill> project-based
     course <year>", "<skill> tutorial <year>") -- determine "current
     year" from the invocation's actual date, never hardcode one.
   - No-year-filter queries for canonical/official docs (e.g. "<skill>
     official documentation").
2. **Select 2-3 real resources**, in this preference order:
   1. Hands-on / project-based resources (build-along tutorials, guided
      projects) -- these transfer best.
   2. Official docs, when the gap is fundamentally a tooling gap (learning
      a specific library/platform's API surface) rather than a conceptual
      one.
   3. Structured courses (a syllabus with graded progression).
   4. Articles / blog posts, only when nothing better surfaced.
3. **Record each resource** as: name, URL, a one-line reason it's a good
   fit for this specific skill gap, an estimated duration (hours, or
   weeks for a multi-week course), and a cost. Only record cost as "free"
   when the fetched resource itself confirms it is free -- never assume
   free from a query snippet or a resource's general reputation.
4. **Add a tailored study-direction line**, if `profile.yaml` is
   available. Resolve it the same way `/skillpath` does:
   ```bash
   PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
   ```
   then check for `${PROJECT_ROOT}/profile.yaml`. If present, load it
   (`python3 "${CLAUDE_SKILL_DIR}/../skillpath/scripts/profile_io.py" load
   "${PROJECT_ROOT}/profile.yaml"` reuses `skillpath`'s own loader rather
   than re-implementing YAML parsing here) and use its `current_role`,
   `target_role`, and existing `current_skills` proficiencies to write one
   short line connecting these resources to where the user already is
   (e.g. "since you're already practiced in Python, skip straight to the
   pandas-specific sections of resource 2"). If `profile.yaml` isn't
   present, omit this line entirely rather than guessing at a profile.

## Print results (direct invocation only)

When invoked directly via `/find-courses <skill>`, print the 2-3 resources
and the optional study-direction line to the terminal as the final
response -- never write them to a file. When invoked in-process by
`/skillpath`, skip this and return the same structured data (resource
list plus optional study-direction line) to the caller instead, per the
note under "Used in-process by `/skillpath`" above.
