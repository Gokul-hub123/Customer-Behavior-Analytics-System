from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.config import DATA_DIR
from backend.database import load_cleaned_dataset, load_current_dataset, save_current_dataset, store_dataset_in_db
from backend.services.data_processing import build_standard_dataset

router = APIRouter()


@router.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

    file_path = DATA_DIR / file.filename
    file_path.write_bytes(content)

    import pandas as pd

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid CSV file.") from exc

    if df.empty:
        raise HTTPException(status_code=400, detail="The CSV file contains no data rows.")

    try:
        standard_df = build_standard_dataset(df)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    save_current_dataset(standard_df)
    store_dataset_in_db(standard_df)

    preview = standard_df.head(10).to_dict(orient="records")
    return {
        "message": "Dataset uploaded successfully",
        "file_name": file.filename,
        "rows": int(len(standard_df)),
        "columns": list(standard_df.columns),
        "preview": preview,
    }


@router.get("/api/data-preview")
async def data_preview():
    df = load_cleaned_dataset() if load_cleaned_dataset() is not None else load_current_dataset()
    if df is None:
        return {"message": "No dataset uploaded yet."}
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "preview": df.head(10).to_dict(orient="records"),
    }
