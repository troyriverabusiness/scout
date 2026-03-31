from api.v1.services.outreach import generate_outreach
from fastapi import APIRouter
from pydantic import BaseModel
from api.v1.data_access.supabase import Startup

router = APIRouter()

class OutreachRequest(BaseModel):
    startup: Startup
    target: str

class OutreachResponse(BaseModel):
    outreach: str

@router.post("/outreach")
def outreach(request: OutreachRequest):
    outreach_text = generate_outreach(request.startup, request.target)
    return OutreachResponse(outreach=outreach_text)