from api.v1.services import embedding
from api.v1 import app_state
from langfuse import observe
from api.v1.data_access import firecrawl, supabase, openai, langfuse


@observe(name="extract_and_save_startup_data")
def extract_and_save_startup_data(url: str):
    markdown = firecrawl.scrape(url)

    # Extract startup data
    data = openai.extract_startup_data(markdown)
    langfuse.create_scores(data)

    # Get embeddings
    data.embedding, data.best_fitting_vc, data.confidence = embedding.get_embeddings(data, app_state.funds_index, app_state.funds_metadata)

    # Save startup data
    supabase.insert_startup_data(url, markdown, data)
    return markdown
