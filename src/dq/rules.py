"""Data quality rules for validating datasets.

Each rule is a callable that accepts a Polars DataFrame and returns a Boolean mask or performs a check.
"""

import polars as pl


# Define rules as functions returning boolean series
def email_not_null(df: pl.DataFrame) -> pl.Series:
    return df["email"].is_not_null()


def age_valid(df: pl.DataFrame) -> pl.Series:
    return (df["age"] > 0) & (df["age"] < 120)


RULES = {
    "email_not_null": email_not_null,
    "age_valid": age_valid,
}
