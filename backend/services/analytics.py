from __future__ import annotations

import numpy as np
import pandas as pd

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
    renamed = {}
    for column in df.columns:
        key = str(column).strip().lower()
        matched = None
        for canonical, aliases in COLUMN_ALIASES.items():
            if key in {alias.lower() for alias in aliases}:
                matched = canonical
                break
        renamed[column] = matched if matched else column
    return df.rename(columns=renamed)


def build_standard_dataset(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("The uploaded file is empty.")

    normalized = normalize_columns(df)

    if "customer_id" not in normalized.columns:
        raise ValueError("Missing required customer identifier column.")
    if "date" not in normalized.columns:
        date_candidates = [c for c in normalized.columns if "date" in str(c).lower() or "time" in str(c).lower()]
        if not date_candidates:
            raise ValueError("Date column is missing. A valid transaction date is required.")
        normalized["date"] = normalized[date_candidates[0]]

    if "quantity" not in normalized.columns:
        raise ValueError("Missing quantity column. Please upload data with quantity information.")
    if "unit_price" not in normalized.columns and "total_amount" not in normalized.columns:
        raise ValueError("Missing price/sales column. Please upload Unit Price or Total Amount.")

    if "transaction_id" not in normalized.columns:
        normalized["transaction_id"] = [f"TXN_{idx + 1}" for idx in range(len(normalized))]
    if "product_id" not in normalized.columns:
        normalized["product_id"] = [f"PROD_{idx + 1}" for idx in range(len(normalized))]
    if "product_name" not in normalized.columns:
        normalized["product_name"] = normalized["product_id"].astype(str)
    if "category" not in normalized.columns:
        normalized["category"] = "General"

    normalized["customer_id"] = normalized["customer_id"].astype(str).str.strip()
    normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce")
    normalized["quantity"] = pd.to_numeric(normalized["quantity"], errors="coerce")

    if "unit_price" in normalized.columns:
        normalized["unit_price"] = pd.to_numeric(normalized["unit_price"], errors="coerce")
    if "total_amount" in normalized.columns:
        normalized["total_amount"] = pd.to_numeric(normalized["total_amount"], errors="coerce")

    if "total_amount" not in normalized.columns:
        normalized["total_amount"] = normalized["quantity"] * normalized["unit_price"]
    elif "unit_price" not in normalized.columns:
        normalized["unit_price"] = np.where(normalized["quantity"] != 0, normalized["total_amount"] / normalized["quantity"], 0)

    cleaned = normalized.dropna(subset=["customer_id", "date"]).copy()
    cleaned = cleaned[(cleaned["quantity"].notna()) & (cleaned["quantity"] >= 0)]
    cleaned = cleaned[(cleaned["unit_price"].notna()) & (cleaned["unit_price"] >= 0)]
    cleaned["total_amount"] = cleaned["quantity"] * cleaned["unit_price"]
    return cleaned.reset_index(drop=True)


def cleaning_summary(df: pd.DataFrame) -> dict:
    rows = len(df)
    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    invalid_records = 0
    if {"quantity", "unit_price"}.issubset(df.columns):
        invalid_records = int(((df["quantity"] < 0) | (df["unit_price"] < 0)).sum())
    return {
        "before_rows": rows,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_records": invalid_records,
    }


def clean_dataset(df: pd.DataFrame):
    before = df.copy()
    cleaned = before.drop_duplicates().copy()
    cleaned = cleaned.dropna(subset=["customer_id", "date"]).copy()

    for column in ["quantity", "unit_price", "total_amount"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

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
