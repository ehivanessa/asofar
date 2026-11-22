import pytest
from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails

from asofar.models import Book, TextUnit

GOOD_BOOK: dict[str, object] = {
    "gutenberg_id": 1342,
    "title": "Pride and Prejudice",
    "author": "Austen, Jane",
    "language": "English",
}

GOOD_UNIT: dict[str, object] = {
    "sequence": 0,
    "content": "It was a dark night.",
    "char_start": 0,
    "char_end": 20,
}


def first_error(model: type[BaseModel], data: dict[str, object]) -> ErrorDetails:
    """Validate `data` as `model`, expect it to be rejected, return the first error."""
    with pytest.raises(ValidationError) as excinfo:
        model.model_validate(data)
    return excinfo.value.errors()[0]


def test_good_book_is_accepted() -> None:
    book = Book.model_validate(GOOD_BOOK)
    assert book.title == "Pride and Prejudice"
    assert book.published_year is None


def test_negative_sequence_is_rejected() -> None:
    error = first_error(TextUnit, {**GOOD_UNIT, "sequence": -1})
    assert error["loc"] == ("sequence",)
    assert error["type"] == "greater_than_equal"


def test_text_instead_of_a_number_is_rejected() -> None:
    error = first_error(TextUnit, {**GOOD_UNIT, "sequence": "abc"})
    assert error["loc"] == ("sequence",)
    assert error["type"] == "int_parsing"


def test_end_before_start_is_rejected() -> None:
    error = first_error(TextUnit, {**GOOD_UNIT, "char_start": 5, "char_end": 3})
    assert error["type"] == "value_error"
    assert "char_end must be greater than char_start" in error["msg"]


def test_equal_offsets_are_rejected() -> None:
    error = first_error(TextUnit, {**GOOD_UNIT, "char_start": 5, "char_end": 5})
    assert error["type"] == "value_error"


def test_book_id_zero_is_rejected() -> None:
    error = first_error(Book, {**GOOD_BOOK, "gutenberg_id": 0})
    assert error["loc"] == ("gutenberg_id",)
    assert error["type"] == "greater_than"


def test_unknown_field_is_rejected() -> None:
    error = first_error(Book, {**GOOD_BOOK, "published_yaer": 1813})
    assert error["loc"] == ("published_yaer",)
    assert error["type"] == "extra_forbidden"


def test_models_are_frozen() -> None:
    unit = TextUnit.model_validate(GOOD_UNIT)
    with pytest.raises(ValidationError) as excinfo:
        unit.sequence = 3
    assert excinfo.value.errors()[0]["type"] == "frozen_instance"
