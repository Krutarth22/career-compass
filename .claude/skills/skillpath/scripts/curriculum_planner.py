"""curriculum_planner.py — deterministic matching, sequencing, and coverage
diffing for the college-plan skill.

Pure-function library first, CLI wrapper second, matching the shape of
skillpath's own scripts/ (resolution.py, project_planner.py, gap_state.py).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# resolution.py lives in the sibling skillpath skill's scripts/ directory —
# reused for its _normalize_key normalization only, to avoid duplicating
# that exact logic and risking drift. Not a package dependency: this repo
# ships both skills side by side, so the relative path is stable.
_SKILLPATH_SCRIPTS = Path(__file__).resolve().parents[2] / "skillpath" / "scripts"
if str(_SKILLPATH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SKILLPATH_SCRIPTS))

from resolution import (  # noqa: E402
    MIN_PHRASE_TOKEN_LEN,
    _is_phrase_eligible,
    _normalize_key,
    _phrase_contains,
)

UNSCHEDULED = "unscheduled"


# ---------------------------------------------------------------------------
# match_completed_courses
# ---------------------------------------------------------------------------


def match_completed_courses(learner_courses: list[dict], course_sequence: list[dict]) -> dict:
    """Match a learner's stated courses against the synthesized archetype.

    `learner_courses` is `[{"course_name": str, "status": "completed" |
    "in_progress"}]`. `course_sequence` is the raw (pre-sequencing) list of
    archetype course records, each with `course_name` and `aliases:
    [string]`.

    Returns `{"matched": [...], "ambiguous": [...], "unmatched": [...]}`.
    Every entry in every bucket carries the `status` it was given:

    - matched:   {"learner_name": str, "course_name": str, "status": str}
    - ambiguous: {"learner_name": str, "candidates": [str], "status": str}
    - unmatched: {"learner_name": str, "status": str}

    Matching is deliberately a new function, not a reuse of resolution.py's
    private `_match_by_phrase` — that helper returns a single owner or
    `None` and cannot represent "ambiguous" (2+ candidates) separately from
    "unmatched" (0 candidates), and has no notion of a course's multiple
    candidate strings (name + aliases).
    """
    # candidate_key -> set of course_name (a candidate string can only ever
    # belong to one course in a well-formed archetype, but the matching
    # logic below is written to tolerate a duplicate defensively).
    candidates: list[tuple[str, str]] = []  # (candidate_key, course_name)
    for course in course_sequence:
        course_name = course["course_name"]
        for candidate in [course_name] + list(course.get("aliases") or []):
            candidate_key = _normalize_key(str(candidate))
            if candidate_key:
                candidates.append((candidate_key, course_name))

    result: dict = {"matched": [], "ambiguous": [], "unmatched": []}

    for learner_course in learner_courses:
        learner_name = learner_course["course_name"]
        status = learner_course["status"]
        input_key = _normalize_key(learner_name)

        if not input_key:
            result["unmatched"].append({"learner_name": learner_name, "status": status})
            continue

        owners: list[str] = []

        # Exact normalized match first.
        exact_owners = [
            course_name for candidate_key, course_name in candidates if candidate_key == input_key
        ]
        if exact_owners:
            for course_name in exact_owners:
                if course_name not in owners:
                    owners.append(course_name)
        else:
            # Bounded whole-word phrase containment, either direction.
            for candidate_key, course_name in candidates:
                matched = False
                if _is_phrase_eligible(candidate_key) and _phrase_contains(candidate_key, input_key):
                    matched = True
                elif _is_phrase_eligible(input_key) and _phrase_contains(input_key, candidate_key):
                    matched = True
                if matched and course_name not in owners:
                    owners.append(course_name)

        if len(owners) == 0:
            result["unmatched"].append({"learner_name": learner_name, "status": status})
        elif len(owners) == 1:
            result["matched"].append(
                {"learner_name": learner_name, "course_name": owners[0], "status": status}
            )
        else:
            result["ambiguous"].append(
                {"learner_name": learner_name, "candidates": owners, "status": status}
            )

    return result


# ---------------------------------------------------------------------------
# sequence_courses
# ---------------------------------------------------------------------------


def sequence_courses(courses: list[dict], program_length_years: int, current_year: int) -> list[dict]:
    """Place each course into a final year, prerequisite-safe, within
    `program_length_years`, reclassifying anything behind the learner's
    `current_year`.

    Each input course dict must have `course_name`, `prerequisites`
    (list of `course_name` strings referencing other entries in this same
    list), `source_years` (list of int), and `status` ("completed" |
    "in_progress" | "upcoming"). All other keys are passed through
    unchanged.

    Returns a new list of course dicts (same order as input), each with:
    `final_year` (int | "unscheduled"), `compressed_from_source_year`
    (int | None), `behind_typical_schedule` (bool),
    `infeasible_within_program_length` (bool), `source_disagreement`
    (bool), `blocked_by_unscheduled_prerequisite` (bool).

    Raises ValueError on a prerequisite cycle — a cycle here is a data
    error from curriculum research, not a case to silently resolve.
    """
    by_name = {course["course_name"]: course for course in courses}
    _validate_prerequisites_exist(by_name)
    order = _topological_order(by_name)

    resolved: dict[str, dict] = {}

    for name in order:
        course = by_name[name]
        source_years = list(course.get("source_years") or [])
        prereq_names = list(course.get("prerequisites") or [])

        out = {
            **course,
            "compressed_from_source_year": None,
            "behind_typical_schedule": False,
            "infeasible_within_program_length": False,
            "source_disagreement": False,
            "blocked_by_unscheduled_prerequisite": False,
        }

        # Genuine source disagreement always wins, regardless of prerequisites.
        if len(set(source_years)) > 1:
            out["final_year"] = UNSCHEDULED
            out["source_disagreement"] = True
            resolved[name] = out
            continue

        # Unscheduled-prerequisite propagation: checked before prereq_floor
        # math, since max() over a set containing "unscheduled" is undefined.
        prereq_years = []
        blocked = False
        for prereq_name in prereq_names:
            prereq_final_year = resolved[prereq_name]["final_year"]
            if prereq_final_year == UNSCHEDULED:
                blocked = True
                break
            prereq_years.append(prereq_final_year)

        if blocked:
            out["final_year"] = UNSCHEDULED
            out["blocked_by_unscheduled_prerequisite"] = True
            resolved[name] = out
            continue

        prereq_floor = 1 + max(prereq_years, default=0)
        stated_year = source_years[0] if source_years else None
        natural_year = max(stated_year if stated_year is not None else 1, prereq_floor)

        if natural_year <= program_length_years:
            final_year = natural_year
            # No program-length clamp fired in this branch — nothing was
            # compressed, even if the prerequisite floor pushed the course
            # later than its source-stated year (that's a delay, already
            # visible from final_year vs. source_years, not a compression).
        elif prereq_floor <= program_length_years:
            final_year = program_length_years
            out["compressed_from_source_year"] = stated_year
        else:
            final_year = UNSCHEDULED
            out["infeasible_within_program_length"] = True

        if (
            isinstance(final_year, int)
            and final_year < current_year
            and course.get("status") not in ("completed", "in_progress")
        ):
            final_year = current_year
            out["behind_typical_schedule"] = True

        out["final_year"] = final_year
        resolved[name] = out

    return [resolved[course["course_name"]] for course in courses]


def _validate_prerequisites_exist(by_name: dict[str, dict]) -> None:
    """Raise ValueError if any course lists a prerequisite whose
    `course_name` is absent from `by_name`.

    This is plausible, not just theoretical: curriculum synthesis can
    legitimately exclude a course that fails the ≥2-school corroboration
    threshold (see curriculum-research-protocol.md) even though some other
    course still lists it as a prerequisite. Without this check, the
    dangling reference surfaces later as a bare KeyError deep inside the
    placement loop instead of a clear, actionable message.
    """
    for course in by_name.values():
        for prereq_name in course.get("prerequisites") or []:
            if prereq_name not in by_name:
                raise ValueError(
                    f"course {course['course_name']!r} lists unknown prerequisite "
                    f"{prereq_name!r} (not present in course_sequence)"
                )


def _topological_order(by_name: dict[str, dict]) -> list[str]:
    """Kahn/DFS-style topological order over `prerequisites` edges (a
    course depends on its prerequisites, so prerequisites are ordered
    first). Raises ValueError on a cycle.
    """
    order: list[str] = []
    visited: set[str] = set()
    stack: list[str] = []

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in stack:
            cycle = stack[stack.index(name):] + [name]
            raise ValueError("cycle detected in prerequisites: " + " -> ".join(cycle))
        stack.append(name)
        for prereq_name in by_name[name].get("prerequisites") or []:
            if prereq_name in by_name:
                visit(prereq_name)
        stack.pop()
        visited.add(name)
        order.append(name)

    for course_name in by_name:
        visit(course_name)

    return order


# ---------------------------------------------------------------------------
# compute_uncovered
# ---------------------------------------------------------------------------

_COVERED_STATUSES = {"completed", "in_progress", "upcoming"}
_UNCOVERED_TIERS = {"Critical", "High", "Medium"}


def compute_uncovered(
    target_requirements: list[dict],
    course_sequence: list[dict],
    self_reported_courses: list[dict],
) -> list[dict]:
    """Return `target_requirements` entries at tier Critical/High/Medium
    whose `skill_id` is not covered by any `course_sequence` or
    `self_reported_courses` entry with status in {completed, in_progress,
    upcoming} (all three count — distinguishing "already have it" from
    "will have it" is a report-body presentation detail, not a computation
    one).

    Reads `covers_skill_ids` uniformly from both source lists —
    `self_reported_courses` entries always have an empty list in v1 (no
    fetchable source to ground a title-only claim against), so they never
    contribute coverage, but need no special-casing here.
    """
    covered: set[str] = set()
    for course in list(course_sequence) + list(self_reported_courses):
        if course.get("status") in _COVERED_STATUSES:
            covered.update(course.get("covers_skill_ids") or [])

    uncovered = []
    for requirement in target_requirements:
        if requirement.get("tier") not in _UNCOVERED_TIERS:
            continue
        if requirement["skill_id"] not in covered:
            uncovered.append({"skill_id": requirement["skill_id"], "tier": requirement["tier"]})

    return uncovered


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _load_json(path) -> object:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="college-plan curriculum planning utility")
    sub = parser.add_subparsers(dest="command", required=True)

    match_p = sub.add_parser("match", help="Match learner courses to the archetype")
    match_p.add_argument("--learner-courses", required=True)
    match_p.add_argument("--sequence", required=True)

    seq_p = sub.add_parser("sequence", help="Sequence archetype courses into years")
    seq_p.add_argument("--courses", required=True)
    seq_p.add_argument("--program-length", required=True, type=int)
    seq_p.add_argument("--current-year", required=True, type=int)

    diff_p = sub.add_parser("diff", help="Compute uncovered target requirements")
    diff_p.add_argument("--requirements", required=True)
    diff_p.add_argument("--sequence", required=True)
    diff_p.add_argument("--self-reported", required=True)

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        if ns.command == "match":
            learner_courses = _load_json(ns.learner_courses)
            course_sequence = _load_json(ns.sequence)
            result = match_completed_courses(learner_courses, course_sequence)
            print(json.dumps(result))
            return 0
        if ns.command == "sequence":
            courses = _load_json(ns.courses)
            result = sequence_courses(courses, ns.program_length, ns.current_year)
            print(json.dumps(result, default=str))
            return 0
        if ns.command == "diff":
            requirements = _load_json(ns.requirements)
            course_sequence = _load_json(ns.sequence)
            self_reported = _load_json(ns.self_reported)
            result = compute_uncovered(requirements, course_sequence, self_reported)
            print(json.dumps(result))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
