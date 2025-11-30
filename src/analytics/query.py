"""Analytics functions leveraging DuckDB for ad‑hoc SQL queries."""

import duckdb

from ..core.logger import get_logger

logger = get_logger()


def run_query(sql: str) -> None:
    """Execute a SQL query using DuckDB and print the results.

    Args:
        sql: The SQL query to execute.
    """
    logger.info(f"Running analytics query: {sql}")
    con = duckdb.connect()
    try:
        df = con.execute(sql).df()
        print(df)
    finally:
        con.close()
