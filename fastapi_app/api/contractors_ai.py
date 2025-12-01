# backend/fastapi_app/api/contractors_ai.py

from fastapi import APIRouter, Form, HTTPException
from fastapi_app.services.contractor_ai_service import search_contractors

router = APIRouter()

@router.post("/search")
def contractors_search(
    job_id: str = Form(...),
    radius: int = Form(25)
):
    """
    Advanced AI contractor search
    """
    try:
        results = search_contractors(job_id, radius)
        return {
            "job_id": job_id,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))