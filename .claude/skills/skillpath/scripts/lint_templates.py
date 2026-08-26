"""lint_templates.py — validates project templates under
`.claude/skills/skillpath/templates/<track>/*.md`.

Pure-function library first, CLI wrapper second. Each check function takes
already-loaded template dict(s) (as returned by template_loader.load_template
/ load_track) and returns a list of error strings (empty list = pass), so
tests/test_lint_templates.py can call them individually against in-test
fixtures without touching the real templates directory.

`lint_all` is the orchestrator: it walks every track directory under
`templates_root`, loads templates via template_loader, and runs every check,
returning the combined error list across all tracks.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from template_loader import load_track

REQUIRED_FRONTMATTER_FIELDS = (
    "title",
    "track",
    "difficulty_tier",
    "estimated_hours",
    "role",
    "skill_tags",
    "skill_prerequisites",
    "project_prerequisites",
    "prerequisite_learning_hours",
)

VALID_DIFFICULTY_TIERS = {"beginner", "intermediate", "advanced"}
VALID_ROLES = {"core", "capstone"}

REQUIRED_SECTIONS = (
    "Production Workflow Mirrored",
    "What You'll Build",
    "Student-Scope Notes",
    "Steps",
    "Extension Ideas",
    "Skills Demonstrated",
    "Industry Relevance",
)


def _label(template: dict) -> str:
    """Best-effort identifying label for a template, for error messages."""
    return template.get("_filename") or template.get("frontmatter", {}).get(
        "title"
    ) or "<unknown template>"


def check_frontmatter_valid(template: dict) -> list[str]:
    """Required fields present and correctly typed.

    Empty lists are valid for skill_tags/skill_prerequisites/
    project_prerequisites; a *missing* key is not (missing-vs-empty-list
    distinction). difficulty_tier in {beginner, intermediate, advanced};
    role in {core, capstone}; estimated_hours is an int > 0;
    prerequisite_learning_hours is an int >= 0.
    """
    errors: list[str] = []
    label = _label(template)
    fm = template.get("frontmatter") or {}

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fm:
            errors.append(f"{label}: missing required frontmatter field '{field}'")

    if errors:
        # Downstream type checks assume presence; bail out early on this
        # template to avoid confusing cascade errors on missing keys.
        return errors

    if fm["difficulty_tier"] not in VALID_DIFFICULTY_TIERS:
        errors.append(
            f"{label}: difficulty_tier '{fm['difficulty_tier']}' not in "
            f"{sorted(VALID_DIFFICULTY_TIERS)}"
        )

    if fm["role"] not in VALID_ROLES:
        errors.append(f"{label}: role '{fm['role']}' not in {sorted(VALID_ROLES)}")

    estimated_hours = fm["estimated_hours"]
    if isinstance(estimated_hours, bool) or not isinstance(estimated_hours, int):
        errors.append(f"{label}: estimated_hours must be an int, got {estimated_hours!r}")
    elif estimated_hours <= 0:
        errors.append(f"{label}: estimated_hours must be > 0, got {estimated_hours}")

    prereq_hours = fm["prerequisite_learning_hours"]
    if isinstance(prereq_hours, bool) or not isinstance(prereq_hours, int):
        errors.append(
            f"{label}: prerequisite_learning_hours must be an int, got {prereq_hours!r}"
        )
    elif prereq_hours < 0:
        errors.append(
            f"{label}: prerequisite_learning_hours must be >= 0, got {prereq_hours}"
        )

    for list_field in ("skill_tags", "skill_prerequisites", "project_prerequisites"):
        if not isinstance(fm[list_field], list):
            errors.append(f"{label}: {list_field} must be a list, got {fm[list_field]!r}")

    return errors


def check_track_matches_directory(template: dict, track_dir_name: str) -> list[str]:
    """The frontmatter `track` field must match the directory it lives in."""
    label = _label(template)
    fm = template.get("frontmatter") or {}
    track = fm.get("track")
    if track != track_dir_name:
        return [
            f"{label}: frontmatter track '{track}' does not match "
            f"directory '{track_dir_name}'"
        ]
    return []


def check_skill_ids_known(template: dict, taxonomy_ids: set[str]) -> list[str]:
    """Every skill_tags and skill_prerequisites entry must be in taxonomy_ids."""
    errors: list[str] = []
    label = _label(template)
    fm = template.get("frontmatter") or {}

    for field in ("skill_tags", "skill_prerequisites"):
        for skill_id in fm.get(field) or []:
            if skill_id not in taxonomy_ids:
                errors.append(f"{label}: unknown skill id '{skill_id}' in {field}")

    return errors


def check_sections_present(template: dict) -> list[str]:
    """Every required ## heading must be present in the template body."""
    label = _label(template)
    sections = template.get("sections") or {}
    errors = []
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            errors.append(f"{label}: missing required section '## {required}'")
    return errors


