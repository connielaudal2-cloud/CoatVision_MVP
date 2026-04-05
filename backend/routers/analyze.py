# backend/routers/analyze.py
import logging
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os

from core.coatvision_core import process_image_file, analyze_coating

router = APIRouter(prefix="/api/analyze", tags=["analyze"])


def _persist_analysis(filename: str, metrics: dict) -> None:
    """Persist an analysis result to Supabase (non-fatal on failure)."""
    try:
        from app.services.supabase_client import insert_analysis_payload
        payload = {
            "id": str(uuid.uuid4()),
            "original_filename": filename,
            "output_filename": None,
            "metrics": metrics,
            "status": "completed",
        }
        insert_analysis_payload(payload)
    except Exception as exc:
        logging.warning("Supabase persist skipped: %s", exc)


@router.post("/")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an uploaded image for coating quality.
    Returns CVI, CQI, coverage and other metrics.
    """
    # Create temp directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded file
        temp_path = os.path.join(temp_dir, file.filename or "upload.jpg")
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)

        try:
            # Run analysis
            metrics = process_image_file(temp_path, temp_dir)
            _persist_analysis(file.filename or "upload", metrics)
            return {
                "status": "success",
                "filename": file.filename,
                "metrics": metrics
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.post("/base64")
async def analyze_base64(payload: dict):
    """
    Analyze a base64-encoded image.
    Expects {"image": "<base64_string>"}
    """
    from core.coatvision_core import decode_base64_image

    image_data = payload.get("image")
    if not image_data:
        raise HTTPException(status_code=400, detail="Missing 'image' field")

    try:
        image = decode_base64_image(image_data)
        metrics = analyze_coating(image)
        _persist_analysis(payload.get("filename", "base64_upload"), metrics)
        return {
            "status": "success",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
