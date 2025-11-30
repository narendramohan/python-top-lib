"""Transformation functions for the ETL pipeline."""

import polars as pl


def filter_adults(df: pl.DataFrame) -> pl.DataFrame:
    """Filter out rows where age is less than 18.

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame containing only rows with age > 18.
    """
    return df.filter(pl.col("age") > 18)
