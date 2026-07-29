import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")


def analyze_argument(argument: str):

    prompt = f"""
You are an AI Debate Coach.

Analyze the following argument.

Argument:
{argument}

Return ONLY valid JSON.

Do not include markdown or explanations.

Return exactly this JSON format:

{{
  "claim": "",
  "evidence": "",
  "reasoning": "",
  "argument_type": "",
  "persuasiveness": 0,
  "strength_score": 0,
  "clarity_score": 0,
  "relevance_score": 0,
  "missing_points": [],
  "feedback": ""
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "error": "Gemini returned invalid JSON",
            "raw_response": text
        }