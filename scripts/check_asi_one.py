"""Check the ASI:One key and API connection without printing the secret."""
from careerpilot.config import ASI_ONE_API_KEY, ASI_ONE_BASE_URL, ASI_ONE_MODEL, ASI_ONE_TIMEOUT
import requests


def main() -> int:
    if not ASI_ONE_API_KEY:
        print("FAIL: ASI_ONE_API_KEY is missing. Add it to .env.")
        return 1
    try:
        response = requests.post(
            f"{ASI_ONE_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {ASI_ONE_API_KEY}", "Content-Type": "application/json"},
            json={"model": ASI_ONE_MODEL, "messages": [{"role": "user", "content": "Reply with exactly: CareerPilot connection works."}], "max_tokens": 40, "temperature": 0},
            timeout=ASI_ONE_TIMEOUT,
        )
        if response.status_code in (401, 402):
            print(f"FAIL: API returned HTTP {response.status_code}. Check key, access, and quota.")
            return 1
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices") or []
        content = ((choices[0].get("message") or {}).get("content") or "").strip() if choices else ""
        if not content:
            print("FAIL: API responded, but no assistant text was returned.")
            return 1
        print("PASS: ASI:One API connection succeeded.")
        print("Model:", data.get("model", ASI_ONE_MODEL))
        print("Response:", content)
        return 0
    except requests.RequestException as exc:
        print(f"FAIL: Network/API request failed ({type(exc).__name__}). Check connection and API settings.")
        return 1
    except (ValueError, KeyError, IndexError, TypeError):
        print("FAIL: ASI:One returned an unexpected response format.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
