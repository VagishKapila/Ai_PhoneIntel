# backend/fastapi_app/services/contractor_ai_service.py

import os
import json
import math
from sentence_transformers import SentenceTransformer, util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JOBS_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../shared/jobs"))

MODEL = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------------------------------
# Dummy contractor DB (expand later)
# -------------------------------------------------------
CONTRACTORS_DB = [
    {
        "id": "c1",
        "name": "Bay Area Trenching & Utilities",
        "trade": "trenching",
        "specialties": ["trenching", "underground utilities", "backfill"],
        "experience": 22,
        "rating": 4.8,
        "phone": "408-555-1100",
        "location": {"lat": 37.3382, "lng": -121.8863, "address": "San Jose, CA"}
    },
    {
        "id": "c2",
        "name": "Precision Concrete & Sitework",
        "trade": "concrete",
        "specialties": ["flatwork", "foundations", "demo & haul"],
        "experience": 17,
        "rating": 4.5,
        "phone": "650-555-2222",
        "location": {"lat": 37.4419, "lng": -122.143, "address": "Palo Alto, CA"}
    },
    {
        "id": "c3",
        "name": "General Bob's Construction",
        "trade": "general",
        "specialties": ["general contracting", "carpentry", "remodeling"],
        "experience": 30,
        "rating": 4.1,
        "phone": "510-555-9090",
        "location": {"lat": 37.4419, "lng": -122.143, "address": "Palo Alto, CA"}
    }
]


# -------------------------------------------------------
# Utility: Load job description embedding
# -------------------------------------------------------
def load_job_embedding(job_id):
    emb_path = os.path.join(JOBS_ROOT, job_id, "embedding.json")
    if not os.path.exists(emb_path):
        raise Exception(f"Missing embedding.json for job {job_id}")

    with open(emb_path) as f:
        data = json.load(f)
    return data["embedding"]


# -------------------------------------------------------
# Fusion Scoring Logic
# -------------------------------------------------------
def compute_fusion_score(similarity, rating, experience, trade_match):
    # Normalize
    rating_norm = rating / 5
    experience_norm = min(experience / 30, 1)

    trade_bonus = 1 if trade_match else 0

    score = (
        similarity * 0.65 +
        rating_norm * 0.20 +
        experience_norm * 0.10 +
        trade_bonus * 0.05
    )

    return round(score * 100, 2)


# -------------------------------------------------------
# Main search logic
# -------------------------------------------------------
def search_contractors(job_id, radius):
    job_embedding = load_job_embedding(job_id)
    job_embedding_tensor = MODEL.encode(job_embedding) if isinstance(job_embedding, str) else job_embedding

    results = []

    for contractor in CONTRACTORS_DB:

        contractor_text = (
            contractor["trade"] + " " +
            " ".join(contractor["specialties"])
        )
        contractor_emb = MODEL.encode(contractor_text)

        similarity = float(util.cos_sim(job_embedding_tensor, contractor_emb))

        trade_match = contractor["trade"] in contractor_text.lower()

        score = compute_fusion_score(
            similarity,
            contractor["rating"],
            contractor["experience"],
            trade_match
        )

        contractor_result = contractor.copy()
        contractor_result["score"] = score

        results.append(contractor_result)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results
    