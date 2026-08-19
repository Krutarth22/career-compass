"""Tests for resolution.py (resolve_skill, resolve_track) and gap_state.py
(reconcile_assessments).
"""

from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

import gap_state
import resolution

REAL_TAXONOMY_PATH = (
    Path(__file__).resolve().parents[1]
    / ".claude"
    / "skills"
    / "skillpath"
    / "reference"
    / "skill-taxonomy.yaml"
)


@pytest.fixture(scope="module")
def real_taxonomy():
    """The REAL shipped taxonomy — the false-positive regressions below are
    only meaningful against the actual data that produced them.
    """
    with open(REAL_TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TAXONOMY = [
    {
        "id": "retrieval-augmented-generation",
        "display_name": "Retrieval-Augmented Generation (RAG)",
        "synonyms": ["rag", "retrieval augmented generation"],
    },
    {
        "id": "python",
        "display_name": "Python",
        "synonyms": ["python programming", "python 3"],
    },
    {
        "id": "docker",
        "display_name": "Docker",
        "synonyms": ["containerization", "containers"],
    },
]

TRACK_ALIASES = {
    "ai-ml-engineer": {
        "aliases": [
            "ai engineer",
            "ml engineer",
            "machine learning engineer",
        ]
    },
    "backend-engineer": {
        "aliases": [
            "backend engineer",
            "backend developer",
        ]
    },
}


# ---------------------------------------------------------------------------
# resolve_skill
# ---------------------------------------------------------------------------


def test_resolve_skill_exact_match():
    result = resolution.resolve_skill("Docker", TAXONOMY)
    assert result == {"id": "docker", "unmapped": False}


def test_resolve_skill_synonym_match():
    result = resolution.resolve_skill("Retrieval Augmented Generation", TAXONOMY)
    assert result == {"id": "retrieval-augmented-generation", "unmapped": False}


def test_resolve_skill_provisional_unmapped_fallback():
    result = resolution.resolve_skill("  Kubernetes Operators!! ", TAXONOMY)
    assert result["unmapped"] is True
    assert result["id"] == "kubernetes-operators"


# ---------------------------------------------------------------------------
# resolve_skill — false-positive substring regressions (I1)
#
# The old matcher used raw bidirectional substring containment, so the
# 3-letter synonym "rag" matched inside "storage", "average" and
# "leverage", and the 2-letter "ml" matched via "serving ml models". These
# must now all fall through to unmapped.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected_id",
    [
        ("storage", "storage"),
        ("average", "average"),
        ("leverage existing tools", "leverage-existing-tools"),
    ],
)
def test_resolve_skill_short_synonym_never_matches_inside_a_word(
    real_taxonomy, text, expected_id
):
    result = resolution.resolve_skill(text, real_taxonomy)
    assert result == {"id": expected_id, "unmapped": True}


def test_resolve_skill_two_letter_synonym_does_not_match_via_containment(
    real_taxonomy,
):
    # "ml" used to resolve to model-serving via its "serving ml models"
    # synonym. A bare "ml" is genuinely ambiguous — refuse to guess.
    assert resolution.resolve_skill("ml", real_taxonomy)["unmapped"] is True


def test_resolve_skill_legitimate_matches_still_work_on_real_taxonomy(real_taxonomy):
    assert resolution.resolve_skill("python", real_taxonomy) == {
        "id": "python",
        "unmapped": False,
    }
    # Multi-token input resolving via a whole-word match on the short-but-
    # long-enough id "python".
    assert resolution.resolve_skill("python scripting", real_taxonomy) == {
        "id": "python",
        "unmapped": False,
    }
    # Exact synonym matches, case- and separator-insensitive.
    assert resolution.resolve_skill("RAG", real_taxonomy)["id"] == (
        "retrieval-augmented-generation"
    )
    assert resolution.resolve_skill("Python 3", real_taxonomy)["id"] == "python"
    assert resolution.resolve_skill("machine learning basics", real_taxonomy)["id"] == (
        "ml-fundamentals"
    )
    assert resolution.resolve_skill("SQL", real_taxonomy)["id"] == "sql"


def test_resolve_skill_normalizes_separators():
    assert resolution.resolve_skill("Python_Programming", TAXONOMY)["id"] == "python"
    assert resolution.resolve_skill("python-programming", TAXONOMY)["id"] == "python"


# ---------------------------------------------------------------------------
# resolve_profile_skills (C1)
# ---------------------------------------------------------------------------


def test_resolve_profile_skills_maps_real_taxonomy_skill(real_taxonomy):
    result = resolution.resolve_profile_skills(
        [{"skill": "Python", "proficiency": "practiced", "evidence": "side projects"}],
        real_taxonomy,
    )
    assert result == [
        {
            "skill": "Python",
            "proficiency": "practiced",
            "evidence": "side projects",
            "skill_id": "python",
        }
    ]


