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
    return supabase.table("startups").insert({"source_url": url, "raw_text": raw_text}).execute()
