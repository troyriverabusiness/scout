from fastapi import Request
import faiss


# TODO: add a get_funds_index() dependency here if routes need direct access to the FAISS index
def get_funds_index(request: Request) -> tuple[faiss.Index, list[str]]:
    return request.app.state.funds_index, request.app.state.funds_metadata
