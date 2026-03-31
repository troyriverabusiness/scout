from langfuse import get_client
from api.v1.data_access.supabase import Startup


EXTRACT_STARTUP_PROMPT_NAME = "extract-startup"
EXTRACT_LINK_PROMPT_NAME = "extract-links"

OUTREACH_FOUNDER_PROMPT_NAME = "outreach-founder"
OUTREACH_VC_PROMPT_NAME = "outreach-vc"

# ===============================
# Functions 
# ===============================
def create_scores(data: Startup):
    completeness = calculate_extracted_fields_score(data)

    get_client().score_current_span(
        name="fields_completeness",
        value=completeness,
    )

def calculate_extracted_fields_score(data: Startup) -> float:
    fields = [
        data.name,
        data.description,
        data.founded,
        data.location,
        data.sector,
        data.stage,
        data.founders,
        data.traction_signals,
    ]

    filled = sum(1 for f in fields if f and f != [] and f != "")
    return round(filled / len(fields), 2)

def get_outreach_prompt(name: str):
    prompt = get_client().get_prompt(name=name)
    return prompt.compile(), prompt

def get_startup_extraction_prompt(markdown: str):
    prompt = get_client().get_prompt(name=EXTRACT_STARTUP_PROMPT_NAME)
    return prompt.compile(markdown=markdown), prompt

def get_link_extraction_prompt(markdown: str):
    prompt = get_client().get_prompt(name=EXTRACT_LINK_PROMPT_NAME)
    return prompt.compile(markdown=markdown), prompt
