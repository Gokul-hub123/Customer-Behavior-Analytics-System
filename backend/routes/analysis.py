from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset, save_cleaned_dataset
from backend.services.data_processing import clean_dataset, cleaning_summary

router = APIRouter()


@router.get("/api/cleaning-summary")
async def get_cleaning_summary():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    if df is None:
        return {"message": "No dataset uploaded yet."}
    return cleaning_summary(df)


@router.post("/api/clean")
async def clean_data():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    if df is None:
        return {"message": "No dataset uploaded yet."}
    cleaned_df, summary = clean_dataset(df)
    save_cleaned_dataset(cleaned_df)
    return {"message": "Data cleaned successfully", "summary": summary, "rows": len(cleaned_df)}
