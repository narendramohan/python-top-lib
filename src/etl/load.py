"""Load functions for the ETL pipeline."""

import polars as pl

from ..core.config import settings
from ..core.logger import get_logger
from .snowflake import load_parquet_to_snowflake

logger = get_logger()


def load_parquet(df: pl.DataFrame, file_name: str) -> str:
    """Write the DataFrame to a Parquet file in the processed directory.

    Args:
        df: DataFrame to write.
        file_name: Name of the Parquet file (within processed directory).

    Returns:
        The path to the Parquet file.
    """
    path = f"{settings.processed_dir}/{file_name}"
    logger.info(f"Writing Parquet to {path}")
    df.write_parquet(path)
    return path


def load_snowflake(parquet_path: str, table_name: str) -> None:
    """Load a Parquet file into a Snowflake table.

    Args:
        parquet_path: Path to the Parquet file to load.
        table_name: Name of the target Snowflake table (schema.table).
    """
    logger.info(f"Loading {parquet_path} into Snowflake table {table_name}")
    load_parquet_to_snowflake(parquet_path, table_name)
