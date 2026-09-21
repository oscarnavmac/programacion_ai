.PHONY: run test lint format check notebook
run:
	uv run --locked python main.py

test:
	uv run --locked python -m pytest

lint:
	uv run --locked ruff check .

format:
	uv run --locked ruff format .

check: lint
	uv run --locked ruff format --check .
	uv run --locked python -m pytest

notebook:
	uv run --locked jupyter lab
