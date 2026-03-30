from fastapi import Request
import faiss


def get_funds_index(request: Request) -> tuple[faiss.Index, list[str]]:
    return request.app.state.funds_index, request.app.state.funds_metadata
