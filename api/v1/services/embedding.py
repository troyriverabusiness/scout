# Aboutme: Score startups against fund thesis vectors
from api.v1.data_access import embeddings, supabase, index
from api.v1.data_access.supabase import Startup
from langfuse import observe
import faiss


@observe(name="get_embeddings")
def get_embeddings(startup: Startup, faiss_index: faiss.Index, metadata: list[str]):
    startup_embedding = get_startup_embedding(startup)
    best_fit, score = rank_startup_against_funds(faiss_index, metadata, startup)
    best_fit_name = lookup_fund_name(best_fit)
    return startup_embedding, best_fit_name, score


@observe(name="get_startup_embedding")
def get_startup_embedding(startup: Startup) -> list[float]:
    return embeddings.create_embedding(startup_to_text(startup))


@observe(name="rank_startup_against_funds")
def rank_startup_against_funds(faiss_index: faiss.Index, metadata: list[str], startup: Startup):
    search_embedding = embeddings.create_embedding(startup_to_text(startup))
    distances, indices = faiss_index.search(search_embedding, 1)
    best_fit = metadata[indices[0][0]]
    score = distances[0][0]
    return best_fit, score

# TODO: implement — look up the human-readable fund name from its ID
# (either store name alongside id in metadata list, or query Supabase funds table)
def lookup_fund_name(id: str) -> str:
    pass

# Flatten startup data to text for embedding
def startup_to_text(startup: Startup) -> str:
    tags = " ".join(startup.traction_signals or [])
    return f"{startup.name} {startup.description} {startup.sector} {tags}"


def create_startups_index() -> tuple[faiss.Index, list[Startup]]:
    startups = supabase.get_all_startup_data()
    vectors = [startup.embedding for startup in startups]
    metadata = [startup.id for startup in startups]
    faiss_index, _ = index.create_index(vectors, metadata, "startups")
    return faiss_index, startups


def create_funds_index() -> tuple[faiss.Index, list[str]]:
    funds = get_fund_memos()
    vectors = [embeddings.create_embedding(fund) for fund in funds]
    return index.create_index(vectors, funds, "funds")


# TODO: replace hardcoded strings with memos stored in Supabase (funds table)
# so new funds can be added without a code change
def get_fund_memos() -> list[str]:
    return ["UVC Partners is a venture capital firm that invests in early-stage startups in the B2B SaaS, DACH, and seed to Series A space.",
            "Unternehmertum Venture Capital is a venture capital firm that invests in early-stage startups in the deep tech, TUM spin-offs, hardware, and industrial AI space.",
            "Bayern Kapital is a venture capital firm that invests in early-stage startups in the Bavarian startups, seed, life sciences, software, and clean tech space.",
            "Speedinvest is a venture capital firm that invests in early-stage startups in the pan-European, pre-seed, fintech, marketplace, and AI space."]