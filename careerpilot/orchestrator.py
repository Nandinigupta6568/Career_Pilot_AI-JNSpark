"""Entry point for the CareerPilot end-to-end workflow."""
from careerpilot.asi_one import ask_asi_one

def run_careerpilot(user_prompt: str) -> str:
    prompt = user_prompt.strip()
    if not prompt:
        raise ValueError("Please provide a career goal and current skills.")
    if len(prompt) > 8000:
        raise ValueError("Please keep the request under 8,000 characters.")
    return ask_asi_one(prompt)
