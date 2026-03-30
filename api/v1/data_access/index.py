# Aboutme: 
# File creates indexes, searches indexes, and saves indexes to disk
import numpy as np
import faiss
import pickle
from pathlib import Path

DATA_DIR = Path("data")


def create_index(embeddings: list[list[float]], metadata: list[str], filename: str) -> tuple[faiss.Index, list[str]]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    matrix = np.array(embeddings, dtype=np.float32)
    index = faiss.IndexFlatIP(len(matrix[0]))
    index.add(matrix)

    faiss.write_index(index, str(DATA_DIR / f"{filename}.index"))
    with open(DATA_DIR / f"{filename}.metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    return index, metadata


def load_index(filename: str) -> tuple[faiss.Index, list[str]]:
    index = faiss.read_index(str(DATA_DIR / f"{filename}.index"))
    with open(DATA_DIR / f"{filename}.metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    return index, metadata