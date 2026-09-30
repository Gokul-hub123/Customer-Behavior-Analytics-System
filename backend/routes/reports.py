from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset, save_forecast
from backend.services.forecasting import run_forecast

router = APIRouter()


@router.post("/api/forecast")
async def create_forecast():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    if df is None:
        return {"message": "No dataset uploaded yet."}
    result = run_forecast(df)
    if "forecast_table" in result:
        import pandas as pd
        forecast_df = pd.DataFrame(result["forecast_table"])
        save_forecast(forecast_df)
    return result


@router.get("/api/forecast")
async def get_forecast():
    from backend.database import load_forecast
    import pandas as pd

    df = load_forecast()
    if df is None or df.empty:
        return {"message": "No forecast available."}
    return {"forecast_table": df.to_dict(orient="records")}
