import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")


class CounterArgumentGenerator:

    def generate(self, argument):

        prompt = f"""
You are an AI Debate Coach.

Given the following argument:

Argument:
{argument}

Generate a counterargument.

Return ONLY valid JSON.

Do not include markdown or explanations.

Return exactly this JSON format:

{{
  "counterargument": "",
  "reasons": [
    "",
    "",
    ""
  ],
  "example": ""
}}
"""

        response = model.generate_content(prompt)

        text = response.text.strip()

        # Remove markdown if Gemini returns it
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "error": "Gemini returned invalid JSON",
                "raw_response": text
            }