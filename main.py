from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.routes.extract import router as extract_router
from api.v1.data_access.embeddings import load_model
from api.v1.services.embedding import create_funds_index
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    app.state.model = await loop.run_in_executor(None, load_model)
    app.state.funds_index, app.state.funds_metadata = await loop.run_in_executor(None, create_funds_index, app.state.model)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(extract_router)

@app.get("/")
def read_root():
    return {"message": "Hello from scout!"}


