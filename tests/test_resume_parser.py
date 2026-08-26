"""Unit tests for resume_parser.py."""

import zipfile

import pytest
import resume_parser


_DOCUMENT_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {paragraphs}
  </w:body>
</w:document>
"""


def _make_docx(tmp_path, paragraphs_xml: str):
    path = tmp_path / "resume.docx"
    document_xml = _DOCUMENT_XML_TEMPLATE.format(paragraphs=paragraphs_xml)
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", document_xml)
    return path


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
