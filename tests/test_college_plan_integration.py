"""Integration checks for the college-plan skill: report round-trip,
directory isolation from skillpath's own roadmaps/, resolve-profile-skills
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


def test_report_round_trips_exactly(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps" / "college-plans"
    frontmatter = _sample_college_plan_frontmatter()

    path = report_state.write_report(str(roadmaps_dir), frontmatter, "# Body\n")
    read_back = report_state.read_report(path)

    assert read_back == frontmatter


def test_directory_isolation_between_skillpath_and_college_plan(tmp_path):
    roadmaps_root = tmp_path / "roadmaps"

    skillpath_frontmatter = {
        "report_id": "11111111-1111-1111-1111-111111111111",
        "generated_at": "2026-08-19T09:00:00+00:00",
        "target_state": "ML Engineer",
    }
    college_plan_frontmatter = {
        "report_id": "22222222-2222-2222-2222-222222222222",
        "generated_at": "2026-08-19T09:30:00+00:00",
        "target_state": "Data Scientist",
    }

    report_state.write_report(str(roadmaps_root), skillpath_frontmatter, "# skillpath\n")
    report_state.write_report(
        str(roadmaps_root / "college-plans"), college_plan_frontmatter, "# college-plan\n"
    )

    last = report_state.get_last_report(str(roadmaps_root))
    assert last["report_id"] == skillpath_frontmatter["report_id"]


def test_resolve_profile_skills_cli_matches_documented_invocation():
    result = subprocess.run(
        [
            "python3",
            str(REPO_ROOT / ".claude" / "skills" / "skillpath" / "scripts" / "resolution.py"),
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
    canonical_reference = REPO_ROOT / ".claude" / "skills" / "college-plan" / "reference"
    canonical_scripts = REPO_ROOT / ".claude" / "skills" / "college-plan" / "scripts"

    codex_reference = REPO_ROOT / "codex" / "skills" / "college-plan" / "reference"
    codex_scripts = REPO_ROOT / "codex" / "skills" / "college-plan" / "scripts"

    assert codex_reference.resolve() == canonical_reference.resolve()
    assert codex_scripts.resolve() == canonical_scripts.resolve()

    agents_symlink = REPO_ROOT / ".agents" / "skills" / "college-plan"
    codex_skill_dir = REPO_ROOT / "codex" / "skills" / "college-plan"
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
