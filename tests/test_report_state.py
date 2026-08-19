"""Unit tests for report_state.py."""

import time

import pytest
import report_state
import yaml


def _sample_frontmatter(
    report_id="12345678-aaaa-bbbb-cccc-1234567890ab",
    generated_at="2026-01-15T10:30:00.123456+00:00",
    target_state="ML/AI Engineer",
):
    return {
        "report_id": report_id,
        "generated_at": generated_at,
        "current_state": "Mechanical Engineer",
        "target_state": target_state,
        "resolved_track": "ai-ml-engineer",
        "research_confidence": "high",
        "target_requirements": [
            {
                "skill_id": "python",
                "unmapped": False,
                "category": "hard",
                "frequency_signal": 0.9,
                "sources": [
                    {
                        "url": "https://example.com/posting",
                        "type": "posting",
                        "title": "ML Engineer",
                        "company": "Acme",
                        "role_level": "Senior",
                        "location": "SF",
                        "posted_at": "2026-01-01",
                        "accessed_at": "2026-01-15T10:00:00+00:00",
                    }
                ],
            }
        ],
        "gap_assessments": [
            {
                "skill_id": "python",
                "tier": "Critical",
                "status": "open",
                "first_seen_at": "2026-01-15T10:30:00+00:00",
                "first_seen_report_id": report_id,
            }
        ],
    }


# ---------------------------------------------------------------------------
# write_report
# ---------------------------------------------------------------------------


def test_write_report_creates_file_with_expected_filename(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    frontmatter = _sample_frontmatter()

    path = report_state.write_report(roadmaps_dir, frontmatter, "# Roadmap\n\nBody.")

    from pathlib import Path

    p = Path(path)
    assert p.exists()
    assert p.parent == roadmaps_dir
    assert p.name == "report-20260115T103000.123456Z-12345678-ml-ai-engineer.md"


def test_write_report_content_has_frontmatter_and_body(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    frontmatter = _sample_frontmatter()

    path = report_state.write_report(roadmaps_dir, frontmatter, "# Roadmap\nBody text")

    content = open(path).read()
    assert content.startswith("---\n")
    assert "# Roadmap\nBody text" in content
    assert content.count("---") >= 2


def test_write_report_target_slug_strips_and_lowercases(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    frontmatter = _sample_frontmatter(target_state="  Staff / Principal ML Engineer!! ")

    path = report_state.write_report(roadmaps_dir, frontmatter, "body")

    from pathlib import Path

    name = Path(path).name
    assert "staff-principal-ml-engineer" in name
    assert not name.endswith("-.md")


def test_write_report_creates_roadmaps_dir_if_missing(tmp_path):
    roadmaps_dir = tmp_path / "does" / "not" / "exist"
    frontmatter = _sample_frontmatter()

    path = report_state.write_report(roadmaps_dir, frontmatter, "body")

    from pathlib import Path

    assert Path(path).exists()


# ---------------------------------------------------------------------------
# read_report
# ---------------------------------------------------------------------------


def test_read_report_round_trips_frontmatter(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    frontmatter = _sample_frontmatter()
    path = report_state.write_report(roadmaps_dir, frontmatter, "body")

    parsed = report_state.read_report(path)

    assert parsed["report_id"] == frontmatter["report_id"]
    assert parsed["target_state"] == frontmatter["target_state"]
    assert parsed["gap_assessments"][0]["skill_id"] == "python"


def test_read_report_raises_on_missing_frontmatter(tmp_path):
    path = tmp_path / "bad.md"
    path.write_text("# Just a heading\nNo frontmatter here.")

    with pytest.raises(ValueError):
        report_state.read_report(path)


def test_read_report_raises_on_unterminated_frontmatter(tmp_path):
    path = tmp_path / "bad.md"
    path.write_text("---\nreport_id: abc\nno closing delimiter\n")

    with pytest.raises(ValueError):
        report_state.read_report(path)


# ---------------------------------------------------------------------------
# get_last_report
# ---------------------------------------------------------------------------


def test_get_last_report_returns_none_when_dir_missing(tmp_path):
    assert report_state.get_last_report(tmp_path / "nope") is None


def test_get_last_report_returns_none_when_dir_empty(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    roadmaps_dir.mkdir()
    assert report_state.get_last_report(roadmaps_dir) is None


def test_get_last_report_picks_newest_by_filename_timestamp_not_mtime(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"

    older = _sample_frontmatter(
        report_id="11111111-aaaa-bbbb-cccc-111111111111",
        generated_at="2026-01-01T00:00:00.000000+00:00",
        target_state="Old Target",
    )
    newer = _sample_frontmatter(
        report_id="22222222-aaaa-bbbb-cccc-222222222222",
        generated_at="2026-06-01T00:00:00.000000+00:00",
        target_state="New Target",
    )

    # Write the "newer" report first (so if mtime were used instead of the
    # embedded filename timestamp, this test would catch the bug).
    report_state.write_report(roadmaps_dir, newer, "body")
    time.sleep(0.01)
    report_state.write_report(roadmaps_dir, older, "body")

    result = report_state.get_last_report(roadmaps_dir)

    assert result["target_state"] == "New Target"


def test_get_last_report_degrades_to_none_on_corrupt_newest_report(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    roadmaps_dir.mkdir()

    good = _sample_frontmatter(
        report_id="11111111-aaaa-bbbb-cccc-111111111111",
        generated_at="2026-01-01T00:00:00.000000+00:00",
    )
    report_state.write_report(roadmaps_dir, good, "body")

    # A corrupt report whose embedded timestamp sorts newest.
    corrupt_path = roadmaps_dir / "report-20260601T000000.000000Z-99999999-ml.md"
    corrupt_path.write_text("this is not valid frontmatter at all")

    result = report_state.get_last_report(roadmaps_dir)

    assert result is None


def test_get_last_report_returns_none_when_only_file_is_corrupt(tmp_path):
    roadmaps_dir = tmp_path / "roadmaps"
    roadmaps_dir.mkdir()
    corrupt_path = roadmaps_dir / "report-20260601T000000.000000Z-99999999-ml.md"
    corrupt_path.write_text("no frontmatter here")

    assert report_state.get_last_report(roadmaps_dir) is None
