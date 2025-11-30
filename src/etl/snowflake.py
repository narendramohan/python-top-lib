"""Snowflake loader utilities."""

import snowflake.connector

from ..core.config import settings
from ..core.logger import get_logger

logger = get_logger()


def get_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    """Create a connection to Snowflake using configured credentials."""
    if not (
        settings.snowflake_account
        and settings.snowflake_user
        and settings.snowflake_password
        and settings.snowflake_warehouse
        and settings.snowflake_database
        and settings.snowflake_schema
    ):
        raise RuntimeError(
            "Snowflake credentials are incomplete. Please set them in your .env file."
        )

    ctx = snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        role=settings.snowflake_role,
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=settings.snowflake_schema,
    )
    return ctx


def load_parquet_to_snowflake(parquet_path: str, table_name: str) -> None:
    """Load a Parquet file from local storage into a Snowflake table.

    This function uses the Snowflake PUT and COPY INTO commands to upload the file and load it.
    Note: the table must already exist in Snowflake with appropriate columns matching the Parquet schema.

    Args:
        parquet_path: Path to the local Parquet file.
        table_name: Fully-qualified target table name (e.g. SCHEMA.TABLE).
    """
    conn = get_snowflake_connection()
    cs = conn.cursor()
    try:
        # Stage name: use a temporary internal stage
        stage_name = f"@%{table_name}"

        # Put the file into stage
        logger.info(f"Uploading {parquet_path} to stage {stage_name}")
        put_cmd = f"PUT file://{parquet_path} {stage_name} AUTO_COMPRESS=TRUE OVERWRITE=TRUE"
        cs.execute(put_cmd)

        # Copy into table
        logger.info(f"Copying into {table_name}")
        copy_cmd = f"COPY INTO {table_name} FROM {stage_name} FILE_FORMAT = (TYPE = 'PARQUET')"
        cs.execute(copy_cmd)

        logger.info("Snowflake load completed")
    finally:
        cs.close()
        conn.close()
