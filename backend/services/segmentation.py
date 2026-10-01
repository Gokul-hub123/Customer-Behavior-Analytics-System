from __future__ import annotations

import numpy as np
import pandas as pd


def _safe_numeric(series: pd.Series) -> pd.Series:
    if series is None:
        return pd.Series(dtype=float)
    return pd.to_numeric(series, errors="coerce").fillna(0)


def get_dashboard_data(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {
            "total_customers": 0,
            "total_transactions": 0,
            "total_sales": 0,
            "average_purchase_value": 0,
            "monthly_sales": [],
            "category_sales": [],
            "top_products": [],
            "customer_distribution": [],
            "key_insights": ["Upload a dataset to get started."],
        }

    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    total_customers = int(df["customer_id"].nunique()) if "customer_id" in df.columns else 0
    total_transactions = int(df["transaction_id"].nunique()) if "transaction_id" in df.columns else int(len(df))
    total_sales = float(_safe_numeric(df["total_amount"]).sum()) if "total_amount" in df.columns else 0.0
    average_purchase_value = float(total_sales / len(df)) if len(df) else 0.0

    monthly = pd.DataFrame()
    if "date" in df.columns and "total_amount" in df.columns:
        monthly = (
            df.assign(month=df["date"].dt.to_period("M"))
            .groupby("month", as_index=False)["total_amount"]
            .sum()
            .rename(columns={"total_amount": "sales"})
        )
        monthly["month"] = monthly["month"].astype(str)

    category_sales = pd.DataFrame()
    if "category" in df.columns and "total_amount" in df.columns:
        category_sales = (
            df.groupby("category", as_index=False)["total_amount"]
            .sum()
            .rename(columns={"total_amount": "sales"})
            .sort_values("sales", ascending=False)
            .head(5)
        )

    top_products = pd.DataFrame()
    if "product_name" in df.columns and "total_amount" in df.columns:
        top_products = (
            df.groupby("product_name", as_index=False)["total_amount"]
            .sum()
            .rename(columns={"total_amount": "sales"})
            .sort_values("sales", ascending=False)
            .head(5)
        )

    distribution = pd.DataFrame({"range": ["0-100", "101-500", "501-1000", "1000+"], "customers": [0, 0, 0, 0]})
    if "total_amount" in df.columns:
        total_spend = df.groupby("customer_id")["total_amount"].sum().reset_index()
        bins = np.array([0, 100, 500, 1000, np.inf])
        labels = ["0-100", "101-500", "501-1000", "1000+"]
        counts, _ = np.histogram(total_spend["total_amount"], bins=bins)
        distribution = pd.DataFrame({"range": labels, "customers": counts.tolist()})

    insights = []
    if not monthly.empty:
        max_month = monthly.loc[monthly["sales"].idxmax()]
        insights.append(f"Peak sales month was {max_month['month']} with ₹{max_month['sales']:.2f} in sales.")
    if not category_sales.empty:
        top_category = category_sales.iloc[0]
        insights.append(f"The strongest category is {top_category['category']} with ₹{top_category['sales']:.2f} in revenue.")
    if not top_products.empty:
        top_product = top_products.iloc[0]
        insights.append(f"Top product is {top_product['product_name']} contributing ₹{top_product['sales']:.2f}.")
    if total_customers:
        insights.append(f"The business has {total_customers} active customers in the current dataset.")
    if not insights:
        insights.append("Upload a valid retail dataset to generate meaningful insights.")

    return {
        "total_customers": total_customers,
        "total_transactions": total_transactions,
        "total_sales": round(total_sales, 2),
        "average_purchase_value": round(average_purchase_value, 2),
        "monthly_sales": monthly.to_dict(orient="records"),
        "category_sales": category_sales.to_dict(orient="records"),
        "top_products": top_products.to_dict(orient="records"),
        "customer_distribution": distribution.to_dict(orient="records"),
        "key_insights": insights[:5],
    }


def get_eda_data(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {"message": "No dataset uploaded yet."}

    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    sales_series = _safe_numeric(df["total_amount"]) if "total_amount" in df.columns else pd.Series(0)

    monthly_sales = pd.DataFrame()
    if "date" in df.columns and "total_amount" in df.columns:
        monthly_sales = (
            df.assign(month=df["date"].dt.to_period("M"))
            .groupby("month", as_index=False)["total_amount"]
            .sum()
            .rename(columns={"total_amount": "sales"})
        )
        monthly_sales["month"] = monthly_sales["month"].astype(str)

    top_categories = pd.DataFrame()
    if "category" in df.columns and "total_amount" in df.columns:
        top_categories = (
            df.groupby("category", as_index=False)["total_amount"]
            .sum()
            .rename(columns={"total_amount": "sales"})
            .sort_values("sales", ascending=False)
            .head(5)
        )

    top_products = pd.DataFrame()
    if "product_name" in df.columns and "total_amount" in df.columns:
        top_products = (
            df.groupby("product_name", as_index=False)["total_amount"]
            .sum()
            .rename(columns={"total_amount": "sales"})
            .sort_values("sales", ascending=False)
            .head(5)
        )

    result = {
        "total_sales": round(float(sales_series.sum()), 2),
        "average_sales": round(float(sales_series.mean()), 2),
        "minimum_sale": round(float(sales_series.min()), 2),
        "maximum_sale": round(float(sales_series.max()), 2),
        "total_customers": int(df["customer_id"].nunique()) if "customer_id" in df.columns else 0,
        "total_transactions": int(df["transaction_id"].nunique()) if "transaction_id" in df.columns else int(len(df)),
        "top_products": top_products.to_dict(orient="records"),
        "top_categories": top_categories.to_dict(orient="records"),
        "monthly_sales": monthly_sales.to_dict(orient="records"),
    }
    return result
