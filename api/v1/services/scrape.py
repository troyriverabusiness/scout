# Aboutme: Scrapes startup urls from different sources
from api.v1.services.extract import extract_and_save_startup_data
from langfuse import observe
from api.v1.data_access import supabase, firecrawl, openai


@observe(name="batch_scrape_companies")
def batch_scrape_companies():
    new_links = get_new_company_links()

    # Scrape new links, extract and save startup data
    for link in new_links:
        extract_and_save_startup_data(link)

def get_new_company_links() -> list[str]:
    # Get existing urls (from Supabase)
    existing_urls = supabase.get_all_startup_urls()

    # Scrape YC companies
    yc_companies = scrape_yc()
    yc_links = [company.url for company in yc_companies]

    # Filter out existing urls - list[str]
    new_links = dedupe(yc_links, existing_urls)

def dedupe(urls: list[str], existing_urls: list[str]) -> list[str]:
    seen = set()
    result = []
    for url in urls:
        if url not in existing_urls and url not in seen:
            seen.add(url)
            result.append(url)
    return result

# Scrape links of YC companies (default is Winter 2026)
def scrape_yc(batch: str = "Winter%202026") -> list[supabase.CompanyLink]:
    url = f"https://www.ycombinator.com/companies?batch={batch}"

    markdown = firecrawl.scrape(url)

    # Extract links using LLM
    links = openai.extract_links(markdown)

    return links
