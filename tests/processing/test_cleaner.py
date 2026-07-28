from pathlib import Path

from src.ingestion.parser import parse_pdf
from src.models.paper import Page, Paper, PaperMetadata
from src.processing.cleaner import clean_page, clean_paper, normalize_whitespace

FIXURE_DIR = Path(__file__).parent.parent / "fixtures"
SAMPLE_PDF_PATH = FIXURE_DIR / "sample.pdf"


def test_clean_text_remains_intact():
    text = "This is a test."
    expected = "This is a test."
    assert normalize_whitespace(text) == expected


def test_multiple_spaces_are_collapsed():
    text = "This  is   a    test."
    expected = "This is a test."
    assert normalize_whitespace(text) == expected


def test_leading_whitespace_is_removed():
    text = "   This is a test."
    expected = "This is a test."
    assert normalize_whitespace(text) == expected


def test_trailing_whitespace_is_removed():
    text = "This is a test.   "
    expected = "This is a test."
    assert normalize_whitespace(text) == expected


def test_multiple_blank_lines_are_collapsed():
    text = "This is a test.\n\n\n\nThis is another test."
    expected = "This is a test.\n\nThis is another test."
    assert normalize_whitespace(text) == expected


def test_multiple_tabs_are_collapsed():
    text = "This\tis\ta\ttest."
    expected = "This is a test."
    assert normalize_whitespace(text) == expected


def test_mixed_whitespace_is_collapsed():
    text = "This  is\t a   test.\n\n\nThis is another test."
    expected = "This is a test.\n\nThis is another test."
    assert normalize_whitespace(text) == expected


def test_carriage_returns_are_normalized():
    text = "This is a test.\r\nThis is another test.\rThis is yet another test."
    expected = "This is a test.\nThis is another test.\nThis is yet another test."
    assert normalize_whitespace(text) == expected


def test_multiple_blank_lines_at_start_and_end_are_removed():
    text = "\n\n\nThis is a test.\n\n\n"
    expected = "This is a test."
    assert normalize_whitespace(text) == expected


def test_empty_string_remains_empty():
    text = ""
    expected = ""
    assert normalize_whitespace(text) == expected


def test_string_with_only_whitespace_becomes_empty():
    text = "   \t   \n\n   "
    expected = ""
    assert normalize_whitespace(text) == expected


def test_string_with_only_blank_lines_becomes_empty():
    text = "\n\n\n"
    expected = ""
    assert normalize_whitespace(text) == expected


def test_string_with_only_tabs_and_spaces_becomes_empty():
    text = "   \t   "
    expected = ""
    assert normalize_whitespace(text) == expected


def test_string_with_only_carriage_returns_becomes_empty():
    text = "\r\r\r"
    expected = ""
    assert normalize_whitespace(text) == expected


def test_citation_like_text_is_preserved():
    text = "This is a test. (Smith et al., 2020)"
    expected = "This is a test. (Smith et al., 2020)"
    assert normalize_whitespace(text) == expected


def test_greek_letters_are_preserved():
    text = "This is a test with Greek letters: α, β, γ."
    expected = "This is a test with Greek letters: α, β, γ."
    assert normalize_whitespace(text) == expected


def test_special_characters_are_preserved():
    text = "This is a test with special characters: !@#$%^&*()_+-=[]{}|;':\",.<>/?"
    expected = "This is a test with special characters: !@#$%^&*()_+-=[]{}|;':\",.<>/?"
    assert normalize_whitespace(text) == expected


def test_unicode_characters_are_preserved():
    text = "This is a test with unicode characters: ü, ñ, ö, 漢字."
    expected = "This is a test with unicode characters: ü, ñ, ö, 漢字."
    assert normalize_whitespace(text) == expected


def test_equations_are_preserved():
    text = "This is a test with an equation: E = mc^2."
    expected = "This is a test with an equation: E = mc^2."
    assert normalize_whitespace(text) == expected


def test_page_cleaning():
    page = Page(
        page_number=1, text="This  is   a    test.\n\n\n\nThis is another test."
    )
    cleaned_page = clean_page(page)
    expected_text = "This is a test.\n\nThis is another test."
    assert cleaned_page.text == expected_text


def test_paper_cleaning():
    paper = Paper(
        filename="test.pdf",
        filepath="/path/to/test.pdf",
        num_pages=2,
        metadata=PaperMetadata(),
        pages=[
            Page(
                page_number=1, text="This  is   a    test.\n\n\n\nThis is another test."
            ),
            Page(page_number=2, text="   This is a test.\n\n\n"),
        ],
    )
    cleaned_paper = clean_paper(paper)
    expected_pages = [
        Page(page_number=1, text="This is a test.\n\nThis is another test."),
        Page(page_number=2, text="This is a test."),
    ]

    assert cleaned_paper.filename == paper.filename
    assert cleaned_paper.filepath == paper.filepath
    assert cleaned_paper.num_pages == paper.num_pages
    assert cleaned_paper.metadata == paper.metadata
    assert cleaned_paper.pages == expected_pages


def test_cleaned_paper_remains_unchanged():
    paper = Paper(
        filename="test.pdf",
        filepath="/path/to/test.pdf",
        num_pages=2,
        metadata=PaperMetadata(),
        pages=[
            Page(page_number=1, text="This is a test."),
            Page(page_number=2, text="This is another test."),
        ],
    )
    cleaned_paper = clean_paper(paper)

    assert cleaned_paper == paper


def test_clean_paper_integration():
    paper = parse_pdf(SAMPLE_PDF_PATH)
    cleaned_paper = clean_paper(paper)
    assert cleaned_paper.num_pages == paper.num_pages
