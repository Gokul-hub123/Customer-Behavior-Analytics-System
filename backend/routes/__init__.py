from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def run_forecast(df: pd.DataFrame) -> dict:
    if df.empty or "date" not in df.columns or "total_amount" not in df.columns:
        return {"message": "Sales forecasting requires valid date and sales data in the uploaded dataset."}

    monthly_sales = (
        df.assign(month=df["date"].dt.to_period("M"))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
    )

    if monthly_sales.empty:
        return {"message": "Sales forecasting requires valid date and sales data in the uploaded dataset."}

    monthly_sales = monthly_sales.sort_values("month").reset_index(drop=True)
    monthly_sales["time_index"] = np.arange(len(monthly_sales))

    model = LinearRegression()
    X = monthly_sales[["time_index"]]
    y = monthly_sales["sales"]

    model.fit(X, y)
    predictions = model.predict(X)
    mae = float(np.mean(np.abs(y - predictions)))
    rmse = float(np.sqrt(np.mean((y - predictions) ** 2)))

    future_index = np.arange(len(monthly_sales), len(monthly_sales) + 3)
    future_sales = model.predict(future_index.reshape(-1, 1))
    future_months = pd.period_range(monthly_sales["month"].iloc[-1] + 1, periods=3, freq="M")

    forecast_table = pd.DataFrame(
        {
            "forecast_month": [str(month) for month in future_months],
            "predicted_sales": future_sales.round(2),
        }
    )

    return {
        "historical_sales": monthly_sales[["month", "sales"]].rename(columns={"month": "date", "sales": "sales"}).to_dict(orient="records"),
        "forecast_table": forecast_table.to_dict(orient="records"),
        "model_used": "Linear Regression",
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "message": "Forecast results are estimates based on historical sales patterns and may differ from actual future sales.",
    }
