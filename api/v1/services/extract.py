from api.v1.data_access import firecrawl, supabase, openai

def extract_and_save_startup_data(url: str):
    markdown = firecrawl.scrape(url)

    data = openai.extract_startup_data(markdown)
    supabase.insert_startup_data(url, markdown, data)

    return data

def enrich_startup_data():
    startups = supabase.get_all_startup_data()
    for startup in startups:
        data = openai.extract_startup_data(startup.raw_text)
        supabase.insert_startup_data(startup.source_url, startup.raw_text, data)
