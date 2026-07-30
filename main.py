from fastapi import FastAPI
from pydantic import BaseModel

from recommendation_engine.recommender import generate_recommendation

app = FastAPI()


class RecommendationRequest(BaseModel):
    strength: int
    clarity: int
    relevance: int
    persuasiveness: int
    fallacy: str


@app.get("/")
def home():
    return {"message": "Welcome to my Recommendation & Coaching Agent!"}


@app.post("/recommendation")
def recommendation(data: RecommendationRequest):

    report = generate_recommendation(
        data.strength,
        data.clarity,
        data.relevance,
        data.persuasiveness,
        data.fallacy
    )

    return {
        "coaching_report": report
    }