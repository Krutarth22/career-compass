"""Tests for resolution.py (resolve_skill, resolve_track) and gap_state.py
(reconcile_assessments).
"""

from datetime import datetime, timezone

import gap_state
import resolution

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
    profile = _profile(
        current_skills=[{"skill": "rag", "proficiency": "practiced"}]
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
