import json
import time
from pathlib import Path

JOBS_ROOT = Path(__file__).resolve().parents[1] / "shared" / "jobs"


def update_progress(job_id, status=None, progress=None, msg=None, results=None):
    """Update metadata.json inside the job folder."""
    job_dir = JOBS_ROOT / job_id
    meta_path = job_dir / "metadata.json"

    if not meta_path.exists():
        raise Exception(f"metadata.json missing for job {job_id}")

    with open(meta_path, "r") as f:
        meta = json.load(f)

    if status is not None:
        meta["status"] = status

    if progress is not None:
        meta["progress"] = progress

    if msg:
        meta.setdefault("messages", []).append(msg)
        meta["message"] = msg  # <- LIVE message for StepRunning

    if results is not None:
        meta["results"] = results

    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)


def run_job_pipeline(job_id):
    """Simulated multi-stage pipeline. Later replaced with real AI intelligence."""
    try:
        update_progress(job_id, status="starting", progress=5,
                        msg="Initializing AI engine…")
        time.sleep(0.8)

        update_progress(job_id, status="analyzing", progress=30,
                        msg="Analyzing description…")
        time.sleep(1.0)

        update_progress(job_id, status="processing_files", progress=55,
                        msg="Processing drawings & PDFs…")
        time.sleep(1.2)

        update_progress(job_id, status="matching_contractors", progress=75,
                        msg="Running contractor suitability…")
        time.sleep(0.9)

        update_progress(
            job_id,
            status="completed",
            progress=100,
            msg="Analysis complete.",
            results={"summary": "AI pipeline finished successfully."}
        )

    except Exception as e:
        update_progress(job_id, status="error", msg=str(e))