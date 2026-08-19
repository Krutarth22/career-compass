"""Unit tests for tracker_io.py."""

import csv

import pytest
import tracker_io


# ---------------------------------------------------------------------------
# append_row
# ---------------------------------------------------------------------------


def test_append_row_creates_file_with_header(tmp_path):
    csv_path = tmp_path / "tracker.csv"

    tracker_io.append_row(
        csv_path,
        "2026-01-15T10:30:00Z",
        "report_generated",
        "Career Transition Assessment",
        ["python", "machine-learning"],
        "report_20260115_001",
    )

    assert csv_path.exists()
    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == tracker_io.COLUMNS
    assert rows[1][0] == "2026-01-15T10:30:00Z"
    assert rows[1][1] == "report_generated"
    assert rows[1][3] == "python|machine-learning"


def test_append_row_appends_without_duplicating_header(tmp_path):
    csv_path = tmp_path / "tracker.csv"

    tracker_io.append_row(
        csv_path,
        "2026-01-15T10:30:00Z",
        "report_generated",
        "Item A",
        ["python"],
        "report_1",
    )
    tracker_io.append_row(
        csv_path,
        "2026-01-16T10:30:00Z",
        "project_started",
        "Item B",
        ["ml"],
        "report_1",
    )

    with open(csv_path, newline="") as f:
        rows = list(csv.reader(f))

    assert len(rows) == 3  # header + 2 rows
    assert rows[0] == tracker_io.COLUMNS


def test_append_row_rejects_invalid_event_type(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    with pytest.raises(ValueError):
        tracker_io.append_row(
            csv_path,
            "2026-01-15T10:30:00Z",
            "not_a_real_event",
            "Item A",
            [],
            "report_1",
        )
    assert not csv_path.exists()


def test_append_row_handles_commas_and_quotes_in_notes(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    tricky_notes = 'Used "scikit-learn", pandas, and numpy; cost: $0'

    tracker_io.append_row(
        csv_path,
        "2026-01-15T10:30:00Z",
        "report_generated",
        "Item A",
        ["python"],
        "report_1",
        notes=tricky_notes,
    )

    rows = tracker_io.read_rows(csv_path)
    assert rows[0]["notes"] == tricky_notes


def test_append_row_creates_parent_dirs(tmp_path):
    csv_path = tmp_path / "nested" / "dir" / "tracker.csv"
    tracker_io.append_row(
        csv_path, "2026-01-15T10:30:00Z", "report_generated", "Item A", [], "r1"
    )
    assert csv_path.exists()


# ---------------------------------------------------------------------------
# read_rows
# ---------------------------------------------------------------------------


def test_read_rows_missing_file_returns_empty_list(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    assert tracker_io.read_rows(csv_path) == []


def test_read_rows_returns_all_rows_with_split_skill_ids(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    tracker_io.append_row(
        csv_path,
        "2026-01-15T10:30:00Z",
        "report_generated",
        "Item A",
        ["python", "ml"],
        "report_1",
    )

    rows = tracker_io.read_rows(csv_path)

    assert len(rows) == 1
    assert rows[0]["related_skill_ids"] == ["python", "ml"]
    assert rows[0]["item_name"] == "Item A"


def test_read_rows_empty_related_skill_ids_becomes_empty_list(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    tracker_io.append_row(
        csv_path, "2026-01-15T10:30:00Z", "report_generated", "Item A", [], "report_1"
    )

    rows = tracker_io.read_rows(csv_path)
    assert rows[0]["related_skill_ids"] == []


def test_read_rows_filters_by_since(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    tracker_io.append_row(
        csv_path, "2026-01-01T00:00:00Z", "report_generated", "Old", [], "r1"
    )
    tracker_io.append_row(
        csv_path, "2026-02-01T00:00:00Z", "project_started", "New", [], "r1"
    )

    rows = tracker_io.read_rows(csv_path, since="2026-01-15T00:00:00Z")

    assert len(rows) == 1
    assert rows[0]["item_name"] == "New"


def test_read_rows_filters_by_event_types(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    tracker_io.append_row(
        csv_path, "2026-01-01T00:00:00Z", "report_generated", "A", [], "r1"
    )
    tracker_io.append_row(
        csv_path, "2026-01-02T00:00:00Z", "project_started", "B", [], "r1"
    )
    tracker_io.append_row(
        csv_path, "2026-01-03T00:00:00Z", "project_completed", "C", [], "r1"
    )

    rows = tracker_io.read_rows(
        csv_path, event_types=["project_started", "project_completed"]
    )

    assert {r["item_name"] for r in rows} == {"B", "C"}


def test_read_rows_skips_malformed_rows_without_crashing(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    # Write a well-formed row via the library, then hand-corrupt the file by
    # appending malformed lines (wrong column count, missing occurred_at,
    # garbage line).
    tracker_io.append_row(
        csv_path, "2026-01-01T00:00:00Z", "report_generated", "Good", [], "r1"
    )
    with open(csv_path, "a", newline="") as f:
        f.write("this is not,a valid,row at all\n")
        f.write(",project_started,Missing occurred_at,,r1,,,\n")
        f.write("2026-01-02T00:00:00Z,project_started,Extra,,r1,,,,,,too,many,cols\n")

    rows = tracker_io.read_rows(csv_path)

    # Only the well-formed row should survive; malformed rows are skipped,
    # not raised.
    assert any(r["item_name"] == "Good" for r in rows)


def test_read_rows_since_and_event_types_combined(tmp_path):
    csv_path = tmp_path / "tracker.csv"
    tracker_io.append_row(
        csv_path, "2026-01-01T00:00:00Z", "report_generated", "A", [], "r1"
    )
    tracker_io.append_row(
        csv_path, "2026-02-01T00:00:00Z", "report_generated", "B", [], "r1"
    )
    tracker_io.append_row(
        csv_path, "2026-02-02T00:00:00Z", "project_started", "C", [], "r1"
    )

    rows = tracker_io.read_rows(
        csv_path, since="2026-01-15T00:00:00Z", event_types=["report_generated"]
    )

    assert len(rows) == 1
    assert rows[0]["item_name"] == "B"


# ---------------------------------------------------------------------------
# get_last_report_meta (delegates to report_state.get_last_report)
# ---------------------------------------------------------------------------


def test_get_last_report_meta_returns_none_when_no_reports(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    roadmaps_dir.mkdir()
    assert tracker_io.get_last_report_meta(roadmaps_dir) is None


def test_get_last_report_meta_delegates_to_report_state(tmp_path):
    import report_state

    roadmaps_dir = tmp_path / "roadmaps"
    frontmatter = {
        "report_id": "12345678-aaaa-bbbb-cccc-1234567890ab",
        "generated_at": "2026-01-15T10:30:00.123456+00:00",
        "current_state": "Mechanical Engineer",
        "target_state": "ML Engineer",
        "resolved_track": None,
        "research_confidence": "high",
        "target_requirements": [],
        "gap_assessments": [],
    }
    report_state.write_report(roadmaps_dir, frontmatter, "# Roadmap\n")

    meta = tracker_io.get_last_report_meta(roadmaps_dir)

    assert meta is not None
    assert meta["report_id"] == frontmatter["report_id"]
    assert meta["target_state"] == "ML Engineer"
