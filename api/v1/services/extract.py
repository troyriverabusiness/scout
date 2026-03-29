import asyncio
from langfuse import observe
from api.v1.data_access import firecrawl, supabase, openai, langfuse

@observe(name="extract_and_save_startup_data")
def extract_and_save_startup_data(url: str):
    trace_id = langfuse.start_trace(name="extract_and_save_startup_data", metadata={"url": url})

    markdown = firecrawl.scrape(url)

    data = openai.extract_startup_data(markdown)

    # Calculate trace scores
    completeness = langfuse.calculate_startup_fields_completeness(data)

    langfuse.create_scores(trace_id, completeness)

    supabase.insert_startup_data(url, markdown, data)

    langfuse.end_trace(trace_id)

    return markdown

@observe(name="enrich_startup_data")
async def enrich_startup_data():
    startups = supabase.get_all_startup_data()
    for i, startup in enumerate(startups):
        data = openai.extract_startup_data(startup.raw_text)
        supabase.insert_startup_data(startup.source_url, startup.raw_text, data)
        if i < len(startups) - 1:
            await asyncio.sleep(20)
