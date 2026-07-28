"""
parser.py

Utilities for parsing scientific PDF documents using PyMuPDF.

This module is responsible only for extracting document metadata
and page-level raw text.

No cleaning, chunking, or preprocessing is performed here.

NOTE:- Currently limited to extracting text only, images and tables are not supported.
"""

import os
from pathlib import Path
from typing import List, Union

import fitz  # PyMuPDF

import src.models.paper


def parse_pdf(file_path: Union[str, os.PathLike[str]]) -> src.models.paper.Paper:
    """
    Extract metadata and page-level text from a PDF.

    Args:
        file_path (str | Path): Path to the PDF file.

    Returns:
        Paper: A Paper model containing metadata and page-level text.
    """
    # Open the PDF file
    fpath = Path(file_path)

    if not fpath.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    doc = fitz.open(fpath)

    # Extract metadata
    metadata = doc.metadata

    pages: List[src.models.paper.Page] = []

    # Extract page-level text
    for page_idx in range(doc.page_count):
        page = doc.load_page(page_idx)

        pages.append(
            src.models.paper.Page(page_number=page_idx + 1, text=page.get_text("text"))
        )

    result = src.models.paper.Paper(
        filename=fpath.name,
        filepath=str(fpath.resolve()),
        num_pages=doc.page_count,
        metadata=src.models.paper.PaperMetadata(
            title=metadata.get("title"),
            author=metadata.get("author"),
            subject=metadata.get("subject"),
            keywords=metadata.get("keywords"),
            creator=metadata.get("creator"),
            producer=metadata.get("producer"),
            creation_date=metadata.get("creationDate"),
            modification_date=metadata.get("modDate"),
        ),
        pages=pages,
    )

    doc.close()

    return result
