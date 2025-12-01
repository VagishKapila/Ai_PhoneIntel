# backend/fastapi_app/services/job_status_store.py

import os
import json
import threading
from typing import List, Dict

# GLOBAL LOCK (Thread-Safe)
_lock = threading.Lock()

# STATUS FILE NAME
STATUS_FILE = "status.json"


# -----------------------------
# UTILITY — LOAD / SAVE
# -----------------------------
def _load(path: str) -> dict:
    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)


def _save(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# INIT STATUS FOR NEW JOB
# -----------------------------
def init_status(job_id: str, jobs_root: str = None):
    job_dir = jobs_root if jobs_root else _default_job_dir(job_id)
    status_path = os.path.join(job_dir, STATUS_FILE)

    with _lock:
        data = {
            "job_id": job_id,
            "status": "initialized",
            "steps": [],
            "progress": 0
        }
        _save(status_path, data)


# -----------------------------
# UPDATE STATUS FIELD
# -----------------------------
def set_status(job_id: str, value: str):
    job_dir = _default_job_dir(job_id)
    status_path = os.path.join(job_dir, STATUS_FILE)

    with _lock:
        data = _load(status_path)
        data["status"] = value
        _save(status_path, data)


# -----------------------------
# ADD A STEP (DONE/NOT DONE)
# -----------------------------
def add_step(job_id: str, label: str, done: bool):
    job_dir = _default_job_dir(job_id)
    status_path = os.path.join(job_dir, STATUS_FILE)

    with _lock:
        data = _load(status_path)
        data.setdefault("steps", [])

        data["steps"].append({
            "label": label,
            "done": done
        })

        # auto-calc progress
        total = len(data["steps"])
        completed = len([s for s in data["steps"] if s["done"]])
        data["progress"] = round((completed / total) * 100, 1)

        _save(status_path, data)


# -----------------------------
# FETCH STATUS (USED BY UI)
# -----------------------------
def get_status(job_id: str):
    job_dir = _default_job_dir(job_id)
    status_path = os.path.join(job_dir, STATUS_FILE)

    if not os.path.exists(status_path):
        return {"error": "job not found", "job_id": job_id}

    return _load(status_path)


# -----------------------------
# INTERNAL: GET ACTUAL JOB PATH
# -----------------------------
def _default_job_dir(job_id: str) -> str:
    base = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../shared/jobs")
    )
    return os.path.join(base, job_id)