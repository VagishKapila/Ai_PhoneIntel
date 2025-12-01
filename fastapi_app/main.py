# backend/fastapi_app/main.py

from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# SERVICES
from fastapi_app.services.job_manager import init_job, start_background_job

# ROUTERS
from fastapi_app.api.upload import router as upload_router
from fastapi_app.api.voice import router as voice_router
from fastapi_app.api.jobs import router as jobs_router
from fastapi_app.api.contractors_ai import router as contractors_ai_router

app = FastAPI(title="AI Project Assistant API")

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROOT CHECK
# -----------------------------
@app.get("/")
def root():
    return {"message": "AI Project Assistant API running."}

# -----------------------------
# STEP A — Describe Work
# -----------------------------
@app.post("/describe")
async def describe_work(
    description: str = Form(...),
    background_tasks: BackgroundTasks = None,
):
    # 1. create job folder + metadata.json
    job_id = init_job(description)

    # 2. queue background AI warmup
    start_background_job(job_id)

    return {
        "job_id": job_id,
        "message": "Description received. AI preprocessing started."
    }

# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(upload_router, prefix="/files")
app.include_router(voice_router, prefix="/voice")
app.include_router(jobs_router, prefix="/jobs")

# USE ONLY THE AI CONTRACTOR SEARCH
app.include_router(contractors_ai_router, prefix="/contractors-ai")