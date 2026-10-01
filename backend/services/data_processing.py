from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset, load_forecast
from backend.services.reports import build_report_summary

router = APIRouter()


@router.get("/api/report")
async def generate_report():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    forecast_data = None
    saved_forecast = load_forecast()
    if saved_forecast is not None and not saved_forecast.empty:
        forecast_data = {
            "forecast_table": saved_forecast.to_dict(orient="records"),
            "message": "Forecast results are estimates based on historical sales patterns and may differ from actual future sales.",
        }
    return build_report_summary(df, forecast_data)
