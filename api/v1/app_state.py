import faiss

funds_index: faiss.Index | None = None
funds_metadata: list[str] | None = None


def initialize(index: faiss.Index, metadata: list[str]) -> None:
    global funds_index, funds_metadata
    funds_index = index
    funds_metadata = metadata
