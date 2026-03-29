from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# ===============================
# Queries
# ===============================
def insert_startup_raw_text(url: str, raw_text: str):
    return supabase.table("startups").upsert({"source_url": url, "raw_text": raw_text}, on_conflict="source_url").execute()

def get_all_startup_urls() -> list[str]:
    result = supabase.table("startups").select("source_url").execute()
    return [row["source_url"] for row in result.data]