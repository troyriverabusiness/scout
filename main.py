from fastapi import FastAPI, APIRouter
from api.v1.routes.extract import router as extract_router

app = FastAPI()

app.include_router(extract_router)

@app.get("/")
def read_root():
    return {"message": "Hello from scout!"}


