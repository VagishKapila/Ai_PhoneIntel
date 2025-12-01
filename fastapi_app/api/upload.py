# backend/fastapi_app/api/upload.py

from fastapi import APIRouter, UploadFile, File, Form
import os
import uuid

from fastapi_app.utils.path_config import (
    job_uploads_path
)

router = APIRouter()


@router.post("/upload")
async def upload_files(
    job_id: str = Form(...),
    files: list[UploadFile] = File(...)
):

    uploads_dir = job_uploads_path(job_id)
    os.makedirs(uploads_dir, exist_ok=True)

    saved_files = []

    for file in files:
        ext = file.filename.split(".")[-1]
        new_name = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(uploads_dir, new_name)

        with open(save_path, "wb") as f:
            f.write(await file.read())

        saved_files.append({
            "original": file.filename,
            "stored_as": new_name,
            "path": save_path
        })

    return {
        "job_id": job_id,
        "count": len(saved_files),
        "files": saved_files,
        "message": "Files uploaded successfully."
    }