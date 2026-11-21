from pydantic import BaseModel, ConfigDict, Field


class Book(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    gutenberg_id: int = Field(gt=0)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    language: str = Field(min_length=1)
    published_year: int | None = None
