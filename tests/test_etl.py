"""Tests for the ETL module."""

import polars as pl

from src.etl.transform import filter_adults


def test_filter_adults_basic():
    """Test filter_adults removes rows with age <= 18."""
    data = {
        "id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", "Charlie", "David"],
        "age": [25, 17, 18, 19],
    }
    df = pl.DataFrame(data)

    result = filter_adults(df)

    assert result.shape[0] == 2  # Only 2 adults (25, 19)
    assert result["age"].to_list() == [25, 19]


def test_filter_adults_all_adults():
    """Test filter_adults when all rows are adults."""
    data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [20, 25, 30],
    }
    df = pl.DataFrame(data)

    result = filter_adults(df)

    assert result.shape[0] == 3
    assert result.shape == df.shape


def test_filter_adults_no_adults():
    """Test filter_adults when no rows are adults."""
    data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [10, 15, 18],
    }
    df = pl.DataFrame(data)

    result = filter_adults(df)

    assert result.shape[0] == 0
    assert result.shape == (0, 3)


def test_filter_adults_edge_case_18():
    """Test filter_adults boundary: age=18 should be filtered out."""
    data = {
        "id": [1, 2],
        "name": ["Alice", "Bob"],
        "age": [18, 19],
    }
    df = pl.DataFrame(data)

    result = filter_adults(df)

    assert result.shape[0] == 1
    assert result["age"][0] == 19


def test_filter_adults_preserves_columns():
    """Test filter_adults preserves all columns."""
    data = {
        "id": [1, 2, 3],
        "email": ["a@test.com", "b@test.com", "c@test.com"],
        "age": [25, 17, 30],
    }
    df = pl.DataFrame(data)

    result = filter_adults(df)

    assert set(result.columns) == {"id", "email", "age"}
    assert result.shape[0] == 2
