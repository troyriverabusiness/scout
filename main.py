from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.routes.extract import router as extract_router
from api.v1.services.embedding import get_or_create_funds_index
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    # TODO: decide whether to keep the funds index in memory or query Supabase at search time
    app.state.funds_index, app.state.funds_metadata = await loop.run_in_executor(None, get_or_create_funds_index)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(extract_router)

@app.get("/")
def read_root():
    return {"message": "Hello from scout!"}


