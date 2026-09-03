"""project_planner.py — deterministic project-selection algorithm.

Given a resolved track's templates (Task 5's template_loader.load_track
shape), this run's gap_assessments (Task 4's gap_state.reconcile_assessments
shape), the profile, and an hour budget, picks a set of "core" project
templates that best covers open/practiced skill gaps within budget, then
sequences them (topological order by project_prerequisites, capstone last).

Pure-function library first, CLI wrapper second. Every step of the greedy
selection loop is its own testable function per the task brief — do not
collapse into one function.

Determinism is a hard requirement (explicitly tested): the same inputs must
always produce byte-identical output, including tie-break order. All
iteration below is over already-deterministically-ordered inputs (the
templates directory's sorted filename order from template_loader.load_track,
or gap_assessments in caller-supplied order), and every place a choice is
made among ties, the tie-break is spelled out and stable.

Judgment calls beyond the brief's literal text (see task-6-report.md for the
full writeup):

- `select_core_projects` takes an extra `all_core_templates` param (not in
  the brief's literal signature) so a candidate's `project_prerequisites`
  can be resolved to actual template dicts even when the prerequisite
  itself doesn't cover any gap (and so isn't in the gap-driven candidate
  pool). Likewise `sequence_projects` takes `all_core_templates` and
  `profile_skill_ids` for the same reason (resolving/costing a capstone's
  own project_prerequisites that weren't already selected).
- Auto-included `project_prerequisites` (pulled in recursively when their
  dependent is picked) count toward the 4/5-project cap and toward
  `total_hours`, since they become real entries in the final sequence a
  learner has to complete. This means a single greedy pick's prerequisite
  cascade can push the selected count past 4 in one step; the cap/exception
  check only runs *between* top-level picks, not per template inside a
  cascade.
- "Marginal score of 0" (the stated stop condition) is treated as
  `<= 0` defensively, though scores are only ever built from non-negative
  gap_weight terms so they never go negative in practice.
- **Capstone prerequisites are mandatory, budget-unconstrained, and
  excluded from `shortfall`.** `sequence_projects` unconditionally pulls
  in any of the capstone's own `project_prerequisites` not already in the
  gap-driven `selected_core` set — no budget check, because once the
  capstone is in scope its prerequisites aren't optional. Two
  consequences, both deliberate:
  1. `plan()`'s `total_hours` sums the *final* sequenced list, so it
     includes these forced additions and can therefore exceed
     `budget_hours` even when `shortfall` is `false` — this is intended,
     not a bug.
  2. `shortfall` is computed from `len(selected_core)` — the gap-driven
     greedy selection's own output, *before* capstone-forced prerequisite
     additions — not from the final sequenced list's core count. This
     keeps a capstone's mandatory (budget-unconstrained) prerequisites
     from masking a genuine shortfall (e.g. 0-1 real gap-covering core
     projects selected) by inflating the apparent core count with
     additions that cover no gap and were never budget-checked.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from template_loader import load_track

TIER_WEIGHTS = {"Critical": 8, "High": 4, "Medium": 1}
FILTER_STATUSES = {"open", "practiced"}
CONFIRMED_PROFICIENCIES = {"practiced", "proficient"}
DEFAULT_CORE_CAP = 4
GENEROUS_BUDGET_FRACTION = 0.5


# ---------------------------------------------------------------------------
# Gap filtering / weighting
# ---------------------------------------------------------------------------


def filter_gap_assessments(gap_assessments: list[dict]) -> list[dict]:
    """Keep only gaps that should drive project selection: status in
    {open, practiced} and tier in {Critical, High, Medium}. Low-tier and
    confirmed-closed gaps never drive selection.
    """
    return [
        gap
        for gap in gap_assessments
        if gap.get("status") in FILTER_STATUSES and gap.get("tier") in TIER_WEIGHTS
    ]


def gap_weight(gap: dict) -> float:
    """tier_weight * status_multiplier (practiced gaps count half as much
    as open gaps of the same tier, since some exposure already exists)."""
    tier_weight = TIER_WEIGHTS[gap["tier"]]
    status_multiplier = 0.5 if gap.get("status") == "practiced" else 1.0
    return tier_weight * status_multiplier


# ---------------------------------------------------------------------------
# Candidate pool / prerequisite cost
# ---------------------------------------------------------------------------


def candidate_pool(core_templates: list[dict], filtered_gaps: list[dict]) -> list[dict]:
    """Core templates whose skill_tags intersect the filtered gaps'
    skill_ids. Filters to role == "core" defensively even if the caller
    already pre-filtered.
    """
    gap_skill_ids = {gap["skill_id"] for gap in filtered_gaps}
    result = []
    for template in core_templates:
        fm = template.get("frontmatter") or {}
        if fm.get("role") != "core":
            continue
        skill_tags = set(fm.get("skill_tags") or [])
        if skill_tags & gap_skill_ids:
            result.append(template)
    return result


def unmet_prerequisite_hours(template: dict, profile_skill_ids: set[str]) -> int:
    """template["prerequisite_learning_hours"] if any of its
    skill_prerequisites is NOT already held (at practiced/proficient) per
    profile_skill_ids, else 0. `profile_skill_ids` is precomputed by the
    caller from profile["current_skills"] (skills at practiced/proficient),
    using each entry's already-resolved canonical `skill_id`.
    """
    fm = template.get("frontmatter") or {}
    skill_prereqs = fm.get("skill_prerequisites") or []
    if any(sid not in profile_skill_ids for sid in skill_prereqs):
        return fm.get("prerequisite_learning_hours", 0)
    return 0


# ---------------------------------------------------------------------------
# Greedy marginal-coverage selection
# ---------------------------------------------------------------------------


def _gap_skill_ids_covered(template: dict, gaps_by_id: dict) -> set[str]:
    fm = template.get("frontmatter") or {}
    skill_tags = set(fm.get("skill_tags") or [])
    return skill_tags & set(gaps_by_id.keys())


def _resolve_cascade(
    template: dict,
    by_filename: dict,
    selected_filenames: set[str],
    stack: list[str],
    planned_filenames: set[str] | None = None,
) -> list[dict]:
    """Return the list of templates to add for `template` (its not-yet-
    selected project_prerequisites, resolved recursively, followed by
    `template` itself). Raises ValueError on a cycle.
    """
    if planned_filenames is None:
        planned_filenames = set(selected_filenames)

    fname = template.get("_filename")
    if not isinstance(fname, str) or not fname:
        raise ValueError("project template is missing a valid _filename")
    if fname in stack:
        cycle = stack[stack.index(fname):] + [fname]
        raise ValueError(
            "cycle detected in project_prerequisites: " + " -> ".join(cycle)
        )
    if fname in planned_filenames:
        return []
    stack = stack + [fname]

    chain: list[dict] = []
    fm = template.get("frontmatter") or {}
    for prereq_name in fm.get("project_prerequisites") or []:
        if prereq_name in planned_filenames:
            continue
        prereq_template = by_filename.get(prereq_name)
        if prereq_template is None:
            continue  # dangling reference; Task 5's linter is responsible for catching this
        chain.extend(
            _resolve_cascade(
                prereq_template,
                by_filename,
                selected_filenames,
                stack,
                planned_filenames,
            )
        )
    planned_filenames.add(fname)
    chain.append(template)
    return chain


def select_core_projects(
    candidates: list[dict],
    all_core_templates: list[dict],
    filtered_gaps: list[dict],
    profile_skill_ids: set[str],
    budget_hours: float,
) -> list[dict]:
    """Greedy marginal-coverage loop.

    Repeatedly scores every remaining candidate by the sum of gap_weight for
    gaps it covers that no already-selected candidate covers (recomputed
    after each pick), picks the highest score, tie-breaking by
    (estimated_hours + unmet_prerequisite_hours) ascending then by
    `_filename` alphabetically. Auto-selects the candidate's own
    project_prerequisites first (recursively), counting their hours too.

    Stops when 4 core projects are selected, or the running hour total
    would exceed budget_hours, or every remaining candidate has marginal
    score 0 — except once the 4-project cap is hit, exactly one more (a
    5th) is allowed if unused budget is still >= 50% of budget_hours and at
    least one remaining candidate has positive marginal score; that 5th
    project is annotated `"generous_budget_exception": True`.

    Returns the selected core-project dicts in selection order, each
    annotated with `"covered_gap_skill_ids"` (which gap skill_ids it was
    chosen to cover — empty for auto-included prerequisites) and
    `"unmet_prerequisite_hours"`.
    """
    by_filename = {t["_filename"]: t for t in all_core_templates}
    gaps_by_id = {gap["skill_id"]: gap for gap in filtered_gaps}

    selected: list[dict] = []
    selected_filenames: set[str] = set()
    covered_ids: set[str] = set()
    total_hours = 0.0

    while True:
        remaining = [c for c in candidates if c["_filename"] not in selected_filenames]
        if not remaining:
            break

        scored = []
        for c in remaining:
            marginal_ids = _gap_skill_ids_covered(c, gaps_by_id) - covered_ids
            score = sum(gap_weight(gaps_by_id[sid]) for sid in marginal_ids)
            scored.append((c, score, marginal_ids))

        if all(score <= 0 for _, score, _ in scored):
            break

        def sort_key(item):
            c, score, _ = item
            fm = c.get("frontmatter") or {}
            hours = fm.get("estimated_hours", 0)
            unmet = unmet_prerequisite_hours(c, profile_skill_ids)
            return (-score, hours + unmet, c["_filename"])

        scored.sort(key=sort_key)

        is_fifth_exception = False
        if len(selected) >= DEFAULT_CORE_CAP:
            if len(selected) == DEFAULT_CORE_CAP:
                remaining_budget = budget_hours - total_hours
                if remaining_budget >= GENEROUS_BUDGET_FRACTION * budget_hours:
                    is_fifth_exception = True
                else:
                    break
            else:
                break

        # Walk candidates in scored (score desc, then tie-break) order and
        # take the first one whose prerequisite cascade actually fits the
        # remaining budget — one unaffordable high-scoring candidate must
        # not stop the whole loop while a cheaper, lower-scoring candidate
        # would still fit.
        pick = None
        for c, score, _marginal_ids in scored:
            if score <= 0:
                continue
            cascade = _resolve_cascade(c, by_filename, selected_filenames, [])
            cascade_cost = sum(
                (t.get("frontmatter") or {}).get("estimated_hours", 0)
                + unmet_prerequisite_hours(t, profile_skill_ids)
                for t in cascade
            )
            if total_hours + cascade_cost > budget_hours:
                continue
            pick = (c, cascade, cascade_cost)
            break

        if pick is None:
            break

        best, cascade, cascade_cost = pick

        # Annotate each cascade member (auto-included prerequisites and the
        # picked candidate itself) with its OWN actual gap coverage, walked
        # in cascade order so later members see earlier members' coverage
        # already claimed — an auto-included prerequisite can itself cover
        # a gap, and that must both show up in its annotation and count
        # toward future marginal-coverage scoring.
        running_covered = set(covered_ids)
        for t in cascade:
            t_gap_ids = _gap_skill_ids_covered(t, gaps_by_id) - running_covered
            annotated = dict(t)
            annotated["unmet_prerequisite_hours"] = unmet_prerequisite_hours(t, profile_skill_ids)
            annotated["covered_gap_skill_ids"] = sorted(t_gap_ids)
            if t.get("_filename") == best.get("_filename") and is_fifth_exception:
                annotated["generous_budget_exception"] = True
            selected.append(annotated)
            selected_filenames.add(t["_filename"])
            running_covered |= t_gap_ids

        total_hours += cascade_cost
        covered_ids = running_covered

        if is_fifth_exception:
            break

    return selected


# ---------------------------------------------------------------------------
# Sequencing
# ---------------------------------------------------------------------------


def sequence_projects(
    selected_core: list[dict],
    capstone: dict | None,
    all_core_templates: list[dict],
    profile_skill_ids: set[str],
    filtered_gaps: list[dict] | None = None,
) -> list[dict]:
    """Topologically sorts selected_core (plus the capstone's own
    project_prerequisites — resolved recursively via _resolve_cascade, so a
    prerequisite's own prerequisite is pulled in too, not just one level
    deep — auto-selected into the core set if not already present) by
    project_prerequisites, then appends capstone as the final element if
    provided. The capstone is always last, never reordered by the
    topological sort. Raises ValueError on a cycle among the core set.

    `filtered_gaps` is optional (callers that don't need
    covered_gap_skill_ids on capstone-forced additions may omit it, in
    which case those additions get covered_gap_skill_ids: [] as before);
    when provided, each capstone-forced prerequisite's real skill_tags
    coverage is computed against gaps not already covered by the
    gap-driven `selected_core` set or an earlier prerequisite in the same
    forced chain.
    """
    by_filename = {t["_filename"]: t for t in all_core_templates}
    core_by_filename = {t["_filename"]: dict(t) for t in selected_core}

    gaps_by_id = {g["skill_id"]: g for g in (filtered_gaps or [])}
    running_covered: set[str] = set()
    for t in core_by_filename.values():
        running_covered |= set(t.get("covered_gap_skill_ids") or [])

    if capstone is not None:
        already_selected = set(core_by_filename.keys())
        cascade = _resolve_cascade(capstone, by_filename, already_selected, [])
        # _resolve_cascade always appends its `template` argument last;
        # that's the capstone itself, handled separately below — only the
        # prerequisite chain ahead of it belongs in the core set.
        prereq_chain = cascade[:-1]
        for prereq_template in prereq_chain:
            fname = prereq_template["_filename"]
            if fname in core_by_filename:
                continue
            annotated = dict(prereq_template)
            annotated["unmet_prerequisite_hours"] = unmet_prerequisite_hours(
                prereq_template, profile_skill_ids
            )
            if gaps_by_id:
                covered = _gap_skill_ids_covered(prereq_template, gaps_by_id) - running_covered
                annotated["covered_gap_skill_ids"] = sorted(covered)
                running_covered |= covered
            else:
                annotated["covered_gap_skill_ids"] = []
            core_by_filename[fname] = annotated

    all_nodes = list(core_by_filename.values())

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node["_filename"]: WHITE for node in all_nodes}
    order: list[dict] = []

    def visit(node: dict, stack: list[str]) -> None:
        fname = node["_filename"]
        color[fname] = GRAY
        stack.append(fname)
        fm = node.get("frontmatter") or {}
        for prereq_name in fm.get("project_prerequisites") or []:
            if prereq_name not in core_by_filename:
                continue
            state = color.get(prereq_name)
            if state == GRAY:
                cycle = stack[stack.index(prereq_name):] + [prereq_name]
                raise ValueError(
                    "cycle detected in project_prerequisites: " + " -> ".join(cycle)
                )
            if state == WHITE:
                visit(core_by_filename[prereq_name], stack)
        stack.pop()
        color[fname] = BLACK
        order.append(node)

    for node in all_nodes:
        if color[node["_filename"]] == WHITE:
            visit(node, [])

    if capstone is not None:
        capstone_annotated = dict(capstone)
        capstone_annotated["unmet_prerequisite_hours"] = unmet_prerequisite_hours(
            capstone, profile_skill_ids
        )
        if gaps_by_id:
            covered = _gap_skill_ids_covered(capstone, gaps_by_id) - running_covered
            capstone_annotated["covered_gap_skill_ids"] = sorted(covered)
        else:
            capstone_annotated.setdefault("covered_gap_skill_ids", [])
        order.append(capstone_annotated)

    return order


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------


def plan(
    track_templates: list[dict],
    gap_assessments: list[dict],
    profile: dict,
    budget_hours: float,
) -> dict:
    """Top-level orchestration: filter gaps -> build candidate pool ->
    greedily select core projects -> sequence (topo sort + capstone last).

    Returns {"projects": [...ordered final sequence...],
    "total_hours": float, "budget_hours": float, "shortfall": bool}.
    shortfall is True when fewer than 2 core projects were selected by the
    gap-driven greedy loop (select_core_projects' own output) — this is
    computed BEFORE any capstone-forced project_prerequisites are added by
    sequence_projects, so a capstone's mandatory (budget-unconstrained)
    prerequisites never mask a genuine shortfall. total_hours, by
    contrast, is summed over the final sequence and so DOES include those
    forced additions — it can exceed budget_hours even when shortfall is
    False. See the module docstring for the full rationale.
    """
    core_templates = [
        t for t in track_templates if (t.get("frontmatter") or {}).get("role") == "core"
    ]
    capstone_templates = [
        t for t in track_templates if (t.get("frontmatter") or {}).get("role") == "capstone"
    ]
    capstone = capstone_templates[0] if capstone_templates else None

    # PROFILE CONTRACT: current_skills entries are read by their `skill_id`
    # key (a canonical taxonomy id), not the free-text `skill` field the
    # user typed into profile.yaml. The caller must have resolved them via
    # resolution.resolve_profile_skills first; entries without a skill_id
    # satisfy no prerequisite.
    profile_skill_ids = {
        entry.get("skill_id")
        for entry in (profile.get("current_skills") or [])
        if entry.get("proficiency") in CONFIRMED_PROFICIENCIES
        and entry.get("skill_id")
    }

    filtered_gaps = filter_gap_assessments(gap_assessments)
    candidates = candidate_pool(core_templates, filtered_gaps)
    selected_core = select_core_projects(
        candidates, core_templates, filtered_gaps, profile_skill_ids, budget_hours
    )
    sequenced = sequence_projects(
        selected_core, capstone, core_templates, profile_skill_ids, filtered_gaps
    )

    total_hours = sum(
        (t.get("frontmatter") or {}).get("estimated_hours", 0)
        + t.get("unmet_prerequisite_hours", 0)
        for t in sequenced
    )
    # shortfall reflects whether the GAP-DRIVEN greedy selection produced
    # enough real core projects — deliberately computed from
    # `selected_core` (select_core_projects' own output), not from
    # `sequenced`. sequence_projects can force in additional core-role
    # templates that the capstone requires as project_prerequisites even
    # though they cover no gap and were never budget-checked; counting
    # those toward core_count would let a capstone's mandatory
    # prerequisites mask a genuine shortfall (0-1 real core projects
    # selected) by inflating the apparent count with budget-unconstrained
    # forced additions. See module docstring for the corresponding
    # total_hours-can-exceed-budget_hours-even-when-shortfall-is-false note.
    core_count = len(selected_core)

    return {
        "projects": sequenced,
        "total_hours": total_hours,
        "budget_hours": budget_hours,
        "shortfall": core_count < 2,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _default_templates_root() -> Path:
    return Path(__file__).parent.parent / "templates"


def _load_json(path) -> object:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="career-compass project planner")
    sub = parser.add_subparsers(dest="command", required=True)

    plan_p = sub.add_parser("plan", help="Select and sequence core projects for a track")
    plan_p.add_argument("--track", required=True, help="Track directory name")
    plan_p.add_argument(
        "--templates-root",
        default=None,
        help="Path to templates/ directory (default: career-compass/templates)",
    )
    plan_p.add_argument("--gaps", required=True, help="Path to gap_assessments JSON")
    plan_p.add_argument(
        "--profile-skills",
        required=True,
        help=(
            "Path to a JSON file containing the profile's current_skills list, "
            "already resolved to canonical ids (each entry carrying a skill_id "
            "key, as produced by resolution.py resolve-profile-skills)"
        ),
    )
    plan_p.add_argument("--budget-hours", required=True, type=float)

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        if ns.command == "plan":
            templates_root = ns.templates_root or _default_templates_root()
            track_dir = Path(templates_root) / ns.track
            track_templates = load_track(track_dir)
            gap_assessments = _load_json(ns.gaps)
            current_skills = _load_json(ns.profile_skills)
            profile = {"current_skills": current_skills}
            result = plan(track_templates, gap_assessments, profile, ns.budget_hours)
            print(json.dumps(result))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
