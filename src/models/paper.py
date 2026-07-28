"""
Pydantic model representing the output of the paper ingestion process.
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Page(BaseModel):
    """
    Represents a single page of a PDF document.
    """

    page_number: int
    text: str


class PaperMetadata(BaseModel):
    """
    Represents the metadata of a PDF document.
    """

    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None


class Paper(BaseModel):
    """
    Represents a PDF document with its metadata and page-level text.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    filename: str
    filepath: str

    num_pages: int

    metadata: PaperMetadata
    pages: List[Page]
