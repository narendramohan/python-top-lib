install:
	uv sync

run-api:
	uv run -m uvicorn src.api.main:app --reload

run-cli:
	uv run -m src.cli.app

run-dashboard:
	uv run -m src.ui.dashboard

test:
	uv run pytest -q

lint:
	uv run ruff check .

format:
	uv run black .

type-check:
	uv run mypy src