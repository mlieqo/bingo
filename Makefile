.PHONY: cq test format run install

cq:
	poetry run ruff check .
	poetry run mypy .

test:
	poetry run pytest

format:
	poetry run ruff check --select I --fix .
	poetry run ruff format .

run:
	poetry run python -m bingo.run

install:
	poetry install
