from api.v1.data_access.supabase import Startup
from api.v1.services import startups
from fastapi import APIRouter
from pydantic import BaseModel
    
router = APIRouter()

class StartupsResponse(BaseModel):
    startups: list[Startup]

class StartupResponse(BaseModel):
    startup: Startup

@router.get("/startups")
def get_startups():
    return StartupsResponse(startups=startups.get_all_startups())

@router.get("/startups/{id}")
def get_startup(id: str):
    return StartupResponse(startup=startups.get_startup(id))