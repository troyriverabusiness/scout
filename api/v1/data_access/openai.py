from dotenv import load_dotenv
import os

load_dotenv()

from langfuse.openai import openai
import instructor
from api.v1.data_access.supabase import Startup, CompanyLink
from api.v1.data_access.langfuse import get_link_extraction_prompt, get_startup_extraction_prompt

client = instructor.from_openai(openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# Uses langfuse versioned prompts
def extract_startup_data(markdown: str) -> Startup:
    content, prompt = get_startup_extraction_prompt(markdown)
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=Startup,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        langfuse_prompt=prompt,
    )


def extract_links(markdown: str) -> list[CompanyLink]:
    content, prompt = get_link_extraction_prompt(markdown)
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=list[CompanyLink],
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        langfuse_prompt=prompt,
    )