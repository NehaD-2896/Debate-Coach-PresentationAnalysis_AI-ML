from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_recommendation(strength, clarity, relevance, persuasiveness, fallacy):

    prompt = f"""
You are an AI Debate Coach.

Analyze the following results:

Argument Strength: {strength}/100
Clarity: {clarity}/100
Relevance: {relevance}/100
Persuasiveness: {persuasiveness}/100

Detected Fallacy:
- {fallacy}

Provide:

1. Strengths
2. Weaknesses
3. Personalized Recommendations
4. Practice Exercises
5. Overall Coaching Feedback
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )

    return response.text