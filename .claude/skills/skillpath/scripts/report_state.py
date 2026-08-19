"""report_state.py — write/read skillpath roadmap report files.

Reports are Markdown files with a YAML frontmatter block (schema documented
in task-3-brief.md) followed by a human-readable rendered body. Pure-function
library first, CLI wrapper second.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

FRONTMATTER_DELIM = "---"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-")


def _compact_timestamp(generated_at: str) -> str:
    """Convert a full ISO8601 timestamp (with colons/dashes) into the basic
    ISO 8601 form used in report filenames: YYYYMMDDTHHMMSS.ffffffZ.
    """
    normalized = generated_at.replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    return dt.strftime("%Y%m%dT%H%M%S.%f") + "Z"


def write_report(roadmaps_dir, frontmatter: dict, body_markdown: str) -> str:
    """Write a report file and return the full path written.

    Filename: report-<YYYYMMDDTHHMMSS.ffffff>Z-<report_id[:8]>-<target-slug>.md
    """
    roadmaps_path = Path(roadmaps_dir)
    roadmaps_path.mkdir(parents=True, exist_ok=True)

    ts_compact = _compact_timestamp(frontmatter["generated_at"])
    report_id = str(frontmatter["report_id"])
    target_slug = _slugify(str(frontmatter["target_state"]))

    filename = f"report-{ts_compact}-{report_id[:8]}-{target_slug}.md"
    out_path = roadmaps_path / filename

    frontmatter_yaml = yaml.safe_dump(
        frontmatter, default_flow_style=False, sort_keys=False
    )
    content = f"{FRONTMATTER_DELIM}\n{frontmatter_yaml}{FRONTMATTER_DELIM}\n{body_markdown}"
    out_path.write_text(content, encoding="utf-8")

    return str(out_path)


def read_report(path) -> dict:
    """Parse a report file and return its frontmatter dict.

    Raises ValueError if the file has no valid frontmatter block.
    """
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith(FRONTMATTER_DELIM):
        raise ValueError(f"{path}: missing frontmatter block")

    parts = text.split(FRONTMATTER_DELIM, 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: malformed frontmatter block")

    frontmatter = yaml.safe_load(parts[1])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: frontmatter did not parse to a mapping")

    return frontmatter


def _embedded_timestamp(path: Path) -> str:
    """Extract the compact timestamp segment embedded in a report filename,
    e.g. report-20260819T103000.123456Z-ab12cd34-ml-engineer.md ->
    20260819T103000.123456Z
    """
    parts = path.name.split("-", 2)
    return parts[1] if len(parts) > 1 else ""


def get_last_report(roadmaps_dir) -> dict | None:
    """Return the newest report's frontmatter dict (by embedded filename
    timestamp, not filesystem mtime), or None if no report files exist or
    the newest one fails to parse.
    """
    roadmaps_path = Path(roadmaps_dir)
    if not roadmaps_path.exists():
        return None

    report_files = list(roadmaps_path.glob("report-*.md"))
    if not report_files:
        return None

    report_files.sort(key=_embedded_timestamp, reverse=True)
    newest = report_files[0]

    try:
        return read_report(newest)
    except Exception:
        # Corrupt newest report -> degrade to "no diff" gracefully, never crash.
        return None


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="skillpath report state utility")
    sub = parser.add_subparsers(dest="command", required=True)

    read_p = sub.add_parser("read", help="Print a report's frontmatter as JSON")
    read_p.add_argument("path")

    last_p = sub.add_parser(
        "last", help="Print the newest report's frontmatter as JSON"
    )
    last_p.add_argument("roadmaps_dir")

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        if ns.command == "read":
            print(json.dumps(read_report(ns.path), default=str))
            return 0
        if ns.command == "last":
            print(json.dumps(get_last_report(ns.roadmaps_dir), default=str))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
