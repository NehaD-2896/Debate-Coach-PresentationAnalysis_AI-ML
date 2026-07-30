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



class PresentationAnalyzer:


    def analyze(self, presentation_text):

        prompt = f"""
You are an expert presentation coach.

Analyze the following presentation transcript:

Presentation:
{presentation_text}


Evaluate the presentation based on:

1. Clarity
2. Structure
3. Grammar
4. Engagement
5. Communication quality


Identify filler words if present.

Return ONLY valid JSON.

Do not include markdown or explanations.


Return exactly this format:


{{
  "clarity_score": 0,
  "structure_score": 0,
  "grammar_score": 0,
  "engagement_score": 0,
  "communication_score": 0,

  "overall_score": 0,

  "filler_words": [
    ""
  ],

  "strengths": [
    ""
  ],

  "weaknesses": [
    ""
  ],

  "improvements": [
    ""
  ]
}}

"""


        response = model.generate_content(prompt)


        try:

            return json.loads(response.text)


        except json.JSONDecodeError:

            return {
                "error": "Invalid JSON response",
                "raw_response": response.text
            }