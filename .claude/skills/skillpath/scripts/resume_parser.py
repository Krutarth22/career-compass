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
import posixpath
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


def _resolve_target(target: str) -> str:
    """Resolve an OPC relationship `Target` to a zip member path.

    Per the OPC spec, a relative target (the common case, e.g.
    `"header1.xml"`, or one with `..` segments) is resolved relative to the
    *source part's* directory -- `word/document.xml` lives in `word/`, so
    `"header1.xml"` -> `"word/header1.xml"`. A target starting with `/` is
    already package-root-relative (e.g. `"/word/header1.xml"`) and is used
    as-is, not joined under `word/` again -- naively prefixing every target
    with `word/` turns that into the nonexistent `word//word/header1.xml`.
    `posixpath.normpath` collapses any `..`/`.` segments in both cases.
    """
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    return posixpath.normpath(posixpath.join("word", target))


def _reference_ids(doc_tree, ref_tag: str) -> list[str]:
    """`r:id` values of every `ref_tag` element (`w:headerReference` /
    `w:footerReference`) in `doc_tree`, in document order."""
    return [
        ref.get(_R_ID_ATTR) for ref in doc_tree.iter(ref_tag) if ref.get(_R_ID_ATTR)
    ]


def _referenced_part_names(
    ref_ids: list[str], rel_info: dict[str, tuple[str, str | None]], zip_names: set[str]
) -> list[str]:
    """Ordered, deduplicated zip member names for `ref_ids`, resolved
    against `rel_info` (`word/_rels/document.xml.rels`'s `{Id: (Target,
    TargetMode)}`, loaded once by the caller and shared across the header
    and footer lookups -- both need the same file).

    A .docx package can retain orphan header/footer parts left over from
    template edits that no relationship or section points at any more --
    globbing `word/header*.xml`/`word/footer*.xml` directly would pull in
    that stale content (or a malformed leftover part) alongside whatever
    the document actually renders. Only parts reachable from the document's
    own relationship graph are real, so an *unreferenced* part is silently
    ignored (the caller never passes its id in `ref_ids`).

    An *active* reference (an id present in `ref_ids`) that fails to
    resolve is a different situation -- it means the package itself is
    broken (the document points at a relationship or part that doesn't
    exist), not that the header/footer is legitimately absent. That must
    raise, not silently fall back to partial body-only text, matching this
    module's documented contract of surfacing a corrupt/malformed file
    rather than guessing.
    """
    names: list[str] = []
    for rid in ref_ids:
        info = rel_info.get(rid)
        if info is None:
            raise ValueError(
                f"document.xml references relationship id {rid!r}, which is "
                "not defined in word/_rels/document.xml.rels (corrupt .docx)"
            )
        target, target_mode = info
        if target_mode == "External":
            # A deliberately external header/footer target -- not a zip
            # part, and not corruption; nothing to extract from it.
            continue
        name = _resolve_target(target)
        if name not in zip_names:
            raise ValueError(
                f"document.xml references {name!r} via relationship "
                f"{rid!r}, but that part is missing from the .docx "
                "(corrupt file)"
            )
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
    missing, corrupt, or non-docx file, and ValueError when an active
    header/footer reference can't be resolved to a real part (see
    `_referenced_part_names`) -- the caller (the model, via the CLI below)
    surfaces those to the user rather than this function guessing.
    """
    with zipfile.ZipFile(path) as zf:
        document_xml = zf.read("word/document.xml")
        doc_tree = ElementTree.fromstring(document_xml)
        header_ids = _reference_ids(doc_tree, _HEADER_REF_TAG)
        footer_ids = _reference_ids(doc_tree, _FOOTER_REF_TAG)

        header_names: list[str] = []
        footer_names: list[str] = []
        if header_ids or footer_ids:
            # Both lookups need the same rels part -- read/parse it once
            # here rather than once per tag.
            try:
                rels_bytes = zf.read("word/_rels/document.xml.rels")
            except KeyError:
                raise ValueError(
                    "document.xml references a header/footer but "
                    "word/_rels/document.xml.rels is missing (corrupt .docx)"
                ) from None
            rels_tree = ElementTree.fromstring(rels_bytes)
            rel_info = {
                rel.get("Id"): (rel.get("Target"), rel.get("TargetMode"))
                for rel in rels_tree.iter(_RELATIONSHIP_TAG)
            }
            zip_names = set(zf.namelist())
            header_names = _referenced_part_names(header_ids, rel_info, zip_names)
            footer_names = _referenced_part_names(footer_ids, rel_info, zip_names)

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
