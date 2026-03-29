# Aboutme: Scrapes startup urls from different sources
import re
from langfuse import observe
from api.v1.data_access import supabase, firecrawl
from api.v1.services import extract_and_save_startup_data

@observe(name="batch_scrape_companies")
def batch_scrape_companies():
    urls = get_new_company_urls()

    for url in urls:
        extract_and_save_startup_data(url)

def get_new_company_urls() -> list[str]:
    existing_urls = supabase.get_all_startup_urls()
    urls = []

    # Scrape sources
    yc_urls = scrape_yc()
    urls.extend(yc_urls)

    new_urls = dedupe(urls, existing_urls)
    return new_urls

# Ensure only new urls are scraped (save firecrawl credits)
def dedupe(urls: list[str], existing_urls: list[str]) -> list[str]:
    seen = set()
    result = []
    for url in urls:
        if url not in existing_urls and url not in seen:
            seen.add(url)
            result.append(url)
    return result

# Scrape links of YC companies (default is Winter 2026)
def scrape_yc(batch: str = "Winter%202026") -> list[str]:
    url = f"https://www.ycombinator.com/companies?batch={batch}"

    markdown = firecrawl.scrape(url)

    # Extract YC company page URLs from markdown links
    links = re.findall(r'\[.*?\]\((https://www\.ycombinator\.com/companies/[^)]+)\)', markdown)

    return links
