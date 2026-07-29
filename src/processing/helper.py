"""
Internal Helper dataclasses
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PageIndex:
    page_number: int
    global_start_idx: int
    global_end_idx: int


@dataclass(frozen=True)
class Window:
    start: int
    end: int
