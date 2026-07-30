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



class PerformanceScorer:


    def evaluate(self, argument):


        prompt = f"""
You are an expert debate evaluator and communication coach.

Analyze the following debate argument:

Argument:
{argument}


Evaluate the debate performance based on:

1. Clarity of argument
2. Logical reasoning
3. Evidence and examples
4. Persuasiveness
5. Argument structure


Give scores from 0-100.

Return ONLY valid JSON.

Do not include markdown or explanations.

Return exactly this format:


{{
  "clarity_score": 0,
  "logic_score": 0,
  "evidence_score": 0,
  "persuasion_score": 0,
  "structure_score": 0,

  "overall_score": 0,

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
                "error": "Invalid JSON response from Gemini",
                "raw_response": response.text
            }