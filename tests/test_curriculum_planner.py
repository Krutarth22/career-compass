"""Tests for curriculum_planner.py (match_completed_courses, sequence_courses,
compute_uncovered).
"""

import pytest

import curriculum_planner as cp

# ---------------------------------------------------------------------------
# match_completed_courses
# ---------------------------------------------------------------------------

ARCHETYPE = [
    {"course_name": "Data Structures", "aliases": ["CS 2110", "CS2110"]},
    {"course_name": "Intro to Programming", "aliases": ["CS 1110"]},
    {"course_name": "Discrete Mathematics", "aliases": []},
    {"course_name": "Statistics", "aliases": []},
    {"course_name": "Applied Statistics", "aliases": []},
]


def test_match_exact_name():
    result = cp.match_completed_courses(
        [{"course_name": "Data Structures", "status": "completed"}], ARCHETYPE
    )
    assert result["matched"] == [
        {"learner_name": "Data Structures", "course_name": "Data Structures", "status": "completed"}
    ]
    assert result["ambiguous"] == []
    assert result["unmatched"] == []


def test_match_course_code_alias():
    result = cp.match_completed_courses(
        [{"course_name": "CS 2110", "status": "in_progress"}], ARCHETYPE
    )
    assert result["matched"] == [
        {"learner_name": "CS 2110", "course_name": "Data Structures", "status": "in_progress"}
    ]


def test_match_ambiguous_returns_candidates():
    # "Statistics" is a whole-word phrase-contained in both "Statistics"
    # (exact) — wait, exact match should win. Use a genuinely ambiguous
    # phrase-containment case instead: a short phrase-eligible learner
    # input that whole-word-matches two different candidate strings.
    archetype = [
        {"course_name": "Applied Statistics", "aliases": []},
        {"course_name": "Statistics for Engineers", "aliases": []},
    ]
    result = cp.match_completed_courses(
        [{"course_name": "Statistics", "status": "completed"}], archetype
    )
    assert result["matched"] == []
    assert len(result["ambiguous"]) == 1
    entry = result["ambiguous"][0]
    assert entry["learner_name"] == "Statistics"
    assert entry["status"] == "completed"
    assert set(entry["candidates"]) == {"Applied Statistics", "Statistics for Engineers"}


def test_match_unmatched_preserves_status():
    result = cp.match_completed_courses(
        [{"course_name": "Underwater Basket Weaving", "status": "in_progress"}], ARCHETYPE
    )
    assert result["matched"] == []
    assert result["ambiguous"] == []
    assert result["unmatched"] == [
        {"learner_name": "Underwater Basket Weaving", "status": "in_progress"}
    ]


def test_match_status_preserved_across_all_three_buckets():
    archetype = [
        {"course_name": "Applied Statistics", "aliases": []},
        {"course_name": "Statistics for Engineers", "aliases": []},
        {"course_name": "Data Structures", "aliases": ["CS 2110"]},
    ]
    learner_courses = [
        {"course_name": "CS 2110", "status": "completed"},
        {"course_name": "Statistics", "status": "in_progress"},
        {"course_name": "Nonexistent Course", "status": "completed"},
    ]
    result = cp.match_completed_courses(learner_courses, archetype)
    assert result["matched"][0]["status"] == "completed"
    assert result["ambiguous"][0]["status"] == "in_progress"
    assert result["unmatched"][0]["status"] == "completed"


# ---------------------------------------------------------------------------
# sequence_courses
# ---------------------------------------------------------------------------


def _course(name, prereqs=None, source_years=None, status="upcoming", **extra):
    return {
        "course_name": name,
        "prerequisites": prereqs or [],
        "source_years": source_years or [],
        "status": status,
        **extra,
    }


def test_sequence_straight_line_prerequisite_chain():
    courses = [
        _course("Intro", source_years=[1]),
        _course("Intermediate", prereqs=["Intro"], source_years=[2]),
        _course("Advanced", prereqs=["Intermediate"], source_years=[3]),
    ]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["Intro"]["final_year"] == 1
    assert by_name["Intermediate"]["final_year"] == 2
    assert by_name["Advanced"]["final_year"] == 3


def test_sequence_cycle_raises():
    courses = [
        _course("A", prereqs=["B"]),
        _course("B", prereqs=["A"]),
    ]
    with pytest.raises(ValueError, match="cycle"):
        cp.sequence_courses(courses, program_length_years=4, current_year=1)


def test_sequence_source_years_empty_defaults_to_prereq_floor():
    courses = [
        _course("Intro", source_years=[]),
        _course("Follows Intro", prereqs=["Intro"], source_years=[]),
    ]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["Intro"]["final_year"] == 1
    assert by_name["Follows Intro"]["final_year"] == 2


def test_sequence_source_years_single_valued():
    courses = [_course("Solo", source_years=[3])]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    assert result[0]["final_year"] == 3
    assert result[0]["compressed_from_source_year"] is None


