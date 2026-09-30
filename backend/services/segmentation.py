from __future__ import annotations

import numpy as np
import pandas as pd


def get_dashboard_data(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {"message": "No dataset uploaded yet."}

    total_customers = int(df["customer_id"].nunique())
    total_transactions = int(df["transaction_id"].nunique()) if "transaction_id" in df.columns else int(len(df))
    total_sales = float(df["total_amount"].sum())
    avg_purchase = float(df["total_amount"].mean()) if len(df) else 0

    monthly_sales = (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
    )

    category_sales = (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .head(10)
        .rename(columns={"total_amount": "sales"})
    )

    top_products = (
        df.groupby("product_name", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .head(5)
        .rename(columns={"total_amount": "sales"})
    )

    customer_values = df.groupby("customer_id", as_index=False)["total_amount"].sum()
    customer_values["bucket"] = pd.cut(
        customer_values["total_amount"],
        bins=[0, 200, 500, 1000, np.inf],
        labels=["Low", "Medium", "High", "Very High"],
    )
    customer_distribution = customer_values["bucket"].value_counts().reset_index()
    customer_distribution.columns = ["range", "customers"]

    insights = []
    if not category_sales.empty:
        top_category = category_sales.iloc[0]
        insights.append(f"Top category is {top_category['category']} with sales of ₹{top_category['sales']:.2f}.")
    if not monthly_sales.empty:
        peak_month = monthly_sales.loc[monthly_sales["sales"].idxmax()]
        insights.append(f"Peak sales month is {peak_month['month']} with ₹{peak_month['sales']:.2f}.")
    insights.append(f"Total unique customers in the dataset: {total_customers}.")
    insights.append(f"Average purchase value is ₹{avg_purchase:.2f} per transaction.")

    return {
        "total_customers": total_customers,
        "total_transactions": total_transactions,
        "total_sales": round(total_sales, 2),
        "average_purchase_value": round(avg_purchase, 2),
        "monthly_sales": monthly_sales.to_dict(orient="records"),
        "category_sales": category_sales.to_dict(orient="records"),
        "top_products": top_products.to_dict(orient="records"),
        "customer_distribution": customer_distribution.to_dict(orient="records"),
        "key_insights": insights[:5],
    }


def get_eda_data(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {"message": "No data available."}

    total_sales = float(df["total_amount"].sum())
    average_sales = float(df["total_amount"].mean())
    min_sale = float(df["total_amount"].min())
    max_sale = float(df["total_amount"].max())
    total_customers = int(df["customer_id"].nunique())
    total_transactions = int(df["transaction_id"].nunique()) if "transaction_id" in df.columns else int(len(df))

    monthly_sales = (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
    )

    category_sales = (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .rename(columns={"total_amount": "sales"})
    )

    top_products = (
        df.groupby("product_name", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .head(10)
        .rename(columns={"total_amount": "sales"})
    )

    customer_purchase_distribution = (
        df.groupby("customer_id", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "amount"})
    )

    return {
        "total_sales": round(total_sales, 2),
        "average_sales": round(average_sales, 2),
        "minimum_sale": round(min_sale, 2),
        "maximum_sale": round(max_sale, 2),
        "total_customers": total_customers,
        "total_transactions": total_transactions,
        "top_products": top_products.to_dict(orient="records"),
        "top_categories": category_sales.to_dict(orient="records"),
        "monthly_sales": monthly_sales.to_dict(orient="records"),
        "customer_purchase_distribution": customer_purchase_distribution.to_dict(orient="records"),
    }
