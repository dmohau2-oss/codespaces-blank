"""Simple API for the dashboard to read ETL data."""

from __future__ import annotations

from typing import Optional

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.processor import DataProcessor, build_dashboard_payload

app = FastAPI(title="Data Processing ETL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/dashboard")
def dashboard(
    category: Optional[str] = Query(default=None),
    date_from: Optional[str] = Query(default=None),
    date_to: Optional[str] = Query(default=None),
) -> dict:
    processor = DataProcessor()
    raw_df = processor.load_data()

    if isinstance(raw_df, pd.DataFrame):
        df = raw_df
    elif hasattr(raw_df, "__iter__"):
        df = pd.concat(list(raw_df), ignore_index=True)
    else:
        df = pd.DataFrame(raw_df)

    if hasattr(df, "columns") and "date" not in df.columns:
        df = processor.enrich_with_dates(df)

    return build_dashboard_payload(df, category=category, date_from=date_from, date_to=date_to)
