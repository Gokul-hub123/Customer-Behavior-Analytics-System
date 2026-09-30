from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_current_dataset
from backend.services.analytics import get_dashboard_data

router = APIRouter()


@router.get("/api/dashboard")
async def dashboard_data():
    df = load_current_dataset()
    if df is None:
        return {"message": "No dataset uploaded yet."}
    return get_dashboard_data(df)
