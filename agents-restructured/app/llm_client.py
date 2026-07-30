"""
One shared function for talking to the LLM - uses Google's "google-genai" SDK.
Includes automatic retry with backoff for rate-limit (429) errors, since the
free tier allows only a few requests per minute - a burst of calls will hit
this normally, and retrying after a short wait resolves it without crashing.
"""
import json
import time

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from app.config import GEMINI_API_KEY, LLM_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

MAX_RETRIES = 3


def call_llm(system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    """
    system_prompt: instructions describing the AI's role (e.g. "You are a debate judge...")
    user_prompt: the actual content to analyze/respond to
    json_mode: if True, forces the model to return valid JSON only (no extra text)
    """
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.4,
        response_mime_type="application/json" if json_mode else "text/plain",
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=LLM_MODEL,
                contents=user_prompt,
                config=config,
            )
            return response.text
        except ClientError as e:
            is_rate_limit = "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e)
            if is_rate_limit and attempt < MAX_RETRIES:
                wait_seconds = 20 * attempt  # 20s, then 40s
                print(f"Rate limit hit (attempt {attempt}/{MAX_RETRIES}). Waiting {wait_seconds}s before retry...")
                time.sleep(wait_seconds)
                continue
            raise


def call_llm_json(system_prompt: str, user_prompt: str) -> dict:
    """Same as call_llm, but parses the result into a Python dict for you."""
    raw = call_llm(system_prompt, user_prompt, json_mode=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Model did not return valid JSON", "raw_output": raw}