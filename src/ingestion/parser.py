"""
parser.py

Utilities for parsing scientific PDF documents using PyMuPDF.

This module is responsible only for extracting document metadata
and page-level raw text.

No cleaning, chunking, or preprocessing is performed here.

NOTE:- Currently limited to extracting text only, images and tables are not supported.
"""
import fitz  # PyMuPDF
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Union

# Finds the absolute path of the directory 2 levels up from this file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models.paper import (
    Page,
    PaperMetadata,
    Paper
)

def parse_pdf(file_path: Union[str, os.PathLike[str]]) -> Paper:
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

    pages : List[Page] = []

    # Extract page-level text
    for page_idx in range(doc.page_count):
        page = doc.load_page(page_idx)

        pages.append(
            Page(
                page_number=page_idx + 1,
                text=page.get_text("text")
            )
        )

    result = Paper(
        filename=fpath.name,
        filepath=str(fpath.resolve()),
        num_pages=doc.page_count,
        metadata=PaperMetadata(
            title=metadata.get("title"),
            author=metadata.get("author"),
            subject=metadata.get("subject"),
            keywords=metadata.get("keywords"),
            creator=metadata.get("creator"),
            producer=metadata.get("producer"),
            creation_date=metadata.get("creationDate"),
            modification_date=metadata.get("modDate"),
        ),
        pages=pages
    )

    doc.close()

    return result
