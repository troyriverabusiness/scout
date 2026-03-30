from api.v1.services import embedding
from langfuse import observe
from api.v1.data_access import firecrawl, supabase, openai, langfuse
import faiss


@observe(name="extract_and_save_startup_data")
def extract_and_save_startup_data(url: str, funds_index: faiss.Index, funds_metadata: list[str]):
    markdown = firecrawl.scrape(url)

    # Extract startup data
    data = openai.extract_startup_data(markdown)
    langfuse.create_scores(data)

    # Get embeddings
    data.embedding, data.best_fitting_vc, data.confidence = embedding.get_embeddings(data, funds_index, funds_metadata)

    # Save startup data
    supabase.insert_startup_data(url, markdown, data)
    return markdown
