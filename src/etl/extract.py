"""Extraction functions for the ETL pipeline."""

import polars as pl
from core.config import settings
from core.logger import get_logger
from .s3 import download_from_s3

logger = get_logger()


def extract_local(file_name: str) -> pl.DataFrame:
    """Read a CSV file from the raw data directory into a Polars DataFrame.

    Args:
        file_name: Name of the CSV file to read (within the raw directory).

    Returns:
        A Polars DataFrame containing the file contents.
    """
    path = f"{settings.raw_dir}/{file_name}"
    logger.info(f"Reading local file {path}")
    return pl.read_csv(path)


def extract_from_s3(key: str) -> pl.DataFrame:
    """Download a CSV from S3 and read it into a DataFrame.

    This function will download the object specified by `key` from the configured S3 bucket
    into the raw directory, then load it as a Polars DataFrame.

    Args:
        key: S3 object key (path within the bucket)

    Returns:
        A Polars DataFrame containing the data.
    """
    # download file
    local_path = download_from_s3(key, destination_dir=settings.raw_dir)
    logger.info(f"Downloaded {key} to {local_path}")
    return pl.read_csv(local_path)