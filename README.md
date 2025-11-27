[![FastAPI](https://img.shields.io/badge/FastAPI-0.122.0+-blue?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat&logo=python)](https://www.python.org/)

# Bingo Solver API

Small FastAPI service that solves the **Advent of Code 2021 – Day 4 (Giant Squid)** bingo game.

- Supports:
  - **Part 1** – score of the **first** board to win
  - **Part 2** – score of the **last** board to win
- JSON-only API
- Modules separated to:
  - `engine` – bingo logic
  - `api` – HTTP layer
  - `settings` – configuration

---

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

---

## Installation

```bash
# Clone repo
git clone git@github.com:mlieqo/bingo.git
cd bingo

# Install dependencies
make install
```

---

## Running the API

From the project root:

```bash
make run
```

This starts the server on:

```text
http://127.0.0.1:8000
```

You can also override the settings env variables, e.g.:
```
BINGO_PORT=9000 make run
```
which will run the server on port 9000, instead of the default 8000.

You can then open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc:      http://127.0.0.1:8000/redoc

---

## API

### Endpoint

`POST /api/v1/bingo/solve`


## Example request (curl)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/bingo/solve" \
  -H "Content-Type: application/json" \
  --data-binary @example/payload.json
```
---

## Tests & code quality

### Run tests

```bash
make test
```

### Code quality checks
Runs ruff checks + mypy
```bash
make cq
```
