from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset, load_forecast
from backend.services.reports import generate_report_summary

router = APIRouter()


@router.get("/api/report")
async def generate_report():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    forecast_data = None
    if load_forecast() is not None:
        forecast_data = {"forecast_table": load_forecast().to_dict(orient="records")}
    return generate_report_summary(df, forecast_data)
