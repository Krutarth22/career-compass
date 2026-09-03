"""report_state.py — write/read skillpath roadmap report files.

Reports are Word documents (`.docx`), rendered from a Markdown body via
`markdown_docx.py`. The YAML frontmatter (schema documented in
task-3-brief.md) that used to sit atop the Markdown file can't live inside
a `.docx` the same way, so it's written to a `.meta.yaml` sidecar file next
to the `.docx`, sharing the same base filename. Pure-function library
first, CLI wrapper second.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

from markdown_docx import render_markdown_to_docx

META_SUFFIX = ".meta.yaml"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-")


_FILENAME_RE = re.compile(
    r"^report-(?P<ts>.+)-(?P<id8>[0-9a-fA-F]{8})-(?P<slug>.+)\.docx$"
)


def _readable_timestamp(generated_at: str) -> str:
    """Convert a full ISO8601 timestamp into a human-readable, sortable
    form used in report filenames: YYYY-MM-DD_HH-MM-SS (local seconds
    resolution -- the report_id[:8] alongside it in the filename already
    guarantees uniqueness, so sub-second precision isn't needed).
    """
    normalized = generated_at.replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def _meta_path_for(docx_path: Path) -> Path:
    """report-<ts>-<id8>-<slug>.docx -> report-<ts>-<id8>-<slug>.meta.yaml"""
    return docx_path.with_name(docx_path.stem + META_SUFFIX)


def write_report(roadmaps_dir, frontmatter: dict, body_markdown: str) -> str:
    """Render a Word (.docx) report and write its frontmatter to a sidecar
    `.meta.yaml` file next to it. Returns the full path to the `.docx`.

    Filenames: report-<YYYY-MM-DD_HH-MM-SS>-<report_id[:8]>-<target-slug>.docx
    and the same base name with `.meta.yaml`.
    """
    roadmaps_path = Path(roadmaps_dir)
    roadmaps_path.mkdir(parents=True, exist_ok=True)

    ts_readable = _readable_timestamp(frontmatter["generated_at"])
    report_id = str(frontmatter["report_id"])
    target_slug = _slugify(str(frontmatter["target_state"]))

    filename = f"report-{ts_readable}-{report_id[:8]}-{target_slug}.docx"
    out_path = roadmaps_path / filename

    doc = render_markdown_to_docx(body_markdown)
    doc.save(str(out_path))

    meta_path = _meta_path_for(out_path)
    meta_yaml = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)
    meta_path.write_text(meta_yaml, encoding="utf-8")

    return str(out_path)


def read_report(path) -> dict:
    """Read a report's `.docx` path and return its sidecar frontmatter dict.

    Raises ValueError if the sidecar `.meta.yaml` file is missing or
    doesn't parse to a mapping.
    """
    docx_path = Path(path)
    meta_path = _meta_path_for(docx_path)
    if not meta_path.exists():
        raise ValueError(f"{path}: missing sidecar metadata file {meta_path.name}")

    frontmatter = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: sidecar metadata did not parse to a mapping")

    return frontmatter


def _embedded_timestamp(path: Path) -> str:
    """Extract the timestamp segment embedded in a report filename, e.g.
    report-2026-08-19_10-30-00-ab12cd34-ml-engineer.docx ->
    2026-08-19_10-30-00. The timestamp itself contains dashes, so this
    anchors on the trailing `-<8-hex-char report_id>-<slug>.docx` instead
    of naively splitting on "-".
    """
    match = _FILENAME_RE.match(path.name)
    return match.group("ts") if match else ""


def get_last_report(roadmaps_dir) -> dict | None:
    """Return the newest report's frontmatter dict (by embedded filename
    timestamp, not filesystem mtime), or None if no report files exist or
    the newest one fails to parse.
    """
    roadmaps_path = Path(roadmaps_dir)
    if not roadmaps_path.exists():
        return None

    report_files = list(roadmaps_path.glob("report-*.docx"))
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
