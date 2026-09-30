from __future__ import annotations

from fastapi import APIRouter

from backend.database import load_cleaned_dataset, load_current_dataset, load_segments, save_segments
from backend.services.segmentation import run_customer_segmentation

router = APIRouter()


@router.post("/api/segmentation")
async def run_segmentation():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    if df is None:
        return {"message": "No dataset uploaded yet."}
    result = run_customer_segmentation(df)
    if "segments" in result:
        import pandas as pd
        segments_df = pd.DataFrame(result["segments"])
        save_segments(segments_df)
    return result


@router.get("/api/segments")
async def get_segments():
    df = load_segments()
    if df is None or df.empty:
        return {"message": "No segmentation result available."}
    return {
        "total_customers": int(df["customer_id"].nunique()),
        "segments": df.to_dict(orient="records"),
    }
