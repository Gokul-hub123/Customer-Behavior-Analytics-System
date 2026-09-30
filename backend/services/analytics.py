from __future__ import annotations

import pandas as pd
import numpy as np


COLUMN_ALIASES = {
    "customer_id": ["customerid", "customer_id", "customer", "client_id", "customer number"],
    "transaction_id": ["transactionid", "transaction_id", "invoiceid", "invoice_id", "order_id", "bill_id"],
    "date": ["date", "transactiondate", "transaction_date", "invoicedate", "invoice_date", "order_date"],
    "product_id": ["productid", "product_id", "sku", "item_id", "product"],
    "product_name": ["productname", "product_name", "item_name", "product_title"],
    "category": ["category", "productcategory", "department", "product_category"],
    "quantity": ["quantity", "qty", "ordered_quantity"],
    "unit_price": ["unitprice", "unit_price", "price", "unitcost"],
    "total_amount": ["totalamount", "total_amount", "sales", "revenue", "amount", "total_sales"],
}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    normalized_cols = {col: col for col in df.columns}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in df.columns:
                normalized_cols[alias] = canonical
                break
    return df.rename(columns=normalized_cols)


def build_standard_dataset(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("The uploaded file is empty.")

    df = normalize_columns(df)

    if "customer_id" not in df.columns:
        raise ValueError("Missing required customer identifier column.")
    if "date" not in df.columns:
        date_cols = [col for col in df.columns if "date" in str(col).lower() or "time" in str(col).lower()]
        if not date_cols:
            raise ValueError("Date column is missing. A valid transaction date is required.")
        df["date"] = df[date_cols[0]]

    if "quantity" not in df.columns:
        raise ValueError("Missing quantity column. Please upload data with quantity information.")

    if "unit_price" not in df.columns and "total_amount" not in df.columns:
        raise ValueError("Missing price/sales column. Please upload Unit Price or Total Amount.")

    if "transaction_id" not in df.columns:
        df["transaction_id"] = [f"TXN_{idx + 1}" for idx in range(len(df))]

    if "product_id" not in df.columns:
        df["product_id"] = [f"PROD_{idx + 1}" for idx in range(len(df))]

    if "product_name" not in df.columns:
        df["product_name"] = df["product_id"].astype(str)

    if "category" not in df.columns:
        df["category"] = "General"

    df["customer_id"] = df["customer_id"].astype(str)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    if "unit_price" in df.columns:
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    if "total_amount" in df.columns:
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")

    if "total_amount" not in df.columns:
        df["total_amount"] = df["quantity"] * df["unit_price"]
    elif "unit_price" not in df.columns:
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
    invalid_records = 0
    if {"quantity", "unit_price"}.issubset(df.columns):
        invalid_records = int(((df["quantity"] < 0) | (df["unit_price"] < 0)).sum())
    return {
        "before_rows": before_rows,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_records": invalid_records,
    }


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    before = df.copy()
    cleaned = before.drop_duplicates().copy()
    cleaned = cleaned.dropna(subset=["customer_id", "date"]).copy()

    for col in ["quantity", "unit_price", "total_amount"]:
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned["quantity"] = cleaned["quantity"].fillna(0)
    cleaned["unit_price"] = cleaned["unit_price"].fillna(0)
    cleaned = cleaned[(cleaned["quantity"] >= 0) & (cleaned["unit_price"] >= 0)]

    if "total_amount" in cleaned.columns:
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
