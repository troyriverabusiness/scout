from api.v1.services import extract_and_save_startup_data, batch_scrape_companies
from fastapi import APIRouter
from pydantic import BaseModel

class ExtractRequest(BaseModel):
    url: str

class ExtractResponse(BaseModel):
    markdown: str

router = APIRouter()

@router.post("/extract")
def extract(request: ExtractRequest):
    markdown = extract_and_save_startup_data(request.url)
    return ExtractResponse(markdown=markdown)

@router.post("/scrape")
def scrape():
    batch_scrape_companies()