def test_resolve_profile_skills_keeps_unmapped_skill_as_provisional_slug(
    real_taxonomy,
):
    result = resolution.resolve_profile_skills(
        [{"skill": "CAD Design", "proficiency": "proficient"}], real_taxonomy
    )
    assert result[0]["skill_id"] == "cad-design"
    # Original free text is preserved for display.
    assert result[0]["skill"] == "CAD Design"


def test_resolve_profile_skills_is_case_insensitive(real_taxonomy):
    lower = resolution.resolve_profile_skills(
        [{"skill": "docker", "proficiency": "practiced"}], real_taxonomy
    )
    upper = resolution.resolve_profile_skills(
        [{"skill": "DOCKER", "proficiency": "practiced"}], real_taxonomy
    )
    assert lower[0]["skill_id"] == upper[0]["skill_id"] == "docker"


def test_resolve_profile_skills_does_not_mutate_input():
    entries = [{"skill": "Docker", "proficiency": "practiced"}]
    resolution.resolve_profile_skills(entries, TAXONOMY)
    assert entries == [{"skill": "Docker", "proficiency": "practiced"}]


def test_resolve_profile_skills_empty_list():
    assert resolution.resolve_profile_skills([], TAXONOMY) == []


# ---------------------------------------------------------------------------
# resolve_track
# ---------------------------------------------------------------------------


def test_resolve_track_alias_match():
    assert resolution.resolve_track("AI Engineer", TRACK_ALIASES) == "ai-ml-engineer"


def test_resolve_track_no_match():
    assert resolution.resolve_track("Product Manager", TRACK_ALIASES) is None


def test_resolve_track_level_word_stripping():
    senior = resolution.resolve_track("Senior AI Engineer", TRACK_ALIASES)
    plain = resolution.resolve_track("AI Engineer", TRACK_ALIASES)
    assert senior == plain == "ai-ml-engineer"


# ---------------------------------------------------------------------------
# reconcile_assessments
# ---------------------------------------------------------------------------

NOW = datetime(2026, 8, 19, 12, 0, 0, tzinfo=timezone.utc)
THIS_REPORT_ID = "report-current-0001"


def _requirement(skill_id="rag", tier="Critical"):
    return {"skill_id": skill_id, "tier": tier}


def _profile(current_skills=None):
    return {"current_skills": current_skills or []}


def test_open_to_practiced_via_project_completed_event():
    requirements = [_requirement()]
    profile = _profile()
    prior_assessments = [
        {
            "skill_id": "rag",
            "tier": "Critical",
            "status": "open",
            "first_seen_at": "2026-07-01T00:00:00+00:00",
            "first_seen_report_id": "report-old-0001",
        }
    ]
    tracker_events = [
        {
            "occurred_at": "2026-07-15T00:00:00+00:00",
            "event_type": "project_completed",
            "related_skill_ids": ["rag"],
            "confirmed_for_target_role": "",
            "confirmed_for_target_level": "",
        }
    ]

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments,
        tracker_events,
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["status"] == "practiced"
    assert result[0]["first_seen_at"] == "2026-07-01T00:00:00+00:00"
    assert result[0]["first_seen_report_id"] == "report-old-0001"


def test_practiced_to_confirmed_closed_via_target_matching_event():
    requirements = [_requirement()]
    profile = _profile()
    prior_assessments = [
        {
            "skill_id": "rag",
            "tier": "Critical",
            "status": "practiced",
            "first_seen_at": "2026-07-01T00:00:00+00:00",
            "first_seen_report_id": "report-old-0001",
        }
    ]
    tracker_events = [
        {
            "occurred_at": "2026-07-15T00:00:00+00:00",
            "event_type": "project_completed",
            "related_skill_ids": ["rag"],
            "confirmed_for_target_role": "",
            "confirmed_for_target_level": "",
        },
        {
            "occurred_at": "2026-08-01T00:00:00+00:00",
            "event_type": "skill_confirmed",
            "related_skill_ids": ["rag"],
            "confirmed_for_target_role": "ai-ml-engineer",
            "confirmed_for_target_level": "senior",
        },
    ]

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments,
        tracker_events,
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["status"] == "confirmed-closed"
    assert result[0]["first_seen_at"] == "2026-07-01T00:00:00+00:00"
    assert result[0]["first_seen_report_id"] == "report-old-0001"


