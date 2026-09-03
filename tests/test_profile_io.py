"""Unit tests for profile_io.py."""

from datetime import datetime, timezone

import profile_io
import yaml


# ---------------------------------------------------------------------------
# load_profile
# ---------------------------------------------------------------------------


def test_load_profile_missing_file_returns_none(tmp_path):
    path = tmp_path / "profile.yaml"
    assert profile_io.load_profile(path) is None


def test_load_profile_parses_existing_yaml(tmp_path):
    path = tmp_path / "profile.yaml"
    path.write_text("current_role: Mechanical Engineer\ntarget_role: ML Engineer\n")

    result = profile_io.load_profile(path)

    assert result == {
        "current_role": "Mechanical Engineer",
        "target_role": "ML Engineer",
    }


# ---------------------------------------------------------------------------
# save_profile
# ---------------------------------------------------------------------------


def test_save_profile_writes_yaml_and_stamps_last_updated(tmp_path):
    path = tmp_path / "profile.yaml"
    profile = {"current_role": "Mechanical Engineer", "target_role": "ML Engineer"}

    profile_io.save_profile(path, profile)

    assert path.exists()
    on_disk = yaml.safe_load(path.read_text())
    assert on_disk["current_role"] == "Mechanical Engineer"
    assert on_disk["target_role"] == "ML Engineer"

    today = datetime.now(timezone.utc).date().isoformat()
    assert on_disk["last_updated"] == today


def test_save_profile_does_not_mutate_input_dict(tmp_path):
    path = tmp_path / "profile.yaml"
    profile = {"current_role": "Mechanical Engineer"}

    profile_io.save_profile(path, profile)

    assert "last_updated" not in profile


def test_save_profile_creates_parent_dirs(tmp_path):
    path = tmp_path / "nested" / "dir" / "profile.yaml"
    profile_io.save_profile(path, {"current_role": "X"})
    assert path.exists()


# ---------------------------------------------------------------------------
# merge_profile
# ---------------------------------------------------------------------------


def test_merge_profile_first_run_no_args():
    effective, mode = profile_io.merge_profile(
        None, {"current_state": None, "target_state": None}
    )
    assert mode == "first_run"
    assert effective == {}


def test_merge_profile_first_run_with_args_prefills():
    effective, mode = profile_io.merge_profile(
        None, {"current_state": "Mechanical Engineer", "target_state": "ML Engineer"}
    )
    assert mode == "first_run"
    assert effective == {
        "current_role": "Mechanical Engineer",
        "target_role": "ML Engineer",
    }


def test_merge_profile_override_when_existing_and_args_supplied():
    existing = {
        "current_role": "Mechanical Engineer",
        "target_role": "ML Engineer",
        "weekly_time_budget_hours": 15,
    }
    effective, mode = profile_io.merge_profile(
        existing, {"current_state": None, "target_state": "Staff ML Engineer"}
    )
    assert mode == "override"
    assert effective["target_role"] == "Staff ML Engineer"
    assert effective["current_role"] == "Mechanical Engineer"
    assert effective["weekly_time_budget_hours"] == 15
    # existing dict must not be mutated
    assert existing["target_role"] == "ML Engineer"


def test_merge_profile_as_is_when_existing_and_no_args():
    existing = {"current_role": "Mechanical Engineer", "target_role": "ML Engineer"}
    effective, mode = profile_io.merge_profile(
        existing, {"current_state": None, "target_state": None}
    )
    assert mode == "as_is"
    assert effective == existing
    assert effective is not existing


# ---------------------------------------------------------------------------
# CLI entrypoint (smoke test)
# ---------------------------------------------------------------------------


def test_cli_merge_prints_json(tmp_path, capsys):
    path = tmp_path / "profile.yaml"
    path.write_text("current_role: Mechanical Engineer\ntarget_role: ML Engineer\n")

    exit_code = profile_io.main(
        ["merge", str(path), "--target-state", "Staff ML Engineer"]
    )

    assert exit_code == 0
    out = capsys.readouterr().out
    assert '"mode": "override"' in out
    assert "Staff ML Engineer" in out


# ---------------------------------------------------------------------------
# CLI date serialization regression (C2)
#
# An unquoted `last_updated: 2026-08-19` in YAML parses to a datetime.date,
# which json.dumps cannot serialize by default. The CLI used to crash on the
# very first script call of the documented onboarding flow.
# ---------------------------------------------------------------------------

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_IO_SCRIPT = (
    REPO_ROOT / ".claude" / "skills" / "career-compass" / "scripts" / "profile_io.py"
)
PROFILE_EXAMPLE = REPO_ROOT / "profile.yaml.example"


def test_cli_load_shipped_profile_example_does_not_crash_on_date(capsys):
    exit_code = profile_io.main(["load", str(PROFILE_EXAMPLE)])
    assert exit_code == 0
    out = capsys.readouterr().out
    parsed = json.loads(out)
    assert parsed["last_updated"] == "2026-08-19"


def test_cli_merge_shipped_profile_example_does_not_crash_on_date(capsys):
    exit_code = profile_io.main(
        ["merge", str(PROFILE_EXAMPLE), "--target-state", "Staff ML Engineer"]
    )
    assert exit_code == 0
    parsed = json.loads(capsys.readouterr().out)
    assert parsed["mode"] == "override"
    assert parsed["profile"]["last_updated"] == "2026-08-19"


def test_cli_load_via_subprocess_exits_zero():
    """End-to-end through the real interpreter, matching the documented
    onboarding invocation exactly.
    """
    proc = subprocess.run(
        [sys.executable, str(PROFILE_IO_SCRIPT), "load", str(PROFILE_EXAMPLE)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["current_role"] == "Mechanical Engineer"
