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
    name: str
    description: str
    founded: str
    location: str
    sector: str
    stage: str
    founders: list[str]
    traction_signals: list[str]

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
        },
        on_conflict="source_url"
    ).execute()

def get_all_startup_urls() -> list[str]:
    result = supabase.table("startups").select("source_url").execute()
    return [row["source_url"] for row in result.data]

def get_all_startup_data() -> list[Startup]:
    result = supabase.table("startups").select("*").execute()
    return [Startup(**row) for row in result.data]