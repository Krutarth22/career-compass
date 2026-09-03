"""markdown_docx.py — render a bounded Markdown subset into a python-docx
Document.

Scope is deliberately limited to what skillpath's report bodies actually
use (see reference/report-format.md's "Style notes"): `#`-`####` headers,
paragraphs with inline **bold** / *italic* / `code` spans and [text](url)
links, `-`/`*`/`1.` list items, and pipe tables. Anything else is dropped
rather than raising, so an unrecognized construct never blocks a report
from being written.
"""

from __future__ import annotations

import re

from docx import Document
from docx.oxml.ns import qn
from docx.oxml.shared import OxmlElement
from docx.shared import RGBColor

_HEADER_RE = re.compile(r"^(#{1,4})\s+(.*)$")
_UL_RE = re.compile(r"^[-*]\s+(.*)$")
_OL_RE = re.compile(r"^\d+\.\s+(.*)$")
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
_TABLE_SEP_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")

_INLINE_RE = re.compile(
    r"(\*\*.+?\*\*|\*.+?\*|`.+?`|\[.+?\]\(\S+?\))"
)

_LINK_COLOR = RGBColor(0x05, 0x63, 0xC1)


def _add_hyperlink(paragraph, text: str, url: str) -> None:
    """Add a real, clickable hyperlink run to `paragraph`."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")

    color = OxmlElement("w:color")
    color.set(qn("w:val"), str(_LINK_COLOR))
    rpr.append(color)

    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.append(underline)

    run.append(rpr)
    text_el = OxmlElement("w:t")
    text_el.text = text
    run.append(text_el)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def _add_inline_runs(paragraph, text: str) -> None:
    """Split `text` on inline markdown spans and add formatted runs."""
    pos = 0
    for match in _INLINE_RE.finditer(text):
        if match.start() > pos:
            paragraph.add_run(text[pos : match.start()])
        token = match.group(0)
        if token.startswith("**"):
            paragraph.add_run(token[2:-2]).bold = True
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            run.font.name = "Courier New"
        elif token.startswith("["):
            link_text, url = re.match(r"\[(.+?)\]\((\S+?)\)", token).groups()
            _add_hyperlink(paragraph, link_text, url)
        elif token.startswith("*"):
            paragraph.add_run(token[1:-1]).italic = True
        pos = match.end()
    if pos < len(text):
        paragraph.add_run(text[pos:])


def _flush_table(doc, rows: list[list[str]]) -> None:
    if not rows:
        return
    n_cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=n_cols)
    try:
        table.style = "Light Grid Accent 1"
    except KeyError:
        pass
    for r_idx, row in enumerate(rows):
        for c_idx in range(n_cols):
            cell_text = row[c_idx] if c_idx < len(row) else ""
            cell_para = table.cell(r_idx, c_idx).paragraphs[0]
            _add_inline_runs(cell_para, cell_text)
            if r_idx == 0:
                for run in cell_para.runs:
                    run.bold = True


def render_markdown_to_docx(markdown_text: str, doc: Document | None = None) -> Document:
    """Render `markdown_text` into `doc` (or a new Document if omitted)."""
    if doc is None:
        doc = Document()

    lines = markdown_text.splitlines()
    i = 0
    paragraph_buffer: list[str] = []
    table_buffer: list[list[str]] = []

    def flush_paragraph():
        if paragraph_buffer:
            para = doc.add_paragraph()
            _add_inline_runs(para, " ".join(paragraph_buffer))
            paragraph_buffer.clear()

    def flush_table():
        if table_buffer:
            _flush_table(doc, table_buffer.copy())
            table_buffer.clear()

    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            flush_paragraph()
            flush_table()
            i += 1
            continue

        header_match = _HEADER_RE.match(line)
        if header_match:
            flush_paragraph()
            flush_table()
            level = len(header_match.group(1))
            doc.add_heading(header_match.group(2).strip(), level=level)
            i += 1
            continue

        table_row_match = _TABLE_ROW_RE.match(line)
        if table_row_match:
            flush_paragraph()
            cells = [c.strip() for c in table_row_match.group(1).split("|")]
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if not table_buffer and _TABLE_SEP_RE.match(next_line):
                table_buffer.append(cells)
                i += 2
                continue
            if table_buffer:
                table_buffer.append(cells)
                i += 1
                continue

        flush_table()

        ul_match = _UL_RE.match(line)
        if ul_match:
            flush_paragraph()
            para = doc.add_paragraph(style="List Bullet")
            _add_inline_runs(para, ul_match.group(1))
            i += 1
            continue

        ol_match = _OL_RE.match(line)
        if ol_match:
            flush_paragraph()
            para = doc.add_paragraph(style="List Number")
            _add_inline_runs(para, ol_match.group(1))
            i += 1
            continue

        if re.match(r"^-{3,}$", line.strip()):
            flush_paragraph()
            i += 1
            continue

        paragraph_buffer.append(line.strip())
        i += 1

    flush_paragraph()
    flush_table()

    return doc
