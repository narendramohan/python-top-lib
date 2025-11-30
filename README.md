# Enterprise Data Platform

This project provides a complete data engineering template designed for production‑grade data operations.  It includes a FastAPI API, Typer CLI, Polars ETL pipeline, DuckDB analytics engine, Textual dashboard, and a browser‑based Pyodide app.  Additional integrations for AWS S3 and Snowflake allow you to ingest files from object storage and load processed data into your cloud warehouse.

## Features

- **FastAPI** backend exposing validation and health endpoints.
- **Typer** CLI for running ETL jobs, data quality checks and analytics queries.
- **Polars** for high‑performance data transformations.
- **DuckDB** as an embedded OLAP engine for SQL analytics.
- **Loguru** and **Rich** for structured, colourized logging.
- **Textual** to build a terminal dashboard.
- **Pyodide** for client‑side Python in the browser.
- **AWS S3 integration** for downloading raw data files.
- **Snowflake integration** for loading processed Parquet data into your warehouse.
- Dockerfile, docker‑compose and Makefile for local development and deployment.

## Getting started

### Prerequisites

Install [uv](https://github.com/astral-sh/uv) - the fast Python package manager:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation & Setup

1. Install dependencies and create virtual environment:

```sh
make install
# or: uv sync
```

2. Copy `.env.example` to `.env` and fill out your configuration.  You need AWS credentials (access key, secret key, region) and Snowflake credentials (account, user, password, role, warehouse, database, schema).

3. Run the API:

```sh
make run-api
```

4. Use the CLI:

```sh
make run-cli
# available commands: etl, dq, analytics, s3-download, snowflake-load
```

5. Run the dashboard:

```sh
make run-dashboard
```

6. Start the browser app (Pyodide) by opening `src/browser/index.html` in a browser.

### Development

Run linting, formatting, and type checking:

```sh
make lint       # Run ruff linter
make format     # Format with black
make type-check # Run mypy type checker
make test       # Run pytest
```

## AWS S3 integration

The `src/etl/s3.py` module provides functions to download files from S3 using `boto3`.  Use the CLI command `s3-download` to pull a CSV from your configured bucket into the local `data/raw` directory.  Credentials and bucket configuration are read from the `Settings` class in `src/core/config.py`.

## Snowflake integration

The `src/etl/snowflake.py` module implements a simple loader that writes a Parquet file into a Snowflake table using the Python connector's `PUT` and `COPY INTO` commands.  Use the CLI command `snowflake-load` to upload a processed Parquet file into Snowflake.  Connection parameters are configured via the `.env` file.
