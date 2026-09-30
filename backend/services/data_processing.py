from __future__ import annotations

import sqlite3
from pathlib import Path

from backend.config import BASE_DIR, CURRENT_DATASET_PATH, CLEANED_DATASET_PATH, SEGMENTS_PATH, FORECAST_PATH

DB_PATH = BASE_DIR / "customer_behavior.db"


def get_sqlite_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_sqlite_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            row_count INTEGER,
            column_count INTEGER,
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customer_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            recency INTEGER,
            frequency INTEGER,
            monetary REAL,
            cluster INTEGER,
            cluster_label TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            forecast_month TEXT,
            predicted_sales REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_current_dataset(df):
    if df is not None and not df.empty:
        df.to_csv(CURRENT_DATASET_PATH, index=False)


def load_current_dataset():
    if CURRENT_DATASET_PATH.exists():
        import pandas as pd
        return pd.read_csv(CURRENT_DATASET_PATH)
    return None


def save_cleaned_dataset(df):
    if df is not None and not df.empty:
        df.to_csv(CLEANED_DATASET_PATH, index=False)


def load_cleaned_dataset():
    if CLEANED_DATASET_PATH.exists():
        import pandas as pd
        return pd.read_csv(CLEANED_DATASET_PATH)
    return None


def save_segments(df):
    if df is not None and not df.empty:
        df.to_csv(SEGMENTS_PATH, index=False)


def load_segments():
    if SEGMENTS_PATH.exists():
        import pandas as pd
        return pd.read_csv(SEGMENTS_PATH)
    return None


def save_forecast(df):
    if df is not None and not df.empty:
        df.to_csv(FORECAST_PATH, index=False)


def load_forecast():
    if FORECAST_PATH.exists():
        import pandas as pd
        return pd.read_csv(FORECAST_PATH)
    return None
