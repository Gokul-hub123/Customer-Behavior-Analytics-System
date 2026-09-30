from __future__ import annotations

import pandas as pd


def generate_report_summary(df: pd.DataFrame, forecast_data: dict | None = None) -> dict:
    if df is None or df.empty:
        return {
            "dataset_summary": {"records": 0, "customers": 0, "transactions": 0},
            "sales_summary": {"total_sales": 0, "average_purchase": 0, "top_category": "N/A", "top_product": "N/A"},
            "customer_summary": {"segments": 0, "customers_per_segment": {}},
            "forecast_summary": {"next_3_months_forecast": [], "model_used": "Linear Regression"},
            "key_findings": ["Upload a valid dataset to generate a report."],
        }

    dataset = {
        "records": int(len(df)),
        "customers": int(df["customer_id"].nunique()),
        "transactions": int(df["transaction_id"].nunique()) if "transaction_id" in df.columns else int(len(df)),
    }

    sales = df["total_amount"].sum()
    category_summary = df.groupby("category")["total_amount"].sum().sort_values(ascending=False)
    product_summary = df.groupby("product_name")["total_amount"].sum().sort_values(ascending=False)

    sales_summary = {
        "total_sales": round(float(sales), 2),
        "average_purchase": round(float(df["total_amount"].mean()), 2),
        "top_category": category_summary.index[0] if not category_summary.empty else "N/A",
        "top_product": product_summary.index[0] if not product_summary.empty else "N/A",
    }

    segment_count = 3 if "cluster" in df.columns else 0
    customer_summary = {
        "segments": segment_count,
        "customers_per_segment": {
            "High-value customers": int((df["cluster"] == 0).sum()) if "cluster" in df.columns else 0,
            "Regular customers": int((df["cluster"] == 1).sum()) if "cluster" in df.columns else 0,
            "Less-active customers": int((df["cluster"] == 2).sum()) if "cluster" in df.columns else 0,
        },
    }

    forecast_summary = {
        "next_3_months_forecast": [],
        "model_used": "Linear Regression",
    }
    if forecast_data and isinstance(forecast_data, dict) and "forecast_table" in forecast_data:
        forecast_summary["next_3_months_forecast"] = forecast_data["forecast_table"]

    findings = [
        f"The dataset contains {dataset['records']} records across {dataset['customers']} unique customers.",
        f"Total sales generated are ₹{sales_summary['total_sales']:.2f}.",
        f"The highest revenue category is {sales_summary['top_category']}.",
        f"The best-selling product is {sales_summary['top_product']}.",
        "Customer segmentation shows different purchasing patterns that can guide marketing strategy.",
    ]

    if forecast_data and "message" in forecast_data:
        findings.append(forecast_data["message"])

    return {
        "dataset_summary": dataset,
        "sales_summary": sales_summary,
        "customer_summary": customer_summary,
        "forecast_summary": forecast_summary,
        "key_findings": findings[:6],
    }
