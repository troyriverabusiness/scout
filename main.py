from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.routes import extract_router, startups_router, outreach_router
from api.v1.services.embedding import get_or_create_funds_index
from api.v1 import app_state
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    # TODO: decide whether to keep the funds index in memory or query Supabase at search time
    index, metadata = await loop.run_in_executor(None, get_or_create_funds_index)
    app_state.initialize(index, metadata)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(extract_router)
app.include_router(startups_router)
app.include_router(outreach_router)

@app.get("/")
def read_root():
    return {"message": "Hello from scout!"}


