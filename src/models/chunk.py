"""
Pydantic model representing the output of chunking process.
"""

from pydantic import BaseModel, Field


class PageSpan(BaseModel):
    page_number: int = Field(..., ge=1)
    start_index: int = Field(..., ge=0)
    end_index: int = Field(..., ge=0)


class Chunk(BaseModel):
    chunk_id: str = Field(..., description="Unique identifier for the chunk")
    text: str
    page_spans: list[PageSpan] = Field(
        default_factory=list, description="List of page spans associated with the chunk"
    )


class ChunkCollection(BaseModel):
    chunks: list[Chunk] = Field(default_factory=list)

    def __len__(self) -> int:
        return len(self.chunks)

    def __iter__(self):
        return iter(self.chunks)
