from supabase import create_client, Client
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class Startup(BaseModel):
    id: str | None = None
    source_url: str | None = None
    raw_text: str | None = None
    name: str | None = None
    description: str | None = None
    founded: str | None = None
    location: str | None = None
    sector: str | None = None
    stage: str | None = None
    founders: list[str] | None = None
    traction_signals: list[str] | None = None
    embedding: list[float] | None = None
    best_fitting_vc: str | None = None
    confidence: float | None = None
    created_at: str | None = None

# ===============================
# Queries
# ===============================
def insert_startup_data(url: str, raw_text: str, data: Startup):
    return supabase.table("startups").upsert(
        {
            "source_url": url,
            "raw_text": raw_text,
            "name": data.name,
            "description": data.description,
            "founded": data.founded,
            "location": data.location,
            "sector": data.sector,
            "stage": data.stage,
            "founders": data.founders,
            "traction_signals": data.traction_signals,
            "embedding": data.embedding,
            "best_fitting_vc": data.best_fitting_vc,
            "confidence": data.confidence,
        },
        on_conflict="source_url"
    ).execute()

def get_all_startup_urls() -> list[str]:
    result = supabase.table("startups").select("source_url").order("created_at", desc=True).execute()
    return [row["source_url"] for row in result.data]

def get_all_startup_data() -> list[Startup]:
    result = supabase.table("startups").select("*").execute()
    return [Startup(**row) for row in result.data]

def update_startup_vc_match(startup_id: str, vc_name: str, confidence: float):
    return supabase.table("startups").update(
        {"best_fitting_vc": vc_name, "confidence": confidence}
    ).eq("id", startup_id).execute()

def get_startup_data(id: str) -> Startup:
    result = supabase.table("startups").select("*").eq("id", id).execute()
    return Startup(**result.data[0])