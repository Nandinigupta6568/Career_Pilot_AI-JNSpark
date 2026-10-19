"""Local preflight checks before trying Agentverse deployment."""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    failures = []
    for module in ("uagents", "dotenv", "requests"):
        if importlib.util.find_spec(module) is None:
            failures.append(f"Missing Python package: {module}")
    env_file = ROOT / ".env"
    if not env_file.exists():
        failures.append("Missing .env file; copy .env.example to .env")
    else:
        # load_dotenv used by config; do not print secret values
        from dotenv import load_dotenv
        load_dotenv(env_file)
        if not os.getenv("ASI_ONE_API_KEY", "").strip():
            failures.append("ASI_ONE_API_KEY is blank in .env")
        seed = os.getenv("CAREERPILOT_AGENT_SEED", "").strip()
        if not seed or seed == "replace_with_your_own_private_seed_phrase":
            failures.append("Set a private CAREERPILOT_AGENT_SEED in .env before deploying")
    if failures:
        print("PREFLIGHT FAILED:")
        for item in failures:
            print("-", item)
        return 1
    print("PREFLIGHT PASSED: dependencies, .env, API key, and private seed are present.")
    print("This does not prove the API key works or that Agentverse deployment succeeded.")
    print("Next: python scripts/check_asi_one.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
