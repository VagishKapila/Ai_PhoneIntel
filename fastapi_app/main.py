# backend/fastapi_app/main.py

from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# SERVICES
from fastapi_app.services.job_manager import init_job, start_background_job

# ROUTERS
from fastapi_app.api.upload import router as upload_router
from fastapi_app.api.voice import router as voice_router
from fastapi_app.jobs.router import router as jobs_router
from fastapi_app.api.contractors_ai import router as contractors_ai_router


# ---------------------------------------------------
# DEFINE APP FIRST (ONLY ONCE)
# ---------------------------------------------------
app = FastAPI(title="AI Project Assistant API")


# ---------------------------------------------------
# ENABLE CORS (AFTER app is created)
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # ← allow everything (React, CodeSandbox, Railway, Cloudflare)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# ROOT CHECK
# ---------------------------------------------------
@app.get("/")
def root():
    return {"message": "AI Project Assistant API running."}


# ---------------------------------------------------
# Step A — Describe Work → Create job + warmup
# ---------------------------------------------------
@app.post("/describe")
async def describe_work(
    description: str = Form(...),
    background_tasks: BackgroundTasks = None,
):
    # create job metadata
    job_id = init_job(description)

    # start async background job
    start_background_job(job_id)

    return {
        "job_id": job_id,
        "message": "Description received. AI preprocessing started."
    }


# ---------------------------------------------------
# ROUTERS
# ---------------------------------------------------
app.include_router(upload_router, prefix="/files")
app.include_router(voice_router, prefix="/voice")
app.include_router(jobs_router, prefix="/jobs")
app.include_router(contractors_ai_router, prefix="/contractors-ai")
