from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset, load_forecast, save_forecast
from backend.services.forecasting import run_forecast

router = APIRouter()


@router.post("/api/forecast")
async def forecast():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    if df is None:
        return {"message": "Sales forecasting requires valid date and sales data in the uploaded dataset."}

    result = run_forecast(df)
    if "forecast_table" in result and result.get("forecast_table"):
        import pandas as pd

        forecast_df = pd.DataFrame(result["forecast_table"])
        forecast_df["mae"] = result.get("mae", 0)
        forecast_df["rmse"] = result.get("rmse", 0)
        save_forecast(forecast_df)
    return result


@router.get("/api/forecast")
async def get_forecast():
    df = load_forecast()
    if df is None or df.empty:
        return {"message": "No forecast result available."}
    return {
        "forecast_table": df.to_dict(orient="records"),
    }
