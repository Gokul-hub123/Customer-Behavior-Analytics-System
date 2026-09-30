from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import HTTPException

from backend.config import DATA_DIR


def validate_uploaded_file(file_path: Path) -> None:
    if not file_path.exists():
        raise HTTPException(status_code=400, detail="File not found.")
    if file_path.stat().st_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")
    if file_path.suffix.lower() != ".csv":
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")


def read_uploaded_csv(file_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
    except Exception:
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid CSV file.")
    if df.empty:
        raise HTTPException(status_code=400, detail="The CSV file contains no data rows.")
    return df


def save_uploaded_dataset(file_path: Path, df: pd.DataFrame) -> None:
    destination = DATA_DIR / file_path.name
    df.to_csv(destination, index=False)
