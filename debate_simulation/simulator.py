import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")


class DebateSimulator:

    def simulate(self, argument):

        prompt = f"""
You are an expert AI Debate Coach and Debate Opponent.

A user has presented the following argument:

Argument:
{argument}

Your task is to simulate a debate by taking the opposing side.

Return ONLY valid JSON.

Do not include markdown, explanations, or extra text.

Return exactly this JSON format:

{{
  "stance": "Opposition",
  "opponent_response": "",
  "supporting_points": [
    "",
    "",
    ""
  ],
  "question": "",
  "strategy": "",
  "confidence": 0
}}

Instructions:
- stance should always be "Opposition".
- opponent_response should contain a strong opposing argument.
- supporting_points should contain exactly 3 logical points.
- question should challenge the user's argument.
- strategy should briefly explain the debating approach.
- confidence should be an integer between 0 and 100.
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