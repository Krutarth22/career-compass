"""Integration checks for the college-plan skill: report round-trip,
directory isolation from CareerCompass's own roadmaps/, resolve-profile-skills
reuse, Codex packaging symlink integrity, and privacy (.gitignore).
"""

import subprocess
from pathlib import Path

import report_state

REPO_ROOT = Path(__file__).resolve().parents[1]


def _sample_college_plan_frontmatter():
    return {
        "report_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        "generated_at": "2026-08-19T10:00:00+00:00",
        "major": "Computer Science",
        "target_state": "Data Scientist",
        "target_level": "entry-level / new graduate",
        "target_level_was_defaulted": True,
        "research_confidence": "high",
        "learner_context": {
            "degree_type": "BS",
            "education_system": "United States",
            "current_year_number": 1,
            "current_year_or_semester": "Fall, freshman year",
            "expected_program_length_years": 4,
            "course_load_constraints": None,
            "completed_courses": [],
            "in_progress_courses": [],
        },
        "target_requirements": [
            {
                "skill_id": "python",
                "unmapped": False,
                "category": "hard",
                "tier": "Critical",
                "confidence": "high",
                "frequency_signal": 0.9,
                "sources": [],
            }
        ],
        "course_sequence": [
            {
                "year": 1,
                "courses": [
                    {
                        "course_name": "Intro to Programming",
                        "aliases": ["CS 1110"],
                        "status": "upcoming",
                        "prerequisites": [],
                        "source_years": [1],
                        "covers_skill_ids": ["python"],
                        "coverage_evidence": [],
                        "confidence": "high",
                        "compressed_from_source_year": None,
                        "behind_typical_schedule": False,
                        "infeasible_within_program_length": False,
                        "source_disagreement": False,
                        "blocked_by_unscheduled_prerequisite": False,
                        "sources": [],
                    }
                ],
            }
        ],
        "electives": [],
        "self_reported_courses": [],
        "uncovered_skills": [],
        "supplemental_resources": [],
    }


# report_state.py performs no schema validation of its own (it round-trips
# whatever dict it's given), so a fixture that silently drops a required
# field would still pass a bare equality round-trip check. These key sets
# mirror the design spec's Report Schema exactly, so this test fails loudly
# if the fixture (or the schema itself) drifts.
REQUIRED_TOP_LEVEL_KEYS = {
    "report_id",
    "generated_at",
    "major",
    "target_state",
    "target_level",
    "target_level_was_defaulted",
    "research_confidence",
    "learner_context",
    "target_requirements",
    "course_sequence",
    "electives",
    "self_reported_courses",
    "uncovered_skills",
    "supplemental_resources",
}

REQUIRED_COURSE_KEYS = {
    "course_name",
    "aliases",
    "status",
    "prerequisites",
    "source_years",
    "covers_skill_ids",
    "coverage_evidence",
    "confidence",
    "compressed_from_source_year",
    "behind_typical_schedule",
    "infeasible_within_program_length",
    "source_disagreement",
    "blocked_by_unscheduled_prerequisite",
    "sources",
}


def test_report_round_trips_exactly(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps" / "college-plans"
    frontmatter = _sample_college_plan_frontmatter()

    assert set(frontmatter.keys()) == REQUIRED_TOP_LEVEL_KEYS
    sample_course = frontmatter["course_sequence"][0]["courses"][0]
    assert set(sample_course.keys()) == REQUIRED_COURSE_KEYS

    path = report_state.write_report(str(roadmaps_dir), frontmatter, "# Body\n")
    read_back = report_state.read_report(path)

    assert read_back == frontmatter


def test_directory_isolation_between_career_compass_and_college_plan(tmp_path):
    roadmaps_root = tmp_path / "roadmaps"

    career_compass_frontmatter = {
        "report_id": "11111111-1111-1111-1111-111111111111",
        "generated_at": "2026-08-19T09:00:00+00:00",
        "target_state": "ML Engineer",
    }
    college_plan_frontmatter = {
        "report_id": "22222222-2222-2222-2222-222222222222",
        "generated_at": "2026-08-19T09:30:00+00:00",
        "target_state": "Data Scientist",
    }

    report_state.write_report(str(roadmaps_root), career_compass_frontmatter, "# career-compass\n")
    report_state.write_report(
        str(roadmaps_root / "college-plans"), college_plan_frontmatter, "# college-plan\n"
    )

    last = report_state.get_last_report(str(roadmaps_root))
    assert last["report_id"] == career_compass_frontmatter["report_id"]


def test_resolve_profile_skills_cli_matches_documented_invocation():
    result = subprocess.run(
        [
            "python3",
            str(REPO_ROOT / ".claude" / "skills" / "career-compass" / "scripts" / "resolution.py"),
            "resolve-profile-skills",
            "--help",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--current-skills" in result.stdout
    assert "--taxonomy" in result.stdout


def test_codex_packaging_symlinks_resolve_to_canonical_files():
    canonical_reference = REPO_ROOT / ".claude" / "skills" / "career-compass" / "reference"
    canonical_scripts = REPO_ROOT / ".claude" / "skills" / "career-compass" / "scripts"
    canonical_modes = REPO_ROOT / ".claude" / "skills" / "career-compass" / "modes"

    codex_reference = REPO_ROOT / "codex" / "skills" / "career-compass" / "reference"
    codex_scripts = REPO_ROOT / "codex" / "skills" / "career-compass" / "scripts"
    codex_modes = REPO_ROOT / "codex" / "skills" / "career-compass" / "modes"

    assert codex_reference.resolve() == canonical_reference.resolve()
    assert codex_scripts.resolve() == canonical_scripts.resolve()
    assert codex_modes.resolve() == canonical_modes.resolve()

    assert (canonical_modes / "roadmap.md").is_file()
    assert (canonical_modes / "college-plan.md").is_file()
    assert (canonical_modes / "find-courses.md").is_file()

    agents_symlink = REPO_ROOT / ".agents" / "skills" / "career-compass"
    codex_skill_dir = REPO_ROOT / "codex" / "skills" / "career-compass"
    assert agents_symlink.resolve() == codex_skill_dir.resolve()


def test_gitignore_matches_college_plans_directory():
    result = subprocess.run(
        ["git", "check-ignore", "-v", "roadmaps/college-plans/report-example.md"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0
    assert ".gitignore" in result.stdout
