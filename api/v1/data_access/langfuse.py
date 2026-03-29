from langfuse import Langfuse
from api.v1.data_access.supabase import Startup

import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    base_url=os.getenv("LANGFUSE_BASE_URL")
)

# ===============================
# Functions 
# ===============================
def create_scores(trace_id: str, value: float):
    langfuse.create_score(
        name="fields_completeness",
        value=value,
        trace_id=trace_id,
    )



def calculate_startup_fields_completeness(data: Startup) -> float:
    fields = [
        profile.name,
        profile.location,
        profile.sector,
        profile.stage,
        profile.one_liner,
        profile.description,
        profile.website,
        profile.founders,  # non-empty list
    ]
    
    filled = sum(1 for f in fields if f and f != [] and f != "")
    return round(filled / len(fields), 2)