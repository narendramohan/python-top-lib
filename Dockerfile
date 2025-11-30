FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and sync dependencies
COPY pyproject.toml .
RUN uv sync --frozen

# Copy application code
COPY . .

CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]