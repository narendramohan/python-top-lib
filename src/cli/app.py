"""Command line interface for the data platform using Typer."""

import typer
from etl.runner import run_etl
from analytics.query import run_query
from dq.checks import run_dq
from etl.s3 import download_from_s3
from etl.snowflake import load_parquet_to_snowflake
from etl.load import load_parquet
from etl.extract import extract_local
from etl.transform import filter_adults
from core.logger import get_logger

app = typer.Typer(help="Data platform command line interface.")
logger = get_logger()


@app.command()
def etl(source: str = typer.Option("input.csv", help="Name of the input CSV file in raw directory"),
        output: str = typer.Option("output.parquet", help="Name of the output Parquet file in processed directory")) -> None:
    """Run the ETL pipeline: extract, transform and load.

    Reads from raw CSV, filters adults, and writes to Parquet. Does not load to Snowflake by default.
    """
    logger.info("Starting CLI ETL")
    df = extract_local(source)
    df_t = filter_adults(df)
    load_parquet(df_t, output)
    logger.info("ETL finished")


@app.command()
def dq() -> None:
    """Run data quality checks on the input CSV."""
    run_dq()


@app.command()
def analytics(sql: str = typer.Argument(..., help="SQL query to run using DuckDB")) -> None:
    """Run an ad‑hoc analytics SQL query using DuckDB."""
    run_query(sql)


@app.command()
def s3_download(key: str = typer.Argument(..., help="S3 object key to download")) -> None:
    """Download a file from the configured S3 bucket into the raw directory."""
    local_path = download_from_s3(key)
    print(f"Downloaded to {local_path}")


@app.command()
def snowflake_load(parquet_file: str = typer.Argument(..., help="Name of the Parquet file in processed directory"),
                   table: str = typer.Argument(..., help="Target Snowflake table (schema.table)")
                  ) -> None:
    """Load a local Parquet file into a Snowflake table."""
    path = f"{parquet_file}" if parquet_file.startswith('/') else f"data/processed/{parquet_file}"
    load_parquet_to_snowflake(path, table)
    print("Snowflake load complete")


if __name__ == "__main__":
    app()