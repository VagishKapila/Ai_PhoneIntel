import uuid
import json
from pathlib import Path

JOBS_DIR = Path("shared/jobs")

def start_job(description: str):
    job_id = str(uuid.uuid4())
    JOBS_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "job_id": job_id,
        "description": description,
        "status": "received"
    }

    with open(JOBS_DIR / f"{job_id}.json", "w") as f:
        json.dump(payload, f)

    return job_id


def get_job_status(job_id: str):
    file = JOBS_DIR / f"{job_id}.json"
    if not file.exists():
        return {"error": "Job not found"}

    return json.load(open(file))