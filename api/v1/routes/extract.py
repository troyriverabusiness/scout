from api.v1.services import extract_and_save_startup_data, batch_scrape_companies
from api.v1.dependencies import get_funds_index
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
import faiss

class ExtractRequest(BaseModel):
    url: str

class ExtractResponse(BaseModel):
    markdown: str

router = APIRouter()

@router.post("/extract")
def extract(request: Request, body: ExtractRequest, funds: tuple[faiss.Index, list[str]] = Depends(get_funds_index)):
    funds_index, funds_metadata = funds
    markdown = extract_and_save_startup_data(body.url, funds_index, funds_metadata)
    return ExtractResponse(markdown=markdown)

@router.post("/scrape")
def scrape():
    batch_scrape_companies()
