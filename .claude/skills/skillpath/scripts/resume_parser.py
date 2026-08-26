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
_HEADER_REF_TAG = f"{_WORD_NS}headerReference"
_FOOTER_REF_TAG = f"{_WORD_NS}footerReference"

_REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"
_RELATIONSHIP_TAG = f"{_REL_NS}Relationship"

_R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_R_ID_ATTR = f"{_R_NS}id"


def _referenced_part_names(zf: zipfile.ZipFile, doc_tree, ref_tag: str) -> list[str]:
    """Ordered, deduplicated `word/<target>` names actually referenced by
    `doc_tree` via `ref_tag` (`w:headerReference` / `w:footerReference`),
    resolved through `word/_rels/document.xml.rels`.

    A .docx package can retain orphan header/footer parts left over from
    template edits that no relationship or section points at any more --
    globbing `word/header*.xml`/`word/footer*.xml` directly would pull in
    that stale content (or a malformed leftover part) alongside whatever
    the document actually renders. Only parts reachable from the document's
    own relationship graph are real.
    """
    try:
        rels_tree = ElementTree.fromstring(zf.read("word/_rels/document.xml.rels"))
    except KeyError:
        return []
    rel_targets = {
        rel.get("Id"): rel.get("Target")
        for rel in rels_tree.iter(_RELATIONSHIP_TAG)
    }

    names: list[str] = []
    for ref in doc_tree.iter(ref_tag):
        rid = ref.get(_R_ID_ATTR)
        target = rel_targets.get(rid)
        if not target:
            continue
        name = f"word/{target}" if not target.startswith("word/") else target
        if name not in names:
            names.append(name)
    return names


def _paragraph_lines(xml_bytes: bytes) -> list[str]:
    tree = ElementTree.fromstring(xml_bytes)
    lines: list[str] = []
    for para in tree.iter(_PARA_TAG):
        parts: list[str] = []
        for node in para.iter():
            if node.tag == _TEXT_TAG:
                parts.append(node.text or "")
            elif node.tag in (_BREAK_TAG, _TAB_TAG):
                parts.append(" ")
        line = "".join(parts).strip()
        if line:
            lines.append(line)
    return lines


def extract_docx_text(path) -> str:
    """Return the visible text of a .docx file, one paragraph per line.

    Resume templates commonly place the candidate's name or title in a
    header, or contact details in a footer, rather than in the document
    body. Those live in separate XML parts from `word/document.xml`, but
    which parts are actually active is determined by the document's own
    `w:headerReference`/`w:footerReference` section elements resolved
    through `word/_rels/document.xml.rels` -- not by every `word/header*.xml`
    /`word/footer*.xml` file present in the zip, since orphaned/unreferenced
    parts can remain in a .docx from earlier template edits (see
    `_referenced_part_names`). Header text is emitted first (it visually
    appears at the top of the page), then the body, then footer text; a
    document with no header/footer relationships yields body text only.

    Raises FileNotFoundError / zipfile.BadZipFile / KeyError as-is on a
    missing, corrupt, or non-docx file — the caller (the model, via the CLI
    below) surfaces those to the user rather than this function guessing.
    """
    with zipfile.ZipFile(path) as zf:
        document_xml = zf.read("word/document.xml")
        doc_tree = ElementTree.fromstring(document_xml)
        header_names = _referenced_part_names(zf, doc_tree, _HEADER_REF_TAG)
        footer_names = _referenced_part_names(zf, doc_tree, _FOOTER_REF_TAG)

        lines: list[str] = []
        for name in header_names:
            lines.extend(_paragraph_lines(zf.read(name)))
        lines.extend(_paragraph_lines(document_xml))
        for name in footer_names:
            lines.extend(_paragraph_lines(zf.read(name)))

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
