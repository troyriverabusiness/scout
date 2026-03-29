from api.v1.data_access import firecrawl, supabase

def extract_and_save_startup_data(url: str):
    # Scrape the url using firecrawl 
    markdown = firecrawl.scrape(url)

    # Insert the raw text into supabase
    supabase.insert_startup_raw_text(url, markdown)

    return markdown