import threading
import json
import uuid
from pathlib import Path
from fastapi_app.worker.job_worker import run_job_pipeline


# Job folder: shared/jobs/<job_id>
JOBS_ROOT = Path(__file__).resolve().parents[1] / "shared" / "jobs"


def init_job(description: str):
    """Create job folder + metadata.json"""
    job_id = uuid.uuid4().hex
    job_dir = JOBS_ROOT / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "job_id": job_id,
        "description": description,
        "status": "starting",
        "progress": 0,
        "messages": [],
        "results": None
    }

    with open(job_dir / "metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

    return job_id


def start_background_job(job_id: str):
    """Start the async pipeline worker thread."""
    t = threading.Thread(target=run_job_pipeline, args=(job_id,), daemon=True)
    t.start()