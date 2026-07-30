""" "
Text chunking utilities.

The chunker splits the text of a paper into smaller, manageable pieces (chunks) for
further processing.

"""

from typing import List, Tuple

from src.models.paper import Paper
from src.processing.helper import PageIndex


def flatten_paper(paper: Paper) -> Tuple[str, List[PageIndex]]:
    """
    Flatten a Paper into one continuous string while preserving
    the global character offsets of each page.

    Args:
        paper(Paper): Paper to be flattened.

    Returns:
        Tuple[str, List[PageIndex]]

            flattened_text:
                Complete paper text as a continuous string

            page_index:
                Mapping from page numbers to character offsets
                in the flattened text.
    """
    flattened_pages: list[str] = []
    page_indices: list[PageIndex] = []

    current_offset = 0

    for page in paper.pages:
        flattened_pages.append(page.text)

        page_indices.append(
            PageIndex(page.page_number, current_offset, current_offset + len(page.text))
        )

        current_offset = current_offset + len(page.text)

    flattened_text = "".join(flattened_pages)
    return flattened_text, page_indices
