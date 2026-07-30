from fastapi import FastAPI
from pydantic import BaseModel

# ==========================
# AI Module Imports
# ==========================
from argument_analysis.analyzer import analyze_argument
from counterargument_generation.generator import CounterArgumentGenerator
from debate_simulation.simulator import DebateSimulator

# ==========================
# Initialize AI Modules
# ==========================
generator = CounterArgumentGenerator()
simulator = DebateSimulator()

# ==========================
# FastAPI Application
# ==========================
app = FastAPI(
    title="AI Debate Coach API",
    version="1.0"
)

# ==========================
# Request Model
# ==========================
class ArgumentRequest(BaseModel):
    argument: str


# ==========================
# Home Route
# ==========================
@app.get("/")
def home():
    return {
        "message": "AI Debate Coach API Running"
    }


# ====================================================
# Module 1: Argument Analysis Engine
# ====================================================
@app.post("/argument-analysis")
def argument_analysis(request: ArgumentRequest):
    return analyze_argument(request.argument)


# ====================================================
# Module 2: Counterargument Generation Engine
# ====================================================
@app.post("/counterargument")
def counterargument(request: ArgumentRequest):

    result = generator.generate(request.argument)

    return {
        "module": "Counterargument Generation Engine",
        "input_argument": request.argument,
        "result": result
    }


# ====================================================
# Module 3: Debate Simulation Engine
# ====================================================
@app.post("/debate-simulation")
def debate_simulation(request: ArgumentRequest):

    result = simulator.simulate(request.argument)

    return {
        "module": "Debate Simulation Engine",
        "input_argument": request.argument,
        "result": result
    }