from api.v1.services import embedding
from langfuse import observe
from api.v1.data_access import firecrawl, supabase, openai, langfuse

@observe(name="extract_and_save_startup_data")
def extract_and_save_startup_data(url: str):
    markdown = firecrawl.scrape(url)
    data = openai.extract_startup_data(markdown)
    langfuse.create_scores(data)
    data.embedding = embedding.get_startup_embedding(data)
    # TODO: call get_embeddings() here once lookup_fund_name() is implemented,
    # so best_fit_fund and score are stored alongside the startup record
    supabase.insert_startup_data(url, markdown, data)
    return markdown
