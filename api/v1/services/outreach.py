# Aboutme: Generate natural outreach message/text to a founder or VC fund
from api.v1.data_access import openai, langfuse
from api.v1.data_access.supabase import Startup
from langfuse import observe

@observe(name="generate_outreach")
def generate_outreach(startup: Startup, target: str) -> str:
    # Generate outreach message/text to a founder or VC fund
    if target == "founder":
        return generate_founder_outreach(startup)
    elif target == "vc":
        return generate_vc_outreach(startup)
    else:
        raise ValueError(f"Invalid target: {target}, must be 'founder' or 'vc'")


def generate_founder_outreach(startup: Startup) -> str:
    system_prompt, langfuse_prompt_ref = langfuse.get_outreach_prompt(langfuse.OUTREACH_FOUNDER_PROMPT_NAME)
    return openai.create_message(system_prompt, langfuse_prompt_ref, startup_to_text(startup))

def generate_vc_outreach(startup: Startup) -> str:
    system_prompt, langfuse_prompt_ref = langfuse.get_outreach_prompt(langfuse.OUTREACH_VC_PROMPT_NAME)
    return openai.create_message(system_prompt, langfuse_prompt_ref, startup_to_text(startup))

def startup_to_text(startup: Startup) -> str:
    return f"""Company: {startup.name}
One-liner: {startup.one_liner}
Founders: {startup.founders}
Traction: {startup.traction_signals}
Description: {startup.description}
"""