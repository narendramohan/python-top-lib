"""Data quality check execution.

This module applies the defined rules in `dq.rules` to a dataset and reports the number of failing rows per rule.
"""

import polars as pl

from ..core.config import settings
from ..core.logger import get_logger
from .rules import RULES

logger = get_logger()


def run_dq() -> None:
    """Run data quality checks on the raw input CSV.

    Reads the input CSV from the configured raw data directory and applies each rule from the RULES dictionary.
    Logs the number of failed rows per rule and prints a summary.
    """
    file_path = f"{settings.raw_dir}/input.csv"
    try:
        df = pl.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"Input file {file_path} not found.")
        return

    results: dict[str, int] = {}
    for name, rule in RULES.items():
        failing = df.filter(~rule(df))
        results[name] = failing.shape[0]
        logger.info(f"Rule {name}: {results[name]} failing rows")

    # Print summary to stdout
    print(results)
