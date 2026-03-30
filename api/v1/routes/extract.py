from api.v1.services import extract_and_save_startup_data, batch_scrape_companies
from api.v1.dependencies import get_model
from fastapi import APIRouter, Depends
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

class ExtractRequest(BaseModel):
    url: str

class ExtractResponse(BaseModel):
    markdown: str

router = APIRouter()

@router.post("/extract")
def extract(request: ExtractRequest, model: SentenceTransformer = Depends(get_model)):
    markdown = extract_and_save_startup_data(request.url, model)
    return ExtractResponse(markdown=markdown)

@router.post("/scrape")
def scrape():
    batch_scrape_companies()
