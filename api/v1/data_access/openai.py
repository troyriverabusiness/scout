from dotenv import load_dotenv
import os

load_dotenv()

from langfuse.openai import openai
import instructor
from api.v1.data_access.supabase import Startup, CompanyLink
from api.v1.data_access.langfuse import get_link_extraction_prompt, get_startup_extraction_prompt

raw_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = instructor.from_openai(raw_client)

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


def create_message(system_prompt: str, langfuse_prompt_ref, startup_text: str) -> str:
    response = raw_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": startup_text},
        ],
        langfuse_prompt=langfuse_prompt_ref,
    )
    return response.choices[0].message.content
