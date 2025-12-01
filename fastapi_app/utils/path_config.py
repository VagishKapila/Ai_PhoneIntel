# backend/fastapi_app/utils/path_config.py

import os

# Absolute path to the project root (folder containing backend and shared)
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

# /shared
SHARED_ROOT = os.path.join(PROJECT_ROOT, "shared")
os.makedirs(SHARED_ROOT, exist_ok=True)

# /shared/jobs
JOBS_ROOT = os.path.join(SHARED_ROOT, "jobs")
os.makedirs(JOBS_ROOT, exist_ok=True)


def job_path(job_id: str):
    """Return absolute path to a job folder."""
    return os.path.join(JOBS_ROOT, job_id)


def job_uploads_path(job_id: str):
    """Return absolute path to job uploads folder."""
    return os.path.join(JOBS_ROOT, job_id, "uploads")