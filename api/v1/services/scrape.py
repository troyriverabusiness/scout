# Aboutme: Scrapes startup urls from different sources
import re
from api.v1.data_access import supabase, firecrawl
from api.v1.services import extract_and_save_startup_data

# Get chunk of new company data from multiple sources
def scrape_sources():
    urls = []
    # Scrape YC
    urls.extend(scrape_yc())

    # Deduplicate the urls
    new_urls = dedupe(urls)

    for url in new_urls:
        extract_and_save_startup_data(url)


# Ensure only new urls are scraped (save firecrawl credits)
def dedupe(urls: list[str]) -> list[str]:
    existing_urls = set(supabase.get_all_startup_urls())
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
