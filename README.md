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


Test Suite Summary (17 Tests Total)
test_api.py (7 tests) 🔗
Tests for FastAPI endpoints and Pydantic models:

✅ test_health_endpoint - Health check endpoint
✅ test_record_model_valid - Valid Record model creation
✅ test_record_model_invalid_id - ID validation (must be > 0)
✅ test_record_model_invalid_age - Age validation (0 < age < 120)
✅ test_record_model_invalid_email - Email format validation
✅ test_validate_endpoint_valid_csv - CSV validation with valid data
✅ test_validate_endpoint_invalid_csv - CSV validation error handling
test_dq.py (5 tests) ✨
Tests for data quality rules and checks:

✅ test_email_not_null_rule - Null email detection
✅ test_age_valid_rule - Age range validation (0 < age < 120)
✅ test_age_valid_boundary - Boundary conditions
✅ test_rules_dictionary - Rule registry validation
✅ test_rules_applied_to_dataset - Complete rule application workflow
test_etl.py (5 tests) 🔄
Tests for ETL transformation functions:

✅ test_filter_adults_basic - Basic adult filtering (age > 18)
✅ test_filter_adults_all_adults - All rows are adults
✅ test_filter_adults_no_adults - No rows are adults
✅ test_filter_adults_edge_case_18 - Boundary condition at age 18
✅ test_filter_adults_preserves_columns - Column preservation
Key Changes
✅ Added httpx>=0.24.0 to dev dependencies for FastAPI TestClient
✅ All tests follow best practices with clear docstrings
✅ Edge cases and boundary conditions covered
✅ Comprehensive error handling tests
✅ 100% pass rate: 17/17 tests passing