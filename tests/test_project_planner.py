"""Tests for project_planner.py — deterministic project-selection algorithm.

Templates are constructed as plain dicts matching template_loader's output
shape ({"frontmatter": {...}, "_filename": ...}) rather than real files on
disk, since project_planner's functions are pure and take already-loaded
template dicts.
"""

import project_planner as pp


def make_template(
    filename,
    role="core",
    estimated_hours=10,
    skill_tags=None,
    skill_prerequisites=None,
    project_prerequisites=None,
    prerequisite_learning_hours=0,
):
    return {
        "frontmatter": {
            "title": filename,
            "track": "test-track",
            "difficulty_tier": "intermediate",
            "estimated_hours": estimated_hours,
            "role": role,
            "skill_tags": skill_tags or [],
            "skill_prerequisites": skill_prerequisites or [],
            "project_prerequisites": project_prerequisites or [],
            "prerequisite_learning_hours": prerequisite_learning_hours,
        },
        "sections": {},
        "_filename": filename,
    }


def make_gap(skill_id, tier="High", status="open"):
    return {"skill_id": skill_id, "tier": tier, "status": status}


# ---------------------------------------------------------------------------
# filter_gap_assessments
# ---------------------------------------------------------------------------


def test_filter_gap_assessments_keeps_open_and_practiced_critical_high_medium():
    gaps = [
        make_gap("a", tier="Critical", status="open"),
        make_gap("b", tier="High", status="practiced"),
        make_gap("c", tier="Medium", status="open"),
        make_gap("d", tier="Low", status="open"),
        make_gap("e", tier="Critical", status="confirmed-closed"),
    ]
    result = pp.filter_gap_assessments(gaps)
    assert {g["skill_id"] for g in result} == {"a", "b", "c"}


# ---------------------------------------------------------------------------
# gap_weight
# ---------------------------------------------------------------------------


def test_gap_weight_tiers_and_status_multiplier():
    assert pp.gap_weight(make_gap("a", tier="Critical", status="open")) == 8
    assert pp.gap_weight(make_gap("a", tier="High", status="open")) == 4
    assert pp.gap_weight(make_gap("a", tier="Medium", status="open")) == 1
    assert pp.gap_weight(make_gap("a", tier="Critical", status="practiced")) == 4
    assert pp.gap_weight(make_gap("a", tier="Medium", status="practiced")) == 0.5


# ---------------------------------------------------------------------------
# candidate_pool
# ---------------------------------------------------------------------------


def test_candidate_pool_filters_by_role_and_skill_overlap():
    gaps = [make_gap("rag"), make_gap("docker")]
    templates = [
        make_template("01.md", role="core", skill_tags=["rag"]),
        make_template("02.md", role="core", skill_tags=["kubernetes"]),
        make_template("03.md", role="capstone", skill_tags=["docker"]),
    ]
    result = pp.candidate_pool(templates, gaps)
    assert [t["_filename"] for t in result] == ["01.md"]


# ---------------------------------------------------------------------------
# unmet_prerequisite_hours
# ---------------------------------------------------------------------------


def test_unmet_prerequisite_hours_all_held_returns_zero():
    t = make_template(
        "01.md",
        skill_prerequisites=["python"],
        prerequisite_learning_hours=5,
    )
    assert pp.unmet_prerequisite_hours(t, {"python"}) == 0


def test_unmet_prerequisite_hours_missing_prereq_returns_full_hours():
    t = make_template(
        "01.md",
        skill_prerequisites=["python", "sql"],
        prerequisite_learning_hours=5,
    )
    assert pp.unmet_prerequisite_hours(t, {"python"}) == 5


def test_unmet_prerequisite_hours_no_prereqs_returns_zero():
    t = make_template("01.md", skill_prerequisites=[], prerequisite_learning_hours=5)
    assert pp.unmet_prerequisite_hours(t, set()) == 0


# ---------------------------------------------------------------------------
# select_core_projects — marginal-coverage scoring
# ---------------------------------------------------------------------------


def test_select_prefers_multi_gap_template_over_single_gap_templates():
    # Template A covers both gaps (score 8+4=12 on first pick).
    # B covers only the Critical gap (score 8), C only the High gap (score 4).
    # Greedy must pick A first since its single-pick score beats either
    # alone, even though B+C together would eventually cover the same gaps.
    gaps = [
        make_gap("rag", tier="Critical", status="open"),
        make_gap("docker", tier="High", status="open"),
    ]
    a = make_template("a-multi.md", estimated_hours=10, skill_tags=["rag", "docker"])
    b = make_template("b-single.md", estimated_hours=10, skill_tags=["rag"])
    c = make_template("c-single.md", estimated_hours=10, skill_tags=["docker"])
    candidates = [a, b, c]

    selected = pp.select_core_projects(candidates, candidates, gaps, set(), budget_hours=100)
    assert selected[0]["_filename"] == "a-multi.md"
    # A alone covers everything; B and C now have marginal score 0 and are
    # not selected.
    assert [s["_filename"] for s in selected] == ["a-multi.md"]