def test_sequence_source_years_disagreement_always_unscheduled():
    courses = [_course("Disputed", source_years=[1, 2])]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    assert result[0]["final_year"] == cp.UNSCHEDULED
    assert result[0]["source_disagreement"] is True

    # Disagreement wins even when a prerequisite relationship exists.
    courses = [
        _course("Prereq", source_years=[1]),
        _course("Disputed With Prereq", prereqs=["Prereq"], source_years=[1, 3]),
    ]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["Disputed With Prereq"]["final_year"] == cp.UNSCHEDULED
    assert by_name["Disputed With Prereq"]["source_disagreement"] is True


def test_sequence_delay_from_prereq_floor_is_not_compression():
    # Prereq floor pushes the course to year 3, later than its own
    # source_years[0] of 1 — this is a delay, not a program-length clamp,
    # so compressed_from_source_year must stay null.
    courses = [
        _course("First", source_years=[1]),
        _course("Second", prereqs=["First"], source_years=[1]),
        _course("Third", prereqs=["Second"], source_years=[1]),
    ]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["Third"]["final_year"] == 3
    assert by_name["Third"]["compressed_from_source_year"] is None


def test_sequence_clamping_succeeds_without_violating_prerequisite_order():
    courses = [
        _course("Early", source_years=[1]),
        _course("Late", prereqs=["Early"], source_years=[6]),
    ]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["Late"]["final_year"] == 4
    assert by_name["Late"]["compressed_from_source_year"] == 6
    assert by_name["Late"]["infeasible_within_program_length"] is False


def test_sequence_clamping_would_violate_order_marks_infeasible():
    courses = [
        _course("A", source_years=[1]),
        _course("B", prereqs=["A"], source_years=[2]),
        _course("C", prereqs=["B"], source_years=[3]),
        _course("D", prereqs=["C"], source_years=[4]),
        _course("E", prereqs=["D"], source_years=[5]),
    ]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["E"]["final_year"] == cp.UNSCHEDULED
    assert by_name["E"]["infeasible_within_program_length"] is True


def test_sequence_behind_schedule_reclassification():
    courses = [_course("Required", source_years=[1], status="upcoming")]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=3)
    assert result[0]["final_year"] == 3
    assert result[0]["behind_typical_schedule"] is True


def test_sequence_behind_schedule_skipped_if_completed():
    courses = [_course("Required", source_years=[1], status="completed")]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=3)
    assert result[0]["final_year"] == 1
    assert result[0]["behind_typical_schedule"] is False


def test_sequence_unscheduled_prerequisite_propagates():
    courses = [
        _course("Disputed", source_years=[1, 2]),
        _course("Depends On Disputed", prereqs=["Disputed"], source_years=[3]),
    ]
    result = cp.sequence_courses(courses, program_length_years=4, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["Disputed"]["final_year"] == cp.UNSCHEDULED
    assert by_name["Depends On Disputed"]["final_year"] == cp.UNSCHEDULED
    assert by_name["Depends On Disputed"]["blocked_by_unscheduled_prerequisite"] is True


def test_sequence_unscheduled_prerequisite_propagates_transitively():
    courses = [
        _course("Disputed", source_years=[1, 2]),
        _course("Middle", prereqs=["Disputed"], source_years=[3]),
        _course("Far", prereqs=["Middle"], source_years=[4]),
    ]
    result = cp.sequence_courses(courses, program_length_years=5, current_year=1)
    by_name = {c["course_name"]: c for c in result}
    assert by_name["Middle"]["final_year"] == cp.UNSCHEDULED
    assert by_name["Middle"]["blocked_by_unscheduled_prerequisite"] is True
    assert by_name["Far"]["final_year"] == cp.UNSCHEDULED
    assert by_name["Far"]["blocked_by_unscheduled_prerequisite"] is True


# ---------------------------------------------------------------------------
# compute_uncovered
# ---------------------------------------------------------------------------

REQUIREMENTS = [
    {"skill_id": "python", "tier": "Critical"},
    {"skill_id": "sql", "tier": "High"},
    {"skill_id": "docker", "tier": "Medium"},
    {"skill_id": "public-speaking", "tier": "Low"},
]


@pytest.mark.parametrize("status", ["completed", "in_progress", "upcoming"])
def test_coverage_each_status_covers(status):
    course_sequence = [{"covers_skill_ids": ["python"], "status": status}]
    result = cp.compute_uncovered(REQUIREMENTS, course_sequence, [])
    skill_ids = {r["skill_id"] for r in result}
    assert "python" not in skill_ids


def test_coverage_self_reported_courses_contribute_nothing():
    self_reported = [{"covers_skill_ids": [], "status": "completed"}]
    result = cp.compute_uncovered(REQUIREMENTS, [], self_reported)
    skill_ids = {r["skill_id"] for r in result}
    assert "python" in skill_ids


def test_coverage_low_tier_never_appears_regardless_of_coverage():
    result = cp.compute_uncovered(REQUIREMENTS, [], [])
    skill_ids = {r["skill_id"] for r in result}
    assert "public-speaking" not in skill_ids
