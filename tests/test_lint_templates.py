"""Tests for template_loader.py and lint_templates.py.

Fixture templates are constructed in-test as temp files (via pytest's
tmp_path), not real templates from the repo (Task 7 hasn't written those
yet) — every happy-path and failure-mode case listed in task-5-brief.md is
covered here.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from template_loader import load_template, load_track
from lint_templates import (
    check_exactly_one_capstone,
    check_frontmatter_valid,
    check_project_prerequisites_valid,
    check_sections_present,
    check_skill_ids_known,
    check_track_matches_directory,
    lint_all,
)

TAXONOMY_IDS = {"python", "sql", "docker", "rag", "vector-databases"}

REQUIRED_SECTIONS = (
    "Production Workflow Mirrored",
    "What You'll Build",
    "Student-Scope Notes",
    "Steps",
    "Extension Ideas",
    "Skills Demonstrated",
    "Industry Relevance",
)


def default_frontmatter(**overrides) -> dict:
    fm = {
        "title": "Build a RAG Pipeline",
        "track": "ai-ml-engineer",
        "difficulty_tier": "intermediate",
        "estimated_hours": 8,
        "role": "core",
        "skill_tags": ["python", "rag"],
        "skill_prerequisites": ["sql"],
        "project_prerequisites": [],
        "prerequisite_learning_hours": 2,
    }
    fm.update(overrides)
    return fm


def default_sections_body(missing: str | None = None) -> str:
    parts = []
    for heading in REQUIRED_SECTIONS:
        if heading == missing:
            continue
        parts.append(f"## {heading}\n\nSome content for {heading}.\n")
    return "\n".join(parts)


def write_template(dir_path: Path, filename: str, frontmatter: dict, missing_section: str | None = None) -> Path:
    dir_path.mkdir(parents=True, exist_ok=True)
    path = dir_path / filename
    fm_yaml = yaml.safe_dump(frontmatter, sort_keys=False)
    body = default_sections_body(missing=missing_section)
    path.write_text(f"---\n{fm_yaml}---\n\n{body}", encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# template_loader.py
# ---------------------------------------------------------------------------


def test_load_template_parses_frontmatter_and_sections(tmp_path):
    path = write_template(tmp_path, "01-rag-pipeline.md", default_frontmatter())
    result = load_template(path)

    assert result["frontmatter"]["title"] == "Build a RAG Pipeline"
    assert result["frontmatter"]["skill_tags"] == ["python", "rag"]
    assert set(result["sections"].keys()) == set(REQUIRED_SECTIONS)
    assert "Some content for Steps." in result["sections"]["Steps"]


def test_load_track_skips_template_md_and_annotates_filename(tmp_path):
    track_dir = tmp_path / "ai-ml-engineer"
    write_template(track_dir, "01-core.md", default_frontmatter(role="core"))
    write_template(
        track_dir,
        "02-capstone.md",
        default_frontmatter(role="capstone", title="Capstone"),
    )
    write_template(track_dir, "TEMPLATE.md", default_frontmatter(title="Template"))

    templates = load_track(track_dir)

    filenames = {t["_filename"] for t in templates}
    assert filenames == {"01-core.md", "02-capstone.md"}


# ---------------------------------------------------------------------------
# check_frontmatter_valid
# ---------------------------------------------------------------------------


def test_check_frontmatter_valid_happy_path():
    template = {"frontmatter": default_frontmatter(), "_filename": "01.md"}
    assert check_frontmatter_valid(template) == []


def test_check_frontmatter_valid_missing_key_fails():
    fm = default_frontmatter()
    del fm["skill_prerequisites"]
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_frontmatter_valid(template)
    assert any("skill_prerequisites" in e for e in errors)


def test_check_frontmatter_valid_empty_lists_pass():
    fm = default_frontmatter(skill_tags=[], skill_prerequisites=[], project_prerequisites=[])
    template = {"frontmatter": fm, "_filename": "01.md"}
    assert check_frontmatter_valid(template) == []


def test_check_frontmatter_valid_bad_difficulty_tier_fails():
    fm = default_frontmatter(difficulty_tier="expert")
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_frontmatter_valid(template)
    assert any("difficulty_tier" in e for e in errors)


def test_check_frontmatter_valid_bad_role_fails():
    fm = default_frontmatter(role="student")
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_frontmatter_valid(template)
    assert any("role" in e for e in errors)


def test_check_frontmatter_valid_estimated_hours_zero_fails():
    fm = default_frontmatter(estimated_hours=0)
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_frontmatter_valid(template)
    assert any("estimated_hours" in e for e in errors)


def test_check_frontmatter_valid_estimated_hours_negative_fails():
    fm = default_frontmatter(estimated_hours=-3)
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_frontmatter_valid(template)
    assert any("estimated_hours" in e for e in errors)


def test_check_frontmatter_valid_prerequisite_learning_hours_zero_passes():
    fm = default_frontmatter(prerequisite_learning_hours=0)
    template = {"frontmatter": fm, "_filename": "01.md"}
    assert check_frontmatter_valid(template) == []


def test_check_frontmatter_valid_prerequisite_learning_hours_negative_fails():
    fm = default_frontmatter(prerequisite_learning_hours=-1)
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_frontmatter_valid(template)
    assert any("prerequisite_learning_hours" in e for e in errors)


# ---------------------------------------------------------------------------
# check_track_matches_directory
# ---------------------------------------------------------------------------


def test_check_track_matches_directory_pass():
    template = {"frontmatter": default_frontmatter(track="ai-ml-engineer"), "_filename": "01.md"}
    assert check_track_matches_directory(template, "ai-ml-engineer") == []


def test_check_track_matches_directory_fail():
    template = {"frontmatter": default_frontmatter(track="ai-ml-engineer"), "_filename": "01.md"}
    errors = check_track_matches_directory(template, "backend-engineer")
    assert len(errors) == 1
    assert "backend-engineer" in errors[0]


# ---------------------------------------------------------------------------
# check_skill_ids_known
# ---------------------------------------------------------------------------


def test_check_skill_ids_known_pass():
    template = {"frontmatter": default_frontmatter(), "_filename": "01.md"}
    assert check_skill_ids_known(template, TAXONOMY_IDS) == []


def test_check_skill_ids_known_unknown_skill_tag_fails():
    fm = default_frontmatter(skill_tags=["python", "not-a-real-skill"])
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_skill_ids_known(template, TAXONOMY_IDS)
    assert any("not-a-real-skill" in e for e in errors)


def test_check_skill_ids_known_unknown_skill_prerequisite_fails():
    fm = default_frontmatter(skill_prerequisites=["nonexistent-skill"])
    template = {"frontmatter": fm, "_filename": "01.md"}
    errors = check_skill_ids_known(template, TAXONOMY_IDS)
    assert any("nonexistent-skill" in e for e in errors)


# ---------------------------------------------------------------------------
# check_sections_present
# ---------------------------------------------------------------------------


def test_check_sections_present_happy_path(tmp_path):
    path = write_template(tmp_path, "01.md", default_frontmatter())
    template = load_template(path)
    assert check_sections_present(template) == []


def test_check_sections_present_missing_section_fails(tmp_path):
    path = write_template(tmp_path, "01.md", default_frontmatter(), missing_section="Extension Ideas")
    template = load_template(path)
    errors = check_sections_present(template)
    assert any("Extension Ideas" in e for e in errors)


# ---------------------------------------------------------------------------
# check_project_prerequisites_valid
# ---------------------------------------------------------------------------


def test_check_project_prerequisites_valid_pass():
    templates = [
        {"frontmatter": default_frontmatter(role="core", project_prerequisites=[]), "_filename": "01-core.md"},
        {
            "frontmatter": default_frontmatter(role="core", project_prerequisites=["01-core.md"]),
            "_filename": "02-core.md",
        },
        {
            "frontmatter": default_frontmatter(role="capstone", project_prerequisites=["02-core.md"]),
            "_filename": "03-capstone.md",
        },
    ]
    assert check_project_prerequisites_valid(templates) == []


def test_check_project_prerequisites_valid_dangling_reference_fails():
    templates = [
        {
            "frontmatter": default_frontmatter(role="core", project_prerequisites=["does-not-exist.md"]),
            "_filename": "01-core.md",
        },
    ]
    errors = check_project_prerequisites_valid(templates)
    assert any("does-not-exist.md" in e for e in errors)


def test_check_project_prerequisites_valid_cycle_fails():
    templates = [
        {
            "frontmatter": default_frontmatter(role="core", project_prerequisites=["02-core.md"]),
            "_filename": "01-core.md",
        },
        {
            "frontmatter": default_frontmatter(role="core", project_prerequisites=["01-core.md"]),
            "_filename": "02-core.md",
        },
    ]
    errors = check_project_prerequisites_valid(templates)
    assert any("cycle" in e.lower() for e in errors)


def test_check_project_prerequisites_valid_core_lists_capstone_fails():
    templates = [
        {
            "frontmatter": default_frontmatter(role="core", project_prerequisites=["02-capstone.md"]),
            "_filename": "01-core.md",
        },
        {
            "frontmatter": default_frontmatter(role="capstone", project_prerequisites=[]),
            "_filename": "02-capstone.md",
        },
    ]
    errors = check_project_prerequisites_valid(templates)
    assert any("capstone" in e.lower() and "01-core.md" in e for e in errors)


# ---------------------------------------------------------------------------
# check_exactly_one_capstone
# ---------------------------------------------------------------------------


def test_check_exactly_one_capstone_pass():
    templates = [
        {"frontmatter": default_frontmatter(role="core"), "_filename": "01-core.md"},
        {"frontmatter": default_frontmatter(role="capstone"), "_filename": "02-capstone.md"},
    ]
    assert check_exactly_one_capstone(templates) == []


def test_check_exactly_one_capstone_zero_fails():
    templates = [
        {"frontmatter": default_frontmatter(role="core"), "_filename": "01-core.md"},
        {"frontmatter": default_frontmatter(role="core"), "_filename": "02-core.md"},
    ]
    errors = check_exactly_one_capstone(templates)
    assert len(errors) == 1
    assert "zero" in errors[0]


def test_check_exactly_one_capstone_two_fails():
    templates = [
        {"frontmatter": default_frontmatter(role="capstone"), "_filename": "01-capstone.md"},
        {"frontmatter": default_frontmatter(role="capstone"), "_filename": "02-capstone.md"},
    ]
    errors = check_exactly_one_capstone(templates)
    assert len(errors) == 1
    assert "2" in errors[0]


# ---------------------------------------------------------------------------
# lint_all (whole-tree orchestration, real temp files on disk)
# ---------------------------------------------------------------------------


def test_lint_all_happy_path(tmp_path):
    templates_root = tmp_path / "templates"
    track_dir = templates_root / "ai-ml-engineer"

    write_template(
        track_dir,
        "01-core.md",
        default_frontmatter(role="core", project_prerequisites=[]),
    )
    write_template(
        track_dir,
        "02-capstone.md",
        default_frontmatter(
            role="capstone",
            title="Capstone Project",
            project_prerequisites=["01-core.md"],
        ),
    )

    errors = lint_all(templates_root, TAXONOMY_IDS)
    assert errors == []


def test_lint_all_aggregates_errors_across_track(tmp_path):
    templates_root = tmp_path / "templates"
    track_dir = templates_root / "ai-ml-engineer"

    # Missing section, unknown skill tag, zero capstones.
    write_template(
        track_dir,
        "01-core.md",
        default_frontmatter(role="core", skill_tags=["not-a-real-skill"]),
        missing_section="Extension Ideas",
    )

    errors = lint_all(templates_root, TAXONOMY_IDS)

    assert any("Extension Ideas" in e for e in errors)
    assert any("not-a-real-skill" in e for e in errors)
    assert any("zero" in e for e in errors)
    # Errors are prefixed with the track directory name for traceability.
    assert all(e.startswith("ai-ml-engineer:") for e in errors)


def test_lint_all_empty_templates_root_passes(tmp_path):
    templates_root = tmp_path / "templates"
    templates_root.mkdir()
    assert lint_all(templates_root, TAXONOMY_IDS) == []
