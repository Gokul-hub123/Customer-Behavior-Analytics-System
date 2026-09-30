from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset
from backend.services.analytics import get_eda_data

router = APIRouter()


@router.get("/api/analysis")
async def analysis_data():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    return get_eda_data(df)
