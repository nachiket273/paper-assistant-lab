"""
Unit tests for parser.py
"""

import os
from pathlib import Path
from pydantic import ValidationError
import pytest
import sys

# Finds the absolute path of the directory 2 levels up from this file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.parser import parse_pdf
from src.models.paper import Paper, Page


FIXURE_DIR = Path(__file__).parent / "fixtures"
SAMPLE_PDF_PATH = FIXURE_DIR / "sample.pdf"


def test_parse_pdf_returns_paper_model():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert isinstance(paper, Paper)


def test_filename_matches_input():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert paper.filename == SAMPLE_PDF_PATH.name


def test_num_pages_matches_page_list():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert paper.num_pages == len(paper.pages)


def test_pages_not_empty():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert len(paper.pages) > 0


def test_page_numbers_are_sequential():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    expected = list(range(1, paper.num_pages + 1))
    actual = [page.page_number for page in paper.pages]
    assert actual == expected


def test_page_text_is_string():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert all(isinstance(page.text, str) for page in paper.pages)


def test_metadata_is_present():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert paper.metadata is not None


def test_invalid_pdf_path_raises():
    with pytest.raises(FileNotFoundError):
        parse_pdf("non_existent_file.pdf")


def test_filepath_is_absolute():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert Path(paper.filepath).is_absolute()


def test_page_text_is_not_none():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    assert all(page.text is not None for page in paper.pages)


def test_metadata_fields_are_strings_or_none():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    metadata_fields = [
        paper.metadata.title,
        paper.metadata.author,
        paper.metadata.subject,
        paper.metadata.keywords,
        paper.metadata.creator,
        paper.metadata.producer,
        paper.metadata.creation_date,
        paper.metadata.modification_date
    ]
    assert all(isinstance(field, (str, type(None))) for field in metadata_fields)


def test_page_requires_integer_page_number():
    with pytest.raises(ValidationError):
        Page(page_number="not_an_integer",
             text="Sample text")
