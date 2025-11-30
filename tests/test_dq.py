"""Tests for the data quality module."""

import polars as pl

from src.dq.rules import RULES, age_valid, email_not_null


def test_email_not_null_rule():
    """Test email_not_null rule with valid and null emails."""
    data = {
        "id": [1, 2, 3],
        "email": ["test@example.com", None, "another@example.com"],
        "age": [25, 30, 35],
    }
    df = pl.DataFrame(data)

    result = email_not_null(df)

    assert result.to_list() == [True, False, True]


def test_age_valid_rule():
    """Test age_valid rule with various age values."""
    data = {
        "id": [1, 2, 3, 4, 5],
        "email": ["a@test.com", "b@test.com", "c@test.com", "d@test.com", "e@test.com"],
        "age": [0, 25, 119, 120, -5],
    }
    df = pl.DataFrame(data)

    result = age_valid(df)

    # Valid: 25, 119 (0 < age < 120)
    # Invalid: 0, 120, -5
    assert result.to_list() == [False, True, True, False, False]


def test_age_valid_boundary():
    """Test age_valid rule boundaries (0 < age < 120)."""
    data = {
        "id": [1, 2, 3, 4],
        "email": ["a@test.com", "b@test.com", "c@test.com", "d@test.com"],
        "age": [1, 50, 119, 120],
    }
    df = pl.DataFrame(data)

    result = age_valid(df)

    # 1 and 119 are valid, 120 and out of range are invalid
    assert result.to_list() == [True, True, True, False]


def test_rules_dictionary():
    """Test that RULES dictionary contains expected rules."""
    assert "email_not_null" in RULES
    assert "age_valid" in RULES
    assert callable(RULES["email_not_null"])
    assert callable(RULES["age_valid"])


def test_rules_applied_to_dataset():
    """Test applying rules to a complete dataset."""
    data = {
        "id": [1, 2, 3, 4],
        "email": ["a@test.com", None, "c@test.com", "d@test.com"],
        "age": [25, 30, 150, 18],
    }
    df = pl.DataFrame(data)

    # Row 0: email valid (0 < age < 120), age valid -> passes both
    # Row 1: email null, age valid (0 < age < 120) -> fails email_not_null
    # Row 2: email valid, age invalid (150 >= 120) -> fails age_valid
    # Row 3: email valid, age valid (0 < 18 < 120) -> passes age_valid

    email_rule_result = RULES["email_not_null"](df)
    age_rule_result = RULES["age_valid"](df)

    assert email_rule_result.to_list() == [True, False, True, True]
    assert age_rule_result.to_list() == [True, True, False, True]

    # Count failing rows for each rule
    email_failures = (~email_rule_result).sum()
    age_failures = (~age_rule_result).sum()

    assert email_failures == 1
    assert age_failures == 1
