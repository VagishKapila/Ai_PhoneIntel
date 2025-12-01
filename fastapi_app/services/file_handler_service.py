from pathlib import Path

async def save_job_file(upload: "UploadFile"):
    JOBS_DIR = Path("shared/jobs")
    JOBS_DIR.mkdir(parents=True, exist_ok=True)

    dest = JOBS_DIR / upload.filename
    with open(dest, "wb") as f:
        f.write(await upload.read())

    return str(dest)