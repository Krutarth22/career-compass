"""Unit tests for resume_parser.py."""

import zipfile

import pytest
import resume_parser


_W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
_R_NS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'

_HEADER_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"
)
_FOOTER_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
)

_PART_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document {w_ns}>
  <w:body>
    {paragraphs}
  </w:body>
</w:document>
"""

_HDR_FTR_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr {w_ns}>
  {paragraphs}
</w:hdr>
"""

_RELS_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {relationships}
</Relationships>
"""


def _make_docx(
    tmp_path,
    body_paragraphs_xml: str,
    parts: dict | None = None,
    references: list | None = None,
    target_overrides: dict | None = None,
):
    """Build a minimal .docx.

    `parts`: {"word/header1.xml": "<w:p>...</w:p>"} -- part files written
    into the zip regardless of whether they're referenced (so a test can
    plant an orphan part, or omit an entry to leave an active reference
    dangling at a missing part).
    `references`: [("rId1", "word/header1.xml", "header"), ...] -- each
    becomes both a relationship in `word/_rels/document.xml.rels` and a
    `w:headerReference`/`w:footerReference` in `document.xml`'s `w:sectPr`,
    i.e. an *actually active* header/footer.
    `target_overrides`: {"rId1": "/word/header1.xml"} -- write this raw OPC
    target string verbatim as that id's Relationship `Target`, instead of
    deriving it from the matching `references` entry's `target`. Lets a
    test exercise `_resolve_target`'s absolute/dot-segment handling without
    a second zip-building helper.
    """
    path = tmp_path / "resume.docx"
    references = references or []
    target_overrides = target_overrides or {}

    ref_tags = []
    rels = []
    for rid, target, kind in references:
        tag = "w:headerReference" if kind == "header" else "w:footerReference"
        ref_tags.append(f'<{tag} w:type="default" r:id="{rid}"/>')
        rel_type = _HEADER_REL_TYPE if kind == "header" else _FOOTER_REL_TYPE
        if rid in target_overrides:
            target_rel = target_overrides[rid]
        else:
            target_rel = target[len("word/") :] if target.startswith("word/") else target
        rels.append(f'<Relationship Id="{rid}" Type="{rel_type}" Target="{target_rel}"/>')

    sect_pr = f"<w:sectPr>{''.join(ref_tags)}</w:sectPr>" if ref_tags else ""
    document_xml = _PART_TEMPLATE.format(
        w_ns=f"{_W_NS} {_R_NS}",
        paragraphs=body_paragraphs_xml + sect_pr,
    )

    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", document_xml)
        if rels:
            zf.writestr(
                "word/_rels/document.xml.rels",
                _RELS_TEMPLATE.format(relationships="\n".join(rels)),
            )
        for name, paragraphs in (parts or {}).items():
            zf.writestr(name, _HDR_FTR_TEMPLATE.format(w_ns=_W_NS, paragraphs=paragraphs))
    return path


def _document_with_header_ref(body: str = "Body") -> str:
    """`document.xml` for a body paragraph plus a single active
    `w:headerReference` (`r:id="rId1"`) -- the shared shape needed by every
    test below that exercises a *resolved* or *broken* header reference,
    independent of how `word/_rels/document.xml.rels` and the header part
    itself are (or aren't) provided."""
    return _PART_TEMPLATE.format(
        w_ns=f"{_W_NS} {_R_NS}",
        paragraphs=f'<w:p><w:r><w:t>{body}</w:t></w:r></w:p>'
        '<w:sectPr><w:headerReference w:type="default" r:id="rId1"/></w:sectPr>',
    )


def test_extract_docx_text_reads_simple_paragraphs(tmp_path):
    path = _make_docx(
        tmp_path,
        """
        <w:p><w:r><w:t>Jane Doe</w:t></w:r></w:p>
        <w:p><w:r><w:t>Software Engineer</w:t></w:r></w:p>
        """,
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Jane Doe\nSoftware Engineer"


def test_extract_docx_text_joins_split_runs(tmp_path):
    path = _make_docx(
        tmp_path,
        """
        <w:p><w:r><w:t>Python, </w:t></w:r><w:r><w:t>SQL, </w:t></w:r><w:r><w:t>AWS</w:t></w:r></w:p>
        """,
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Python, SQL, AWS"


def test_extract_docx_text_skips_blank_paragraphs(tmp_path):
    path = _make_docx(
        tmp_path,
        """
        <w:p><w:r><w:t>Line one</w:t></w:r></w:p>
        <w:p></w:p>
        <w:p><w:r><w:t>Line two</w:t></w:r></w:p>
        """,
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Line one\nLine two"


def test_extract_docx_text_includes_referenced_header_before_body(tmp_path):
    path = _make_docx(
        tmp_path,
        """<w:p><w:r><w:t>Experience section</w:t></w:r></w:p>""",
        parts={
            "word/header1.xml": """<w:p><w:r><w:t>Jane Doe, AI Engineer</w:t></w:r></w:p>""",
        },
        references=[("rId1", "word/header1.xml", "header")],
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Jane Doe, AI Engineer\nExperience section"


def test_extract_docx_text_includes_referenced_footer_after_body(tmp_path):
    path = _make_docx(
        tmp_path,
        """<w:p><w:r><w:t>Experience section</w:t></w:r></w:p>""",
        parts={
            "word/footer1.xml": """<w:p><w:r><w:t>jane@example.com | 555-0100</w:t></w:r></w:p>""",
        },
        references=[("rId1", "word/footer1.xml", "footer")],
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Experience section\njane@example.com | 555-0100"


def test_extract_docx_text_handles_multiple_referenced_headers_and_footers_in_order(
    tmp_path,
):
    path = _make_docx(
        tmp_path,
        """<w:p><w:r><w:t>Body</w:t></w:r></w:p>""",
        parts={
            "word/header2.xml": """<w:p><w:r><w:t>Header two</w:t></w:r></w:p>""",
            "word/header1.xml": """<w:p><w:r><w:t>Header one</w:t></w:r></w:p>""",
            "word/footer1.xml": """<w:p><w:r><w:t>Footer one</w:t></w:r></w:p>""",
            "word/footer2.xml": """<w:p><w:r><w:t>Footer two</w:t></w:r></w:p>""",
        },
        references=[
            ("rId1", "word/header1.xml", "header"),
            ("rId2", "word/header2.xml", "header"),
            ("rId3", "word/footer1.xml", "footer"),
            ("rId4", "word/footer2.xml", "footer"),
        ],
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Header one\nHeader two\nBody\nFooter one\nFooter two"


def test_extract_docx_text_ignores_unreferenced_orphan_parts(tmp_path):
    """A header/footer part with no relationship and no sectPr reference is
    stale template leftover, not active document content -- it must not
    appear in the output, and a malformed orphan part must not break
    parsing of the parts that ARE active."""
    path = _make_docx(
        tmp_path,
        """<w:p><w:r><w:t>Body only</w:t></w:r></w:p>""",
        parts={
            "word/header1.xml": """<w:p><w:r><w:t>Stale unused header</w:t></w:r></w:p>""",
            "word/footer1.xml": "not even valid xml <<<",
        },
        references=[],
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Body only"


def test_extract_docx_text_resolves_package_root_absolute_target(tmp_path):
    path = _make_docx(
        tmp_path,
        "<w:p><w:r><w:t>Body</w:t></w:r></w:p>",
        parts={"word/header1.xml": """<w:p><w:r><w:t>Jane Doe</w:t></w:r></w:p>"""},
        references=[("rId1", "word/header1.xml", "header")],
        target_overrides={"rId1": "/word/header1.xml"},
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Jane Doe\nBody"


def test_extract_docx_text_resolves_dot_segment_relative_target(tmp_path):
    # A target relative to word/document.xml's own directory ("word/") that
    # climbs out and back in -- normalizes to the same word/header1.xml.
    path = _make_docx(
        tmp_path,
        "<w:p><w:r><w:t>Body</w:t></w:r></w:p>",
        parts={"word/header1.xml": """<w:p><w:r><w:t>Jane Doe</w:t></w:r></w:p>"""},
        references=[("rId1", "word/header1.xml", "header")],
        target_overrides={"rId1": "../word/header1.xml"},
    )

    text = resume_parser.extract_docx_text(path)

    assert text == "Jane Doe\nBody"


def test_extract_docx_text_raises_for_reference_to_missing_part(tmp_path):
    """An *active* reference (a real w:headerReference in document.xml)
    pointing at a target that isn't actually in the zip means the package
    itself is broken -- this must raise, not silently fall back to
    partial body-only text."""
    path = _make_docx(
        tmp_path,
        "<w:p><w:r><w:t>Body</w:t></w:r></w:p>",
        references=[("rId1", "word/header1.xml", "header")],
        # note: no `parts` entry -- word/header1.xml is never written
    )

    with pytest.raises(ValueError):
        resume_parser.extract_docx_text(path)


@pytest.mark.parametrize(
    "rels_xml, write_rels_part",
    [
        pytest.param(_RELS_TEMPLATE.format(relationships=""), True, id="no-matching-relationship"),
        pytest.param(None, False, id="rels-file-entirely-missing"),
    ],
)
def test_extract_docx_text_raises_for_unresolvable_reference(tmp_path, rels_xml, write_rels_part):
    """An active reference (`r:id="rId1"` in `document.xml`) with no way to
    resolve it -- whether because no `<Relationship>` defines that id, or
    because `word/_rels/document.xml.rels` isn't in the package at all --
    is package corruption either way and must raise."""
    path = tmp_path / "resume.docx"
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", _document_with_header_ref())
        if write_rels_part:
            zf.writestr("word/_rels/document.xml.rels", rels_xml)

    with pytest.raises(ValueError):
        resume_parser.extract_docx_text(path)


def test_extract_docx_text_skips_external_header_reference(tmp_path):
    """An External-mode relationship target is legitimately not a zip
    part -- valid OPC, not corruption -- and is skipped without error."""
    path = tmp_path / "resume.docx"
    rels_xml = _RELS_TEMPLATE.format(
        relationships=(
            f'<Relationship Id="rId1" Type="{_HEADER_REL_TYPE}" '
            'Target="https://example.com/header.xml" TargetMode="External"/>'
        )
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", _document_with_header_ref())
        zf.writestr("word/_rels/document.xml.rels", rels_xml)

    text = resume_parser.extract_docx_text(path)

    assert text == "Body"


def test_extract_docx_text_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        resume_parser.extract_docx_text(tmp_path / "nope.docx")


def test_extract_docx_text_not_a_zip_raises(tmp_path):
    path = tmp_path / "not-a-docx.docx"
    path.write_text("plain text, not a zip archive")

    with pytest.raises(zipfile.BadZipFile):
        resume_parser.extract_docx_text(path)


def test_main_extract_docx_prints_json(tmp_path, capsys):
    path = _make_docx(
        tmp_path,
        """<w:p><w:r><w:t>Hello resume</w:t></w:r></w:p>""",
    )

    rc = resume_parser.main(["extract-docx", str(path)])

    assert rc == 0
    out = capsys.readouterr().out
    assert '"text": "Hello resume"' in out
