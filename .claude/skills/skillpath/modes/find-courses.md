# find-courses mode

Search for and recommend 2-3 real learning resources for a single skill.
Read-only: it never writes a file, only returns/prints recommended
resources.

**Reached two ways:**

1. **Direct invocation**, routed from `SKILL.md` Step 1 when `$0` is
   literally `find-courses` (`/skillpath find-courses "<skill>"` in Claude
   Code, `$skillpath find-courses "<skill>"` in Codex) -- print the
   results to the terminal as the final response (see "Print results"
   below).
2. **In-process**, invoked directly by this same skill's `SKILL.md` Step 7
   (once per Critical/High gap not covered by a selected project and once
   per selected project's unmet `skill_prerequisites`) and by
   `modes/college-plan.md` Step 8 (once per `uncovered_skills[]` entry).
   In this case, skip "Print results" below and return the structured
   list to the caller instead.

`SKILL_DIR` and `PROJECT_ROOT` are already resolved by the caller (either
`SKILL.md`'s own "Resolving paths" section, when routed, or by whichever
mode file invoked this one in-process) -- reuse them as-is, do not
re-resolve.

## Procedure

Given a skill (this invocation's `$0` when routed directly, or passed
directly when invoked in-process):

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
   weeks for a multi-week course), and a cost. Only state a resource is
   free when the search result's own title or snippet says so; otherwise
   omit the cost field entirely rather than guessing. Never infer "free"
   from a resource's general reputation, and never claim to have opened
   the resource -- this mode searches, it does not fetch pages.
4. **Add a tailored study-direction line**, if `${PROJECT_ROOT}/profile.yaml`
   is available:
   ```bash
   python3 "${SKILL_DIR}/scripts/profile_io.py" load "${PROJECT_ROOT}/profile.yaml"
   ```
   If present, use its `current_role`, `target_role`, and existing
   `current_skills` proficiencies to write one short line connecting these
   resources to where the user already is (e.g. "since you're already
   practiced in Python, skip straight to the pandas-specific sections of
   resource 2"). If `profile.yaml` isn't present, omit this line entirely
   rather than guessing at a profile.

## Print results (direct invocation only)

When routed directly (invocation shape 1 above), print the 2-3 resources
and the optional study-direction line to the terminal as the final
response -- never write them to a file. When invoked in-process
(invocation shape 2), skip this and return the same structured data
(resource list plus optional study-direction line) to the caller instead.
