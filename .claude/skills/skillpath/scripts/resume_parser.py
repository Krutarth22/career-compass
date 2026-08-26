"""resume_parser.py — extract plain text from a .docx resume.

Stdlib-only (zipfile + xml.etree): a .docx is a zip archive containing
`word/document.xml`, whose text runs (`<w:t>` elements) hold the visible
text. No third-party dependency (e.g. python-docx) is required or should be
added — this keeps resume parsing working on a bare Python install.

PDF resumes need no script: Claude Code's own Read tool already extracts
text/visual content from PDF files directly. Pasted resume text needs no
script either. This module exists solely for the DOCX case.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from xml.etree import ElementTree

_WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_TEXT_TAG = f"{_WORD_NS}t"
_PARA_TAG = f"{_WORD_NS}p"
_BREAK_TAG = f"{_WORD_NS}br"
_TAB_TAG = f"{_WORD_NS}tab"


def extract_docx_text(path) -> str:
    """Return the visible text of a .docx file, one paragraph per line.

    Raises FileNotFoundError / zipfile.BadZipFile / KeyError as-is on a
    missing, corrupt, or non-docx file — the caller (the model, via the CLI
    below) surfaces those to the user rather than this function guessing.
    """
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as f:
            tree = ElementTree.parse(f)

    lines: list[str] = []
    for para in tree.getroot().iter(_PARA_TAG):
        parts: list[str] = []
        for node in para.iter():
            if node.tag == _TEXT_TAG:
                parts.append(node.text or "")
            elif node.tag in (_BREAK_TAG, _TAB_TAG):
                parts.append(" ")
        line = "".join(parts).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="skillpath resume parsing utility")
    sub = parser.add_subparsers(dest="command", required=True)

    extract_p = sub.add_parser(
        "extract-docx", help="Extract plain text from a .docx resume"
    )
    extract_p.add_argument("path")

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    ns = parser.parse_args(argv)

    try:
        if ns.command == "extract-docx":
            text = extract_docx_text(ns.path)
            print(json.dumps({"text": text}))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
