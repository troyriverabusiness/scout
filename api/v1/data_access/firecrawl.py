from firecrawl import Firecrawl
from dotenv import load_dotenv
import os

load_dotenv()

app = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

# ===============================
# Endpoints
# ===============================
def scrape(url: str) -> str:
    result = app.scrape(url)
    return result.markdown