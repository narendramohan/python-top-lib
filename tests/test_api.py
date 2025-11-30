"""Tests for the API module."""

import io

import polars as pl
from fastapi.testclient import TestClient

from src.api.main import app
from src.api.models import Record

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_record_model_valid():
    """Test Record model with valid data."""
    record = Record(id=1, email="test@example.com", age=25)
    assert record.id == 1
    assert record.email == "test@example.com"
    assert record.age == 25


def test_record_model_invalid_id():
    """Test Record model with invalid id (must be > 0)."""
    try:
        Record(id=0, email="test@example.com", age=25)
        assert False, "Should have raised validation error"
    except Exception:
        assert True


def test_record_model_invalid_age():
    """Test Record model with invalid age (must be 0 < age < 120)."""
    try:
        Record(id=1, email="test@example.com", age=150)
        assert False, "Should have raised validation error"
    except Exception:
        assert True


def test_record_model_invalid_email():
    """Test Record model with invalid email."""
    try:
        Record(id=1, email="not-an-email", age=25)
        assert False, "Should have raised validation error"
    except Exception:
        assert True


def test_validate_endpoint_valid_csv():
    """Test validate endpoint with valid CSV data."""
    csv_data = "id,email,age\n1,test1@example.com,25\n2,test2@example.com,30"
    csv_file = io.BytesIO(csv_data.encode())

    response = client.post(
        "/validate/",
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 2
    assert data["errors"] == []


def test_validate_endpoint_invalid_csv():
    """Test validate endpoint with invalid data in CSV."""
    csv_data = "id,email,age\n1,invalid-email,25\n2,test2@example.com,30"
    csv_file = io.BytesIO(csv_data.encode())

    response = client.post(
        "/validate/",
        files={"file": ("test.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 2
    assert len(data["errors"]) >= 1  # At least one error for invalid email
