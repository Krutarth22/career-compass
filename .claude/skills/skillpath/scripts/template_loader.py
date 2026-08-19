"""template_loader.py — shared helper for loading project template `.md`
files (frontmatter + `##` body sections).

Pure-function library; no CLI. Used by lint_templates.py (Task 5) and
Task 6's template-selection logic.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n?(.*)\Z", flags=re.DOTALL)
_SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", flags=re.MULTILINE)


def load_template(path) -> dict:
    """Parse a template `.md` file's YAML frontmatter (between `---`
    delimiters) plus its body `##` sections.

    Returns {"frontmatter": {...}, "sections": {heading: body_text, ...}}.
    `frontmatter` is {} if no frontmatter block is found or it's empty.
    `sections` maps each `##` heading's text to the raw text following it,
    up to (but not including) the next `##` heading.
    """
    p = Path(path)
    text = p.read_text(encoding="utf-8")

    match = _FRONTMATTER_RE.match(text)
    if match:
        raw_frontmatter, body = match.group(1), match.group(2)
        frontmatter = yaml.safe_load(raw_frontmatter) or {}
    else:
        frontmatter = {}
        body = text

    sections: dict[str, str] = {}
    headings = list(_SECTION_HEADING_RE.finditer(body))
    for i, heading_match in enumerate(headings):
        heading = heading_match.group(1).strip()
        start = heading_match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
        sections[heading] = body[start:end].strip()

    return {"frontmatter": frontmatter, "sections": sections}


def load_track(track_dir) -> list[dict]:
    """Load every `*.md` file in a track directory except `TEMPLATE.md`.

    Returns a list of load_template results, each annotated with
    `_filename` (basename, e.g. "01-rag-pipeline.md") for downstream
    reference (e.g. resolving project_prerequisites entries).
    """
    d = Path(track_dir)
    results = []
    for md_path in sorted(d.glob("*.md")):
        if md_path.name == "TEMPLATE.md":
            continue
        loaded = load_template(md_path)
        loaded["_filename"] = md_path.name
        results.append(loaded)
    return results
