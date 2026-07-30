import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-flash-latest")


class LogicalFallacyDetector:

    def detect(self, argument):

        prompt = f"""
You are an expert in critical thinking and logical reasoning.

Analyze the following argument and identify any logical fallacies.

Argument:
{argument}

Return ONLY valid JSON.

Do not include markdown or explanations.

Return exactly this format:

{{
  "fallacies": [
    {{
      "name": "",
      "description": "",
      "severity": "",
      "suggestion": ""
    }}
  ],
  "overall_score": 0,
  "feedback": ""
}}

Rules:
- Detect common fallacies such as:
  - Ad Hominem
  - Straw Man
  - False Dilemma
  - Slippery Slope
  - Bandwagon
  - Hasty Generalization
  - Appeal to Authority
  - Circular Reasoning
- If no fallacy exists, return an empty list.
- overall_score must be between 0 and 100.
"""

        response = model.generate_content(prompt)

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(text)

            if isinstance(result.get("overall_score"), int):
                result["overall_score"] = max(
                    0,
                    min(100, result["overall_score"])
                )

            return result

        except json.JSONDecodeError:
            return {
                "error": "Gemini returned invalid JSON",
                "raw_response": text
            }