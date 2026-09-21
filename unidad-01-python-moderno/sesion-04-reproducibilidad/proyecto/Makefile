.PHONY: check lint format-check format test run sync

check: lint format-check test

lint:
	uv run --locked ruff check .

format-check:
	uv run --locked ruff format --check .

format:
	uv run --locked ruff format .

test:
	uv run --locked python -m pytest

run:
	uv run --locked python main.py data/readings.jsonl

sync:
	uv sync --locked
