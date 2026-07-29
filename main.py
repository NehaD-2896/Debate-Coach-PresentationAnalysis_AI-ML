from fastapi import FastAPI
from pydantic import BaseModel

from argument_analysis.analyzer import analyze_argument

app = FastAPI(
    title="AI Debate Coach API",
    version="1.0"
)


class ArgumentRequest(BaseModel):
    argument: str


@app.get("/")
def home():
    return {"message": "AI Debate Coach API Running"}


@app.post("/argument-analysis")
def argument_analysis(request: ArgumentRequest):
    return analyze_argument(request.argument)