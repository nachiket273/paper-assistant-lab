"""
Text cleaning utilities.

The cleaner performs lightweight normalization while preserving
scientific content.

No tokenization or semantic processing is performed here.
"""

import re

from src.models.paper import Page, Paper

_MULTIPLE_WHITESPACE_RE = re.compile(r"[ \t]+")
_MULTIPLE_BLANK_LINES_RE = re.compile(r"\n{3,}")


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in the text while preserving paragraph breaks.

    Args:
        text (str): The input text to normalize.

    Returns:
        str: The normalized text.
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Replace multiple spaces and tabs with a single space
    text = _MULTIPLE_WHITESPACE_RE.sub(" ", text)

    # Reduce multiple blank lines to a maximum of two
    text = _MULTIPLE_BLANK_LINES_RE.sub("\n\n", text)

    return text.strip()


def clean_page(page: Page) -> Page:
    """
    Clean the text of a single page.

    Args:
        page (Page): The Page object to clean.

    Returns:
        Page: A new Page object with cleaned text.
    """
    cleaned_text = normalize_whitespace(page.text)
    return Page(page_number=page.page_number, text=cleaned_text)


def clean_paper(paper: Paper) -> Paper:
    """
    Clean the text of an entire paper.

    Args:
        paper (Paper): The Paper object to clean.

    Returns:
        Paper: A new Paper object with cleaned pages.
    """
    return paper.model_copy(
        update={"pages": [clean_page(page) for page in paper.pages]}
    )
