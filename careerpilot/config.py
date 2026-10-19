import os
from dotenv import load_dotenv

load_dotenv()

ASI_ONE_API_KEY = os.getenv("ASI_ONE_API_KEY", "").strip()
ASI_ONE_BASE_URL = os.getenv("ASI_ONE_BASE_URL", "https://api.asi1.ai/v1").strip().rstrip("/")
ASI_ONE_MODEL = os.getenv("ASI_ONE_MODEL", "asi1").strip()
ASI_ONE_TIMEOUT = int(os.getenv("ASI_ONE_TIMEOUT", "45"))
