# backend/fastapi_app/api/ai_tasks.py

import uuid

# Temporary in-memory store
JOB_STATUS = {}

def start_job(description: str):
    job_id = str(uuid.uuid4())
    JOB_STATUS[job_id] = {
        "description": description,
        "status": "processing",
        "progress": 5,
    }
    return job_id

def get_job_status(job_id: str):
    return JOB_STATUS.get(job_id, {"error": "Job not found"})