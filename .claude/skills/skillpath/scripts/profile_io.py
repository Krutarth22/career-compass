"""profile_io.py — load/save/merge skillpath's profile.yaml.

Pure-function library first, CLI wrapper second. All I/O (load_profile,
save_profile) is isolated from the merge logic (merge_profile) so the merge
rule documented in reference/profile-schema.md can be unit tested without
touching disk.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def load_profile(path) -> dict | None:
    """Load profile.yaml. Returns None if the file doesn't exist."""
    p = Path(path)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_profile(path, profile: dict) -> None:
    """Write `profile` as YAML, stamping last_updated with today's UTC date."""
    to_write = dict(profile)
    to_write["last_updated"] = datetime.now(timezone.utc).date().isoformat()
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(to_write, f, default_flow_style=False, sort_keys=False)


def merge_profile(existing: dict | None, args: dict) -> tuple[dict, str]:
    """Implement the three-branch argument/profile merge rule.

    See reference/profile-schema.md "Argument / profile merge rule":

    1. No profile.yaml exists -> mode "first_run". Supplied args pre-fill
       the effective profile (current_state -> current_role, target_state
       -> target_role); the caller runs the profile-creation flow and is
       expected to write profile.yaml at the end regardless.
    2. profile.yaml exists and args are supplied -> mode "override". The
       supplied args are applied on top of the saved profile for this run
       only; the caller must not silently rewrite profile.yaml.
    3. profile.yaml exists and no args are supplied -> mode "as_is". The
       saved profile is used unchanged.

    This function performs no I/O — it is pure given the loaded profile and
    parsed CLI args.
    """
    current_state = args.get("current_state")
    target_state = args.get("target_state")
    args_supplied = current_state is not None or target_state is not None

    if existing is None:
        effective: dict = {}
        if current_state is not None:
            effective["current_role"] = current_state
        if target_state is not None:
            effective["target_role"] = target_state
        return effective, "first_run"

    if args_supplied:
        effective = dict(existing)
        if current_state is not None:
            effective["current_role"] = current_state
        if target_state is not None:
            effective["target_role"] = target_state
        return effective, "override"

    return dict(existing), "as_is"


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="skillpath profile I/O utility")
    sub = parser.add_subparsers(dest="command", required=True)

    load_p = sub.add_parser("load", help="Load and print profile.yaml as JSON")
    load_p.add_argument("path")

    merge_p = sub.add_parser(
        "merge", help="Merge an existing profile with CLI-supplied args"
    )
    merge_p.add_argument("path")
    merge_p.add_argument("--current-state", default=None)
    merge_p.add_argument("--target-state", default=None)

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        if ns.command == "load":
            result = load_profile(ns.path)
            print(json.dumps(result))
            return 0
        if ns.command == "merge":
            existing = load_profile(ns.path)
            effective, mode = merge_profile(
                existing,
                {"current_state": ns.current_state, "target_state": ns.target_state},
            )
            print(json.dumps({"profile": effective, "mode": mode}))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
