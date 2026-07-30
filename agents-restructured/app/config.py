"""
Loads settings from the .env file so no API keys are ever hardcoded in the code.
"""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is not set. LLM calls will fail until you add it to .env")
