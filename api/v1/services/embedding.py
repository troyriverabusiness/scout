# Aboutme: Score startups against fund thesis vectors
from api.v1.data_access import embeddings, supabase, index
from api.v1.data_access.supabase import Startup
from langfuse import observe
from sentence_transformers import SentenceTransformer
import faiss


@observe(name="get_embeddings")
def get_embeddings(model: SentenceTransformer, startup: Startup, index: faiss.Index, metadata: list[str]):
    # Get startup embedding
    startup_embedding = get_startup_embedding(model, startup)

    # Get fund best-fit & score
    best_fit, score = rank_startup_against_funds(model, index, metadata, startup)
    
    # Lookup best-fit fund name
    best_fit_name = lookup_fund_name(best_fit)
    
    return startup_embedding, best_fit_name, score
    

@observe(name="get_startup_embedding")
def get_startup_embedding(model: SentenceTransformer, startup: Startup) -> list[float]:
    return embeddings.create_embedding(model, startup_to_text(startup))


@observe(name="rank_startup_against_funds")
def rank_startup_against_funds(model: SentenceTransformer, index: faiss.Index, metadata: list[str], startup: Startup):
    # Text
    search_query = startup_to_text(startup)

    # Embedding
    search_embedding = embeddings.create_embedding(model, search_query)

    # Search index
    distances, indices = index.search(search_embedding, 1)

    # Get best-fit fund & score
    best_fit = metadata[indices[0][0]] # RETURNS ID OF FUND
    score = distances[0][0]

    return best_fit, score

# TODO: Lookup fund name from id returned by index search
def lookup_fund_name(id: str) -> str:
    pass

# Flatten startup data to text for embedding
def startup_to_text(startup: Startup) -> str:
    return f"{startup.one_liner} {startup.description} {startup.tags}"


def create_startups_index() -> tuple[faiss.Index, list[Startup]]:
    startups = supabase.get_all_startup_data()
    vectors = [startup.embedding for startup in startups]
    metadata = [startup.id for startup in startups]
    index, _ = index.create_index(vectors, metadata, "startups")
    return index, startups


def create_funds_index(model: SentenceTransformer) -> tuple[faiss.Index, list[str]]:
    funds = get_fund_memos()
    vectors = [embeddings.create_embedding(model, fund) for fund in funds]
    return index.create_index(vectors, funds, "funds")


# TODO: Write good detailed memos
def get_fund_memos() -> list[str]:
    return ["UVC Partners is a venture capital firm that invests in early-stage startups in the B2B SaaS, DACH, and seed to Series A space.",
            "Unternehmertum Venture Capital is a venture capital firm that invests in early-stage startups in the deep tech, TUM spin-offs, hardware, and industrial AI space.",
            "Bayern Kapital is a venture capital firm that invests in early-stage startups in the Bavarian startups, seed, life sciences, software, and clean tech space.",
            "Speedinvest is a venture capital firm that invests in early-stage startups in the pan-European, pre-seed, fintech, marketplace, and AI space."]