from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_current_dataset
from backend.services.analytics import get_dashboard_data

router = APIRouter()


@router.get("/api/dashboard")
async def dashboard_data():
    df = load_current_dataset()
    data = get_dashboard_data(df)
    return data
