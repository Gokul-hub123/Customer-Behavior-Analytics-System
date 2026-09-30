from __future__ import annotations

import sqlite3
from pathlib import Path

from backend.config import BASE_DIR

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
