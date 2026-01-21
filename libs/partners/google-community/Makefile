.PHONY: all lint format test test_watch

all: lint test

lint:
	uv run --group lint ruff check .
	uv run --group typing mypy .

format:
	uv run ruff format .

test:
	uv run --group test pytest tests/unit_tests

test_watch:
	uv run pytest-watcher tests/unit_tests