# ---------------------------------------------------------------------------
# select_core_projects — tie-break determinism
# ---------------------------------------------------------------------------


def test_select_tie_break_deterministic_and_repeatable():
    # Two templates cover disjoint gaps of equal weight (tied score), equal
    # hours, equal unmet prereq hours -> tie-break falls to filename order.
    gaps = [
        make_gap("skill-x", tier="High", status="open"),
        make_gap("skill-y", tier="High", status="open"),
    ]
    z = make_template("z-tied.md", estimated_hours=10, skill_tags=["skill-y"])
    a = make_template("a-tied.md", estimated_hours=10, skill_tags=["skill-x"])
    candidates = [z, a]  # deliberately out-of-alphabetical input order

    run1 = pp.select_core_projects(candidates, candidates, gaps, set(), budget_hours=100)
    run2 = pp.select_core_projects(candidates, candidates, gaps, set(), budget_hours=100)

    assert run1 == run2
    # Alphabetically first filename wins the tie and is picked first.
    assert [s["_filename"] for s in run1] == ["a-tied.md", "z-tied.md"]


# ---------------------------------------------------------------------------
# select_core_projects — project_prerequisites auto-inclusion
# ---------------------------------------------------------------------------


def test_select_auto_includes_project_prerequisites():
    gaps = [make_gap("rag", tier="High", status="open")]
    prereq = make_template("00-setup.md", estimated_hours=3, skill_tags=[])
    main = make_template(
        "01-rag.md",
        estimated_hours=10,
        skill_tags=["rag"],
        project_prerequisites=["00-setup.md"],
    )
    all_templates = [prereq, main]
    candidates = [main]  # prereq covers no gap itself, so isn't in the pool

    selected = pp.select_core_projects(candidates, all_templates, gaps, set(), budget_hours=100)
    assert [s["_filename"] for s in selected] == ["00-setup.md", "01-rag.md"]
    assert selected[0]["covered_gap_skill_ids"] == []
    assert selected[1]["covered_gap_skill_ids"] == ["rag"]


# ---------------------------------------------------------------------------
# select_core_projects — skill_prerequisites already satisfied
# ---------------------------------------------------------------------------


def test_select_does_not_add_hours_for_already_satisfied_skill_prerequisite():
    gaps = [make_gap("rag", tier="High", status="open")]
    t = make_template(
        "01-rag.md",
        estimated_hours=10,
        skill_tags=["rag"],
        skill_prerequisites=["python"],
        prerequisite_learning_hours=20,
    )
    profile_skill_ids = {"python"}  # already held

    selected = pp.select_core_projects([t], [t], gaps, profile_skill_ids, budget_hours=100)
    assert len(selected) == 1
    assert selected[0]["unmet_prerequisite_hours"] == 0

    # Same scenario but python NOT held -> the 20 hours should count and
    # would block selection under a tight budget.
    selected_tight = pp.select_core_projects([t], [t], gaps, set(), budget_hours=15)
    assert selected_tight == []  # 10 + 20 = 30 > 15 budget


# ---------------------------------------------------------------------------
# select_core_projects — 4-project cap
# ---------------------------------------------------------------------------


def test_select_caps_at_four_core_projects_by_default():
    gaps = [make_gap(f"skill-{i}", tier="High", status="open") for i in range(6)]
    templates = [
        make_template(f"{i:02d}.md", estimated_hours=5, skill_tags=[f"skill-{i}"])
        for i in range(6)
    ]
    # Budget is generous enough that all 6 would fit on hours alone, but not
    # generous enough to trigger the 5th-project exception (< 50% of budget
    # remains after 4 picks: 20 hours used out of 30 leaves 10, which is
    # < 15), so the plain 4-project cap is the binding constraint.
    selected = pp.select_core_projects(templates, templates, gaps, set(), budget_hours=30)
    assert len(selected) == 4


# ---------------------------------------------------------------------------
# select_core_projects — 5th-project generous-budget exception
# ---------------------------------------------------------------------------


def test_select_fifth_project_exception_fires_with_generous_budget():
    # 6 candidates, each 5 hours, each covering a distinct gap of equal
    # weight. Budget 100 -> after 4 picks (20 hours used), 80 remain, which
    # is >= 50% of 100, so a 5th is allowed.
    gaps = [make_gap(f"skill-{i}", tier="High", status="open") for i in range(6)]
    templates = [
        make_template(f"{i:02d}.md", estimated_hours=5, skill_tags=[f"skill-{i}"])
        for i in range(6)
    ]
    selected = pp.select_core_projects(templates, templates, gaps, set(), budget_hours=100)
    assert len(selected) == 5
    assert selected[4].get("generous_budget_exception") is True
    assert all(not s.get("generous_budget_exception") for s in selected[:4])


