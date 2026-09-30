from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "customer_behavior_db")
USE_MYSQL = os.getenv("USE_MYSQL", "false").lower() == "true"

UPLOADS_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "frontend"

UPLOADS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
FRONTEND_DIR.mkdir(exist_ok=True, parents=True)

CURRENT_DATASET_PATH = DATA_DIR / "current_dataset.csv"
CLEANED_DATASET_PATH = DATA_DIR / "cleaned_dataset.csv"
SEGMENTS_PATH = DATA_DIR / "segments.csv"
FORECAST_PATH = DATA_DIR / "forecast.csv"
