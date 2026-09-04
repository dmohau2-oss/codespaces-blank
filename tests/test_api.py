"""Endpoint tests for the dashboard API."""

import pandas as pd
from fastapi.testclient import TestClient

from src.api import app
from src.processor import DataProcessor


client = TestClient(app)


def test_health_endpoint_returns_ok():
    """The health endpoint should report that the API is ready."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_dashboard_endpoint_filters_by_category_and_date(monkeypatch):
    """The dashboard endpoint should return only rows matching its filters."""
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "value": [10.0, 20.0, 30.0],
            "category": ["A", "B", "A"],
            "date": pd.to_datetime(["2026-08-01", "2026-08-02", "2026-08-03"]),
        }
    )
    monkeypatch.setattr(DataProcessor, "load_data", lambda self: data)

    response = client.get(
        "/dashboard",
        params={"category": "A", "date_from": "2026-08-01", "date_to": "2026-08-02"},
    )

    assert response.status_code == 200
    assert response.json()["summary"]["row_count"] == 1
    assert response.json()["summary"]["total"] == 10.0
    assert response.json()["rows"][0]["name"] == "Alice"