"""tracker_io.py — append to / read career_compass_tracker.csv.

Pure-function library first, CLI wrapper second.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

COLUMNS = [
    "occurred_at",
    "event_type",
    "item_name",
    "related_skill_ids",
    "report_id",
    "notes",
    "confirmed_for_target_role",
    "confirmed_for_target_level",
]

ALLOWED_EVENT_TYPES = {
    "report_generated",
    "project_started",
    "project_completed",
    "course_started",
    "course_completed",
    "skill_confirmed",
}


def _parse_timestamp(value: str) -> datetime:
    """Parse an ISO 8601 timestamp and normalize it to UTC.

    Naive timestamps are treated as UTC for compatibility with existing
    tracker files.
    """
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def append_row(
    csv_path,
    occurred_at,
    event_type,
    item_name,
    related_skill_ids: list[str],
    report_id,
    notes="",
    confirmed_for_target_role="",
    confirmed_for_target_level="",
) -> None:
    """Append one event row to the tracker CSV, creating it with a header
    row if it doesn't exist yet. Uses the stdlib csv module throughout so
    commas/quotes in free-text fields (e.g. notes) are handled correctly.
    """
    if event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(
            f"invalid event_type {event_type!r}; must be one of {sorted(ALLOWED_EVENT_TYPES)}"
        )

    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    file_needs_header = not path.exists() or path.stat().st_size == 0

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if file_needs_header:
            writer.writerow(COLUMNS)
        writer.writerow(
            [
                occurred_at,
                event_type,
                item_name,
                "|".join(related_skill_ids),
                report_id,
                notes,
                confirmed_for_target_role,
                confirmed_for_target_level,
            ]
        )


def read_rows(
    csv_path,
    since: str | None = None,
    event_types: list[str] | None = None,
) -> list[dict]:
    """Read tracker rows as dicts, filtered by occurred_at >= since and
    event_type in event_types when given.

    Malformed/hand-edited rows are skipped silently rather than raising.
    """
    path = Path(csv_path)
    if not path.exists():
        return []

    since_timestamp = _parse_timestamp(since) if since is not None else None

    rows: list[dict] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            try:
                # csv.DictReader stows any columns beyond COLUMNS under the
                # None key (a ragged/hand-edited row with extra fields) —
                # treat that as malformed too.
                if raw.get(None) is not None:
                    continue
                if any(v is None for v in raw.values()):
                    # Row is short (fewer fields than COLUMNS) — DictReader
                    # fills missing trailing columns with None.
                    continue

                occurred_at = raw["occurred_at"]
                event_type = raw["event_type"]

                if not event_type or event_type not in ALLOWED_EVENT_TYPES:
                    continue

                if not occurred_at:
                    continue
                try:
                    occurred_timestamp = _parse_timestamp(occurred_at)
                except ValueError:
                    continue

                if since_timestamp is not None and occurred_timestamp < since_timestamp:
                    continue
                if event_types is not None and event_type not in event_types:
                    continue

                row = dict(raw)
                skill_ids_raw = row.get("related_skill_ids") or ""
                row["related_skill_ids"] = (
                    skill_ids_raw.split("|") if skill_ids_raw else []
                )
                rows.append(row)
            except Exception:
                # Malformed row (missing/extra columns, bad types, etc.) —
                # skip and continue rather than crashing the caller.
                continue

    return rows


def get_last_report_meta(roadmaps_dir) -> dict | None:
    """Return the newest report's frontmatter, or None if none exist.

    Delegates to report_state.get_last_report() so tracker-focused callers
    don't need to import report_state directly.
    """
    import report_state

    return report_state.get_last_report(roadmaps_dir)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CareerCompass tracker CSV utility")
    sub = parser.add_subparsers(dest="command", required=True)

    append_p = sub.add_parser("append", help="Append one event row")
    append_p.add_argument("csv_path")
    append_p.add_argument("--occurred-at", required=True)
    append_p.add_argument("--event-type", required=True)
    append_p.add_argument("--item-name", required=True)
    append_p.add_argument("--related-skill-ids", default="", help="pipe-separated")
    append_p.add_argument("--report-id", required=True)
    append_p.add_argument("--notes", default="")
    append_p.add_argument("--confirmed-for-target-role", default="")
    append_p.add_argument("--confirmed-for-target-level", default="")

    read_p = sub.add_parser("read", help="Read rows as JSON")
    read_p.add_argument("csv_path")
    read_p.add_argument("--since", default=None)
    read_p.add_argument("--event-types", default=None, help="comma-separated")

    last_p = sub.add_parser(
        "last-report", help="Print the newest report's frontmatter as JSON"
    )
    last_p.add_argument("roadmaps_dir")

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        if ns.command == "append":
            skill_ids = ns.related_skill_ids.split("|") if ns.related_skill_ids else []
            append_row(
                ns.csv_path,
                ns.occurred_at,
                ns.event_type,
                ns.item_name,
                skill_ids,
                ns.report_id,
                notes=ns.notes,
                confirmed_for_target_role=ns.confirmed_for_target_role,
                confirmed_for_target_level=ns.confirmed_for_target_level,
            )
            print(json.dumps({"ok": True}, default=str))
            return 0
        if ns.command == "read":
            event_types = ns.event_types.split(",") if ns.event_types else None
            rows = read_rows(ns.csv_path, since=ns.since, event_types=event_types)
            print(json.dumps(rows, default=str))
            return 0
        if ns.command == "last-report":
            meta = get_last_report_meta(ns.roadmaps_dir)
            print(json.dumps(meta, default=str))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
