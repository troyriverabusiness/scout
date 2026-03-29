from dotenv import load_dotenv
import os

load_dotenv()

from langfuse.openai import openai
import instructor
from api.v1.data_access.supabase import Startup

client = instructor.from_openai(openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

def extract_startup_data(markdown: str) -> Startup:
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=Startup,
        messages=[
            {
                "role": "user",
                "content": f"Extract structured startup information from the following content:\n\n{markdown}",
            }
        ],
    )