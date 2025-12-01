from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()

JOBS_ROOT = Path(__file__).resolve().parents[1] / "shared" / "jobs"

@router.get("/{job_id}")
def get_job_status(job_id: str):
    meta_path = JOBS_ROOT / job_id / "metadata.json"

    if not meta_path.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    with open(meta_path, "r") as f:
        meta = json.load(f)

    return meta