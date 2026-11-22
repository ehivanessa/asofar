from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Book(BaseModel):
    """A book from Project Gutenberg, as its header describes it.

    The database adds `id` and `ingested_at` later; they are not part of this model.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    gutenberg_id: int = Field(gt=0)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    language: str = Field(min_length=1)
    published_year: int | None = None


class TextUnit(BaseModel):
    """One paragraph of a book, the unit every position in the project refers to.

    `sequence` is its 0-based place among the book's paragraphs. `char_start` and
    `char_end` are character offsets into the original text, and `char_end` is
    exclusive like a slice, so a paragraph is never empty. `chapter_number` counts
    from 1 and is `None` for text outside any chapter.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    sequence: int = Field(ge=0)
    chapter_number: int | None = Field(default=None, ge=1)
    chapter_title: str | None = None
    content: str = Field(min_length=1)
    char_start: int = Field(ge=0)
    char_end: int = Field(ge=0)

    @model_validator(mode="after")
    def check_char_span(self) -> Self:
        """Reject a span that ends at or before the character where it starts."""
        if self.char_end <= self.char_start:
            raise ValueError("char_end must be greater than char_start")
        return self
