# Asofar

[![CI](https://github.com/ehivanessa/asofar/actions/workflows/ci.yml/badge.svg)](https://github.com/ehivanessa/asofar/actions/workflows/ci.yml)

A reading companion that answers questions about a book using only the portion
you have already read. Register a book, tell it where you are, and ask
anything. It answers with citations to passages you have already seen, and
when the answer lies ahead of your position it says so rather than spoiling it.

**Status:** early development, starting with the text parser.

## The problem

Ask a general-purpose assistant about a book you are halfway through and it can
easily tell you how it ends. Telling it "no spoilers" in the prompt is a
request, not a guarantee.

## Why it exists

Asofar is designed so that the spoiler boundary is a property of the system, not
of the prompt. Every passage carries its position in the book, and retrieval is
filtered by the reader's position in the database query itself, so text beyond
that position never reaches the model. A spoiler leak rate, measured on a
hand-built question set, will be published here.

## Development

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest
```

## Test data

`tests/fixtures/` holds three Project Gutenberg texts, committed unmodified with
their headers and licence: *Pride and Prejudice* (plain chapters), *War and Peace*
(books and chapters) and *A Modest Proposal* (no chapters).

## License

MIT. See [LICENSE](LICENSE).