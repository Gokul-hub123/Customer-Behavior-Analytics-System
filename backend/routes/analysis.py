from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset
from backend.services.analytics import get_dashboard_data

router = APIRouter()


@router.get("/api/dashboard")
async def dashboard():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    if df is None:
        return {
            "message": "No dataset uploaded yet.",
            "total_customers": 0,
            "total_transactions": 0,
            "total_sales": 0,
            "average_purchase_value": 0,
            "monthly_sales": [],
            "category_sales": [],
            "top_products": [],
            "customer_distribution": [],
            "key_insights": ["Upload a dataset to generate the dashboard."],
        }
    return get_dashboard_data(df)