def test_confirmed_closed_stays_closed_on_repeat_run_no_target_change():
    requirements = [_requirement()]
    profile = _profile()
    prior_assessments = [
        {
            "skill_id": "rag",
            "tier": "Critical",
            "status": "confirmed-closed",
            "first_seen_at": "2026-07-01T00:00:00+00:00",
            "first_seen_report_id": "report-old-0001",
        }
    ]
    tracker_events = [
        {
            "occurred_at": "2026-08-01T00:00:00+00:00",
            "event_type": "skill_confirmed",
            "related_skill_ids": ["rag"],
            "confirmed_for_target_role": "ai-ml-engineer",
            "confirmed_for_target_level": "senior",
        },
    ]

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments,
        tracker_events,
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["status"] == "confirmed-closed"
    assert result[0]["first_seen_at"] == "2026-07-01T00:00:00+00:00"
    assert result[0]["first_seen_report_id"] == "report-old-0001"


def test_confirmed_closed_does_not_carry_forward_when_target_differs():
    """A skill_confirmed event recorded for a different target_role/level
    is a real historical event but must not close the gap for this run's
    (different) target — falls back through steps 2-4 to a fresh Pass-1
    assessment instead.
    """
    requirements = [_requirement()]
    # Pass-1 coverage is false and no completion event -> should fall back
    # to "open", not stay "confirmed-closed".
    profile = _profile()
    prior_assessments = [
        {
            "skill_id": "rag",
            "tier": "Critical",
            "status": "confirmed-closed",
            "first_seen_at": "2026-07-01T00:00:00+00:00",
            "first_seen_report_id": "report-old-0001",
        }
    ]
    tracker_events = [
        {
            "occurred_at": "2026-08-01T00:00:00+00:00",
            "event_type": "skill_confirmed",
            "related_skill_ids": ["rag"],
            "confirmed_for_target_role": "backend-engineer",
            "confirmed_for_target_level": "senior",
        },
    ]

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments,
        tracker_events,
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["status"] == "open"
    assert result[0]["first_seen_at"] == "2026-07-01T00:00:00+00:00"
    assert result[0]["first_seen_report_id"] == "report-old-0001"


def test_confirmed_closed_target_mismatch_falls_back_to_practiced_when_covered():
    """Same target-mismatch scenario, but Pass-1 coverage now applies, so
    the fresh assessment lands on "practiced" rather than "open" — proving
    the fallback genuinely re-runs steps 2-4 rather than just defaulting.
    """
    requirements = [_requirement()]
    # Profile skills are matched by their resolved `skill_id`, not the
    # free-text `skill` field (see gap_state's PROFILE CONTRACT).
    profile = _profile(
        current_skills=[
            {"skill": "RAG", "skill_id": "rag", "proficiency": "practiced"}
        ]
    )
    prior_assessments = [
        {
            "skill_id": "rag",
            "tier": "Critical",
            "status": "confirmed-closed",
            "first_seen_at": "2026-07-01T00:00:00+00:00",
            "first_seen_report_id": "report-old-0001",
        }
    ]
    tracker_events = [
        {
            "occurred_at": "2026-08-01T00:00:00+00:00",
            "event_type": "skill_confirmed",
            "related_skill_ids": ["rag"],
            "confirmed_for_target_role": "backend-engineer",
            "confirmed_for_target_level": "senior",
        },
    ]

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments,
        tracker_events,
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["status"] == "practiced"
    assert result[0]["first_seen_at"] == "2026-07-01T00:00:00+00:00"
    assert result[0]["first_seen_report_id"] == "report-old-0001"


def test_pass1_coverage_ignores_unresolved_free_text_skill_field():
    """An entry carrying only free-text `skill` (never resolved) must not
    cover anything — gap_state matches on `skill_id` exclusively, so a
    caller that forgets to resolve gets an honest "open", not a false close.
    """
    requirements = [_requirement()]
    profile = _profile(current_skills=[{"skill": "rag", "proficiency": "proficient"}])

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments=[],
        tracker_events=[],
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["status"] == "open"


def test_first_seen_freshly_stamped_when_no_prior_assessment():
    requirements = [_requirement()]
    profile = _profile()

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments=[],
        tracker_events=[],
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["status"] == "open"
    assert result[0]["first_seen_at"] == NOW.isoformat()
    assert result[0]["first_seen_report_id"] == THIS_REPORT_ID


def test_tier_is_copied_through_unchanged():
    requirements = [_requirement(tier="Medium")]
    profile = _profile()

    result = gap_state.reconcile_assessments(
        requirements,
        profile,
        prior_assessments=[],
        tracker_events=[],
        target_role="ai-ml-engineer",
        target_level="senior",
        this_report_id=THIS_REPORT_ID,
        now=NOW,
    )

    assert result[0]["tier"] == "Medium"
