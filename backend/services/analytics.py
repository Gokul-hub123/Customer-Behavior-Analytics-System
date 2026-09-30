from __future__ import annotations

import numpy as np
import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    column_mapping = {
        "customer_id": ["customerid", "customer_id", "customer", "customerid", "client_id"],
        "transaction_id": ["transactionid", "transaction_id", "invoiceid", "invoice_id", "order_id", "bill_id"],
        "date": ["date", "transactiondate", "invoicedate", "invoice_date", "order_date"],
        "product_id": ["productid", "product_id", "sku", "item_id"],
        "product_name": ["productname", "product_name", "product", "item_name"],
        "category": ["category", "productcategory", "department"],
        "quantity": ["quantity", "qty", "ordered_quantity"],
        "unit_price": ["unitprice", "unit_price", "price", "unitcost"],
        "total_amount": ["totalamount", "total_amount", "sales", "revenue", "amount", "total_sales"],
    }

    normalized = df.copy()
    for canonical, aliases in column_mapping.items():
        for alias in aliases:
            if alias in normalized.columns:
                normalized.rename(columns={alias: canonical}, inplace=True)
                break
    return normalized


def detect_date_column(df: pd.DataFrame) -> str:
    for col in ["date", "transaction_date", "invoice_date", "order_date"]:
        if col in df.columns:
            return col
    for col in df.columns:
        if "date" in str(col).lower() or "time" in str(col).lower():
            return col
    raise ValueError("A valid date column is required for analysis.")


def build_standard_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    if df.empty:
        raise ValueError("Dataset is empty.")

    date_col = detect_date_column(df)
    if "customer_id" not in df.columns:
        raise ValueError("Customer identifier column is missing.")
    if "quantity" not in df.columns:
        raise ValueError("Quantity column is missing.")
    if "unit_price" not in df.columns and "total_amount" not in df.columns:
        raise ValueError("Price column or total sales column is missing.")

    df["transaction_id"] = df.get("transaction_id", df.index.astype(str))
    if "product_id" not in df.columns:
        df["product_id"] = df.index.astype(str)
    if "product_name" not in df.columns:
        df["product_name"] = df.get("product_id", df.index.astype(str)).astype(str)
    if "category" not in df.columns:
        df["category"] = "General"

    df["customer_id"] = df["customer_id"].astype(str)
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    if "unit_price" in df.columns:
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    if "total_amount" in df.columns:
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")

    if "unit_price" in df.columns and "total_amount" not in df.columns:
        df["total_amount"] = (df["quantity"] * df["unit_price"]).fillna(0)
    elif "unit_price" not in df.columns and "total_amount" in df.columns:
        df["unit_price"] = np.where(df["quantity"] != 0, df["total_amount"] / df["quantity"], 0)

    df = df.dropna(subset=["customer_id", "date"]).copy()
    df = df[(df["quantity"].notna()) & (df["quantity"] >= 0)]
    df = df[(df["unit_price"].notna()) & (df["unit_price"] >= 0)]
    df["total_amount"] = df["quantity"] * df["unit_price"]
    return df.reset_index(drop=True)


def cleaning_summary(df: pd.DataFrame) -> dict:
    before_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    missing_values = int(df.isna().sum().sum())
    invalid_records = int(((df["quantity"] < 0) | (df["unit_price"] < 0)).sum()) if {"quantity", "unit_price"}.issubset(df.columns) else 0
    return {
        "total_rows": before_rows,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_records": invalid_records,
    }


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    before = df.copy()
    cleaned = df.drop_duplicates().copy()
    cleaned = cleaned.dropna(subset=["customer_id", "date"]).copy()

    for col in ["quantity", "unit_price", "total_amount"]:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
    cleaned["quantity"] = cleaned["quantity"].fillna(0)
    cleaned["unit_price"] = cleaned["unit_price"].fillna(0)
    cleaned = cleaned[(cleaned["quantity"] >= 0) & (cleaned["unit_price"] >= 0)]
    cleaned["total_amount"] = cleaned["quantity"] * cleaned["unit_price"]

    rows_removed = len(before) - len(cleaned)
    summary = {
        "before_rows": len(before),
        "after_rows": len(cleaned),
        "rows_removed": rows_removed,
        "duplicate_rows_removed": int(before.duplicated().sum()),
        "remaining_missing_values": int(cleaned.isna().sum().sum()),
    }
    return cleaned.reset_index(drop=True), summary
