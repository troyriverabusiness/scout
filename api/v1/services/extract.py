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

@observe(name="extract_and_score_startup")
def _extract_and_score_startup(raw_text: str):
    data = openai.extract_startup_data(raw_text)
    langfuse.create_scores(data)
    return data

@observe(name="enrich_startup_data")
def enrich_startup_data():
    startups = supabase.get_all_startup_data()

    for startup in startups:
        data = _extract_and_score_startup(startup.raw_text)
        supabase.insert_startup_data(startup.source_url, startup.raw_text, data)
