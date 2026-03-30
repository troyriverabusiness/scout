from dotenv import load_dotenv
load_dotenv()
from langfuse.openai import openai

MODEL_NAME = "text-embedding-3-small"

_client: openai.OpenAI | None = None


def _get_client() -> openai.OpenAI:
    global _client
    if _client is None:
        _client = openai.OpenAI()
    return _client


def create_embedding(text: str) -> list[float]:
    response = _get_client().embeddings.create(input=text, model=MODEL_NAME)
    return response.data[0].embedding