def check_project_prerequisites_valid(all_templates: list[dict]) -> list[str]:
    """Whole-track check: every project_prerequisites entry is a real sibling
    filename (no dangling references), no cycles, and no `core` template
    lists the track's `capstone` template as its own project_prerequisites
    entry (guarantees the capstone can always be placed last).
    """
    errors: list[str] = []

    filenames = {t.get("_filename") for t in all_templates if t.get("_filename")}
    by_filename = {t.get("_filename"): t for t in all_templates if t.get("_filename")}

    capstone_filenames = {
        t.get("_filename")
        for t in all_templates
        if (t.get("frontmatter") or {}).get("role") == "capstone"
    }

    # Dangling references.
    for template in all_templates:
        label = _label(template)
        fm = template.get("frontmatter") or {}
        for prereq in fm.get("project_prerequisites") or []:
            if prereq not in filenames:
                errors.append(
                    f"{label}: project_prerequisites entry '{prereq}' is not "
                    f"a template in this track"
                )

    # Core template listing the capstone as its own prerequisite.
    for template in all_templates:
        label = _label(template)
        fm = template.get("frontmatter") or {}
        if fm.get("role") != "core":
            continue
        for prereq in fm.get("project_prerequisites") or []:
            if prereq in capstone_filenames:
                errors.append(
                    f"{label}: core template must not list capstone "
                    f"'{prereq}' as a project_prerequisites entry"
                )

    # Cycle detection (only over valid, non-dangling edges to avoid
    # KeyErrors and duplicate noise on top of the dangling-ref errors above).
    graph = {
        filename: [
            prereq
            for prereq in (by_filename[filename].get("frontmatter") or {}).get(
                "project_prerequisites"
            )
            or []
            if prereq in filenames
        ]
        for filename in filenames
    }

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {filename: WHITE for filename in filenames}
    cycle_reported: set[frozenset] = set()

    def visit(node: str, stack: list[str]) -> None:
        color[node] = GRAY
        stack.append(node)
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                cycle_start = stack.index(neighbor)
                cycle_nodes = stack[cycle_start:] + [neighbor]
                key = frozenset(cycle_nodes)
                if key not in cycle_reported:
                    cycle_reported.add(key)
                    errors.append(
                        "project_prerequisites cycle detected: "
                        + " -> ".join(cycle_nodes)
                    )
            elif color[neighbor] == WHITE:
                visit(neighbor, stack)
        stack.pop()
        color[node] = BLACK

    for filename in sorted(filenames):
        if color[filename] == WHITE:
            visit(filename, [])

    return errors


def check_exactly_one_capstone(all_templates: list[dict]) -> list[str]:
    """Exactly one role: capstone per track — not zero, not two."""
    capstones = [
        t for t in all_templates if (t.get("frontmatter") or {}).get("role") == "capstone"
    ]
    if len(capstones) == 0:
        return ["track has zero templates with role: capstone (exactly one required)"]
    if len(capstones) > 1:
        names = ", ".join(sorted(t.get("_filename", "<unknown>") for t in capstones))
        return [
            f"track has {len(capstones)} templates with role: capstone "
            f"(exactly one required): {names}"
        ]
    return []


def lint_track(track_templates: list[dict], track_dir_name: str, taxonomy_ids: set[str]) -> list[str]:
    """Run every check across a single track's already-loaded templates."""
    errors: list[str] = []

    for template in track_templates:
        errors.extend(check_frontmatter_valid(template))
        errors.extend(check_track_matches_directory(template, track_dir_name))
        errors.extend(check_skill_ids_known(template, taxonomy_ids))
        errors.extend(check_sections_present(template))

    errors.extend(check_project_prerequisites_valid(track_templates))
    errors.extend(check_exactly_one_capstone(track_templates))

    return errors


def lint_all(templates_root, taxonomy_ids: set[str]) -> list[str]:
    """Orchestrate all checks across every track directory under
    `templates_root`. Returns the combined error list (empty = everything
    passes).
    """
    root = Path(templates_root)
    errors: list[str] = []

    if not root.exists():
        return [f"templates_root '{root}' does not exist"]

    for track_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        track_templates = load_track(track_dir)
        if not track_templates:
            continue
        track_errors = lint_track(track_templates, track_dir.name, taxonomy_ids)
        errors.extend(f"{track_dir.name}: {err}" for err in track_errors)

    return errors


def _load_taxonomy_ids(taxonomy_path) -> set[str]:
    import yaml

    with open(taxonomy_path, "r", encoding="utf-8") as f:
        entries = yaml.safe_load(f) or []
    return {entry["id"] for entry in entries}


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="skillpath template linter")
    parser.add_argument("templates_root", help="Path to templates/ directory")
    parser.add_argument("taxonomy_path", help="Path to skill-taxonomy.yaml")
    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        taxonomy_ids = _load_taxonomy_ids(ns.taxonomy_path)
        errors = lint_all(ns.templates_root, taxonomy_ids)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
