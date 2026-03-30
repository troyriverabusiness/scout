from api.v1.data_access.supabase import Startup
from api.v1.data_access import supabase

def get_all_startups() -> list[Startup]:
    return supabase.get_all_startup_data()


def get_startup(id: str) -> Startup:
    return supabase.get_startup_data(id)