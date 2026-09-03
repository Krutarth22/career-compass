"""End-to-end pipeline integration test against the REAL shipped data.

Every other test file exercises one module against hand-built fixtures. This
one wires the whole deterministic chain together —

    profile.yaml free text
      -> resolution.resolve_profile_skills (canonical skill_ids)
      -> gap_state.reconcile_assessments   (gap statuses)
      -> project_planner.plan              (selected/sequenced projects)

— using the real `reference/skill-taxonomy.yaml` and the real
`templates/ml-engineer/` templates, so a contract break between two
modules (e.g. the C1 bug, where profile skill text was compared against
canonical ids by string equality and therefore covered nothing) shows up
here even when each module's own unit tests still pass.

`target_requirements` and their tiers are hand-constructed rather than
researched: Step 3/4 of the orchestration are LLM judgment steps with no
script, so there is nothing deterministic to exercise there.
"""

from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

import gap_state
import project_planner
import resolution
from template_loader import load_track

SKILL_DIR = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "career-compass"
TAXONOMY_PATH = SKILL_DIR / "reference" / "skill-taxonomy.yaml"
TRACK_DIR = SKILL_DIR / "templates" / "ml-engineer"

NOW = datetime(2026, 8, 19, 12, 0, 0, tzinfo=timezone.utc)
THIS_REPORT_ID = "2f8c3e1a-0b44-4a1d-9f21-6c7b8a9d0e12"

TARGET_ROLE = "ML Engineer"
TARGET_LEVEL = "Senior ML Engineer"

# A realistic free-text profile modeled on profile.yaml.example's persona (a
# mechanical engineer moving into ML), with SQL added — nothing here is
# pre-resolved, exactly as a human would type it into profile.yaml.
RAW_CURRENT_SKILLS = [
    {
        "skill": "CAD Design",
        "proficiency": "proficient",
        "evidence": "5 years designing automotive components in CATIA",
    },
    {
        "skill": "Python",
        "proficiency": "practiced",
        "evidence": "Personal projects and data analysis for engineering reports",
    },
    {
        "skill": "SQL",
        "proficiency": "practiced",
        "evidence": "Pulling test-rig telemetry out of the plant warehouse",
    },
    {
        "skill": "Excel",
        "proficiency": "proficient",
        "evidence": "Daily use for calculations and data management",
    },
    {"skill": "Thermodynamics", "proficiency": "proficient"},
]

# Plausible tiered requirements for the target role (stand-in for Step 3/4).
TARGET_REQUIREMENTS = [
    {"skill_id": "python", "tier": "Critical"},
    {"skill_id": "ml-fundamentals", "tier": "Critical"},
    {"skill_id": "model-serving", "tier": "High"},
    {"skill_id": "docker", "tier": "High"},
    {"skill_id": "feature-engineering", "tier": "High"},
    {"skill_id": "sql", "tier": "Medium"},
    {"skill_id": "data-pipelines", "tier": "Medium"},
]


@pytest.fixture(scope="module")
def taxonomy():
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def track_templates():
    return load_track(TRACK_DIR)


@pytest.fixture(scope="module")
def resolved_profile(taxonomy):
    """Step 2.5 of the orchestration: resolve free text to canonical ids."""
    return {
        "current_role": "Mechanical Engineer",
        "target_role": TARGET_ROLE,
        "target_level": TARGET_LEVEL,
        "current_skills": resolution.resolve_profile_skills(
            RAW_CURRENT_SKILLS, taxonomy
        ),
    }


@pytest.fixture(scope="module")
def gap_assessments(resolved_profile):
    return gap_state.reconcile_assessments(
        TARGET_REQUIREMENTS,
        resolved_profile,
        prior_assessments=[],
        tracker_events=[],
        target_role=TARGET_ROLE,
        target_level=TARGET_LEVEL,
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )


# ---------------------------------------------------------------------------
# Stage 1 — resolution
# ---------------------------------------------------------------------------


def test_profile_free_text_resolves_to_real_taxonomy_ids(resolved_profile):
    by_text = {e["skill"]: e["skill_id"] for e in resolved_profile["current_skills"]}
    assert by_text["Python"] == "python"
    assert by_text["SQL"] == "sql"
    # Skills with no taxonomy home stay provisional rather than being guessed
    # onto some unrelated id.
    assert by_text["CAD Design"] == "cad-design"
    assert by_text["Thermodynamics"] == "thermodynamics"


# ---------------------------------------------------------------------------
# Stage 2 — gap reconciliation
# ---------------------------------------------------------------------------


def test_skill_the_profile_genuinely_has_is_not_an_open_gap(gap_assessments):
    """The C1 regression, stated directly: the user really does have Python
    (practiced) and SQL (practiced), so neither may be reported as an open
    gap.
    """
    by_id = {g["skill_id"]: g for g in gap_assessments}
    assert by_id["python"]["status"] == "practiced"
    assert by_id["python"]["status"] != "open"
    assert by_id["sql"]["status"] == "practiced"


def test_skills_the_profile_lacks_remain_open(gap_assessments):
    by_id = {g["skill_id"]: g for g in gap_assessments}
    for skill_id in (
        "ml-fundamentals",
        "model-serving",
        "docker",
    ):
        assert by_id[skill_id]["status"] == "open", skill_id


# ---------------------------------------------------------------------------
# Stage 3 — project planning
# ---------------------------------------------------------------------------


def test_project_with_only_already_held_prerequisites_is_not_charged_hours(
    track_templates, gap_assessments, resolved_profile
):
    """feature-store-lite.md's skill_prerequisites are exactly
    ["python", "sql"] — both held at practiced — so its
    prerequisite_learning_hours (5) must not be charged. Before C1 was
    fixed, the profile's "Python"/"SQL" text never matched the canonical
    ids and the learner was charged for relearning what they already knew.
    """
    result = project_planner.plan(
        track_templates,
        gap_assessments,
        resolved_profile,
        budget_hours=15 * 24,  # weekly_time_budget_hours * horizon_weeks
    )

    by_filename = {p["_filename"]: p for p in result["projects"]}
    assert "feature-store-lite.md" in by_filename, sorted(by_filename)
    assert by_filename["feature-store-lite.md"]["unmet_prerequisite_hours"] == 0

    # Contrast: ml-model-serving-api.md also requires ml-fundamentals, which
    # the profile does NOT have, so its 10 prerequisite hours still count.
    assert by_filename["ml-model-serving-api.md"]["unmet_prerequisite_hours"] == 10


def test_unresolved_profile_would_be_charged_for_a_skill_it_has(
    track_templates, gap_assessments
):
    """Guard on the contract itself: hand plan() the RAW (unresolved)
    profile and the already-held prerequisite is charged again. This is the
    exact failure mode the resolve-profile-skills step exists to prevent.
    """
    unresolved_profile = {"current_skills": RAW_CURRENT_SKILLS}
    result = project_planner.plan(
        track_templates, gap_assessments, unresolved_profile, budget_hours=15 * 24
    )
    by_filename = {p["_filename"]: p for p in result["projects"]}
    assert by_filename["feature-store-lite.md"]["unmet_prerequisite_hours"] == 5


def test_pipeline_produces_a_usable_sequenced_plan(
    track_templates, gap_assessments, resolved_profile
):
    result = project_planner.plan(
        track_templates, gap_assessments, resolved_profile, budget_hours=15 * 24
    )

    assert result["shortfall"] is False
    assert result["projects"], "expected at least one selected project"
    # Capstone, if present, is always last.
    assert (
        result["projects"][-1]["frontmatter"]["role"] == "capstone"
    ), [p["_filename"] for p in result["projects"]]
    # A capstone's own project_prerequisites precede it.
    filenames = [p["_filename"] for p in result["projects"]]
    for prereq in result["projects"][-1]["frontmatter"]["project_prerequisites"]:
        assert filenames.index(prereq) < len(filenames) - 1


@pytest.mark.parametrize(
    "track",
    [
        "ai-engineer",
        "ml-engineer",
        "data-engineer",
        "data-analyst",
        "data-scientist",
    ],
)
def test_every_shipped_track_builds_a_complete_plan(track):
    """Smoke-test every real template set, including the newly added tracks."""
    templates = load_track(SKILL_DIR / "templates" / track)
    capstones = [t for t in templates if t["frontmatter"]["role"] == "capstone"]
    assert len(capstones) == 1

    skill_ids = sorted(
        {
            skill_id
            for template in templates
            for skill_id in template["frontmatter"]["skill_tags"]
        }
    )
    gaps = [
        {"skill_id": skill_id, "tier": "Critical", "status": "open"}
        for skill_id in skill_ids
    ]
    result = project_planner.plan(
        templates, gaps, {"current_skills": []}, budget_hours=10_000
    )

    assert result["shortfall"] is False
    assert result["projects"]
    assert result["projects"][-1]["frontmatter"]["role"] == "capstone"
