from langfuse import observe
from api.v1.data_access import firecrawl, supabase, openai, langfuse

@observe(name="extract_and_save_startup_data")
def extract_and_save_startup_data(url: str):
    # Scrape for raw Markdown
    markdown = firecrawl.scrape(url)

    # Extract structured startup data and score the extraction span
    data = openai.extract_startup_data(markdown)
    langfuse.create_scores(data)

    supabase.insert_startup_data(url, markdown, data)

    return markdown
