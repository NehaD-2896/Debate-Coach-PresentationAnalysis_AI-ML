from fastapi import FastAPI
from pydantic import BaseModel

from argument_analysis.analyzer import analyze_argument
from counterargument_generation.generator import CounterArgumentGenerator

# Initialize the Counterargument Generator
generator = CounterArgumentGenerator()

# Create FastAPI application
app = FastAPI(
    title="AI Debate Coach API",
    version="1.0"
)

# Request model
class ArgumentRequest(BaseModel):
    argument: str


# Home Route
@app.get("/")
def home():
    return {
        "message": "AI Debate Coach API Running"
    }


# ==============================
# Module 1: Argument Analysis
# ==============================
@app.post("/argument-analysis")
def argument_analysis(request: ArgumentRequest):
    return analyze_argument(request.argument)


# ======================================
# Module 2: Counterargument Generation
# ======================================
@app.post("/counterargument")
def counterargument(request: ArgumentRequest):
    result = generator.generate(request.argument)

    return {
        "input_argument": request.argument,
        "counterargument": result
    }