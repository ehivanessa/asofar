from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Book(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    gutenberg_id: int = Field(gt=0)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    language: str = Field(min_length=1)
    published_year: int | None = None


class TextUnit(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    sequence: int = Field(ge=0)
    chapter_number: int | None = Field(default=None, ge=1)
    chapter_title: str | None = None
    content: str = Field(min_length=1)
    char_start: int = Field(ge=0)
    char_end: int = Field(ge=0)

    @model_validator(mode="after")
    def check_char_span(self) -> Self:
        if self.char_end <= self.char_start:
            raise ValueError("char_end must be greater than char_start")
        return self
