"""Quick live Groq connectivity check for this engine."""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")
if not key:
    raise SystemExit("GROQ_API_KEY is not set. Put it in .env or export it first.")

model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
client = Groq(api_key=key)
result = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "Reply with exactly one short sentence."},
        {"role": "user", "content": "Confirm that the performance scoring engine can reach Groq."},
    ],
    temperature=0,
    max_completion_tokens=80,
)
print("Groq OK")
print("model:", result.model)
print("response:", result.choices[0].message.content)
