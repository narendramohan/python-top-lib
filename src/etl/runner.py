"""Top-level ETL runner function."""

from core.logger import get_logger
from .extract import extract_local
from .transform import filter_adults
from .load import load_parquet

logger = get_logger()


def run_etl() -> None:
    """Execute the full ETL pipeline end to end.

    This function extracts data from the default input CSV (input.csv), transforms it by filtering for adults,
    and writes the result to a Parquet file in the processed directory.
    """
    logger.info("Starting ETL pipeline")
    df = extract_local("input.csv")
    df_t = filter_adults(df)
    load_parquet(df_t, "output.parquet")
    logger.info("ETL pipeline complete")