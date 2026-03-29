from firecrawl import Firecrawl
from langfuse import observe
from dotenv import load_dotenv
import os

load_dotenv()

app = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

# ===============================
# Endpoints
# ===============================
@observe(name="firecrawl_scrape", as_type="span")
def scrape(url: str) -> str:
    result = app.scrape(url)
    return result.markdown