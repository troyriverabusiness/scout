from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-base"


def load_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def create_embedding(model: SentenceTransformer, text: str) -> list[float]:
    return model.encode(text).tolist()

