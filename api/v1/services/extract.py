from api.v1.services import embedding
from langfuse import observe
from api.v1.data_access import firecrawl, supabase, openai, langfuse
from sentence_transformers import SentenceTransformer

@observe(name="extract_and_save_startup_data")
def extract_and_save_startup_data(url: str, model: SentenceTransformer):
    # Scrape for raw Markdown
    markdown = firecrawl.scrape(url)

    # Extract structured startup data and score the extraction span
    data = openai.extract_startup_data(markdown)
    langfuse.create_scores(data)

    # Get embedding
    # TODO: Call the new get_embeddings() function
    startup_embedding = embedding.get_startup_embedding(model, data)

    supabase.insert_startup_data(url, markdown, data, startup_embedding)

    return markdown