def test_select_fifth_project_exception_does_not_fire_with_tight_budget():
    # Same setup, but budget 25: after 4 picks at 5 hours each (20 hours
    # used), only 5 remain, which is < 50% of 25 -> no 5th project.
    gaps = [make_gap(f"skill-{i}", tier="High", status="open") for i in range(6)]
    templates = [
        make_template(f"{i:02d}.md", estimated_hours=5, skill_tags=[f"skill-{i}"])
        for i in range(6)
    ]
    selected = pp.select_core_projects(templates, templates, gaps, set(), budget_hours=25)
    assert len(selected) == 4
    assert all(not s.get("generous_budget_exception") for s in selected)


# ---------------------------------------------------------------------------
# plan — shortfall
# ---------------------------------------------------------------------------


def test_plan_shortfall_true_when_fewer_than_two_core_projects_selected():
    gaps = [make_gap("rag", tier="High", status="open")]
    template = make_template("01-rag.md", estimated_hours=10, skill_tags=["rag"])
    capstone = make_template(
        "99-capstone.md", role="capstone", estimated_hours=20, skill_tags=["rag"]
    )
    track_templates = [template, capstone]
    profile = {"current_skills": []}

    # Budget too small for even one core project.
    result = pp.plan(track_templates, gaps, profile, budget_hours=1)
    assert result["shortfall"] is True
    core_count = sum(
        1 for p in result["projects"] if p["frontmatter"]["role"] != "capstone"
    )
    assert core_count in (0, 1)


def test_plan_no_shortfall_when_two_or_more_core_projects_selected():
    gaps = [
        make_gap("rag", tier="High", status="open"),
        make_gap("docker", tier="High", status="open"),
    ]
    t1 = make_template("01.md", estimated_hours=10, skill_tags=["rag"])
    t2 = make_template("02.md", estimated_hours=10, skill_tags=["docker"])
    profile = {"current_skills": []}

    result = pp.plan([t1, t2], gaps, profile, budget_hours=100)
    assert result["shortfall"] is False
    core_count = sum(
        1 for p in result["projects"] if p["frontmatter"]["role"] != "capstone"
    )
    assert core_count == 2


# ---------------------------------------------------------------------------
# sequence_projects — capstone always last
# ---------------------------------------------------------------------------


def test_sequence_capstone_always_last_regardless_of_topo_order():
    # Selection order deliberately has the "later" (dependent) project
    # first; topo sort must still put prereqs before dependents, and the
    # capstone must land last regardless.
    prereq = make_template("00-foundation.md", estimated_hours=5)
    dependent = make_template(
        "01-advanced.md", estimated_hours=5, project_prerequisites=["00-foundation.md"]
    )
    capstone = make_template("99-capstone.md", role="capstone", estimated_hours=15)
    selected_core = [dependent, prereq]  # out of topo order on purpose

    sequenced = pp.sequence_projects(selected_core, capstone, selected_core, set())
    filenames = [t["_filename"] for t in sequenced]
    assert filenames == ["00-foundation.md", "01-advanced.md", "99-capstone.md"]


def test_sequence_no_capstone_returns_core_only():
    t = make_template("01.md", estimated_hours=5)
    sequenced = pp.sequence_projects([t], None, [t], set())
    assert [x["_filename"] for x in sequenced] == ["01.md"]


# ---------------------------------------------------------------------------
# sequence_projects / select_core_projects — cycle detection
# ---------------------------------------------------------------------------


def test_sequence_raises_on_cycle_in_project_prerequisites():
    a = make_template("a.md", estimated_hours=5, project_prerequisites=["b.md"])
    b = make_template("b.md", estimated_hours=5, project_prerequisites=["a.md"])

    try:
        pp.sequence_projects([a, b], None, [a, b], set())
        assert False, "expected ValueError for cycle"
    except ValueError as exc:
        assert "cycle" in str(exc).lower()


def test_select_core_projects_raises_on_cycle_in_project_prerequisites():
    gaps = [make_gap("x", tier="High", status="open")]
    a = make_template(
        "a.md", estimated_hours=5, skill_tags=["x"], project_prerequisites=["b.md"]
    )
    b = make_template("b.md", estimated_hours=5, project_prerequisites=["a.md"])
    all_templates = [a, b]

    try:
        pp.select_core_projects([a], all_templates, gaps, set(), budget_hours=100)
        assert False, "expected ValueError for cycle"
    except ValueError as exc:
        assert "cycle" in str(exc).lower()
