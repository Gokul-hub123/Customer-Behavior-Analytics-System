from __future__ import annotations

from fastapi import APIRouter, HTTPException, UploadFile, File

from backend.config import DATA_DIR
from backend.database import save_current_dataset
from backend.services.data_processing import build_standard_dataset

router = APIRouter()


@router.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_path = DATA_DIR / file.filename
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

    file_path.write_bytes(content)

    import pandas as pd
    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid CSV file.") from exc

    if df.empty:
        raise HTTPException(status_code=400, detail="The CSV file contains no data rows.")

    try:
        cleaned_df = build_standard_dataset(df)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    save_current_dataset(cleaned_df)

    return {
        "message": "Dataset uploaded successfully",
        "file_name": file.filename,
        "rows": len(cleaned_df),
        "columns": list(cleaned_df.columns),
        "preview": cleaned_df.head(10).to_dict(orient="records"),
    }
