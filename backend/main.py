from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.database import read_uploaded_csv, save_uploaded_dataset, validate_uploaded_file
from backend.services.analytics import get_dashboard_data, get_eda_data
from backend.services.data_processing import build_standard_dataset, clean_dataset, cleaning_summary
from backend.services.forecasting import run_forecast
from backend.services.segmentation import run_customer_segmentation

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    validate_uploaded_file(file_location)
    df = read_uploaded_csv(file_location)
    try:
        df = build_standard_dataset(df)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    save_uploaded_dataset(file_location, df)
    return {
        "message": "Dataset uploaded successfully",
        "file_name": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head(10).to_dict(orient="records"),
    }


@router.get("/dashboard")
async def dashboard_data():
    return {"message": "Dashboard module ready."}


@router.get("/cleaning-summary")
async def cleaning_summary_api():
    return {"message": "Cleaning summary will be generated after upload."}


@router.get("/analysis")
async def analysis_data():
    return {"message": "Analysis module ready."}


@router.get("/segments")
async def get_segments():
    return {"message": "Customer segments will appear after segmentation."}


@router.get("/forecast")
async def get_forecast():
    return {"message": "Forecast output will be generated after forecasting."}


@router.get("/report")
async def get_report():
    return {"message": "Report module ready."}
