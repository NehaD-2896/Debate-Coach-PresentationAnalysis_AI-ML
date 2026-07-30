from fastapi import FastAPI
from pydantic import BaseModel

from argument_analysis.analyzer import analyze_argument
from counterargument_generation.generator import CounterArgumentGenerator
from debate_simulation.simulator import DebateSimulator
from logical_fallacy_detection.detector import LogicalFallacyDetector

# Initialize AI Modules
counter_generator = CounterArgumentGenerator()
debate_simulator = DebateSimulator()
fallacy_detector = LogicalFallacyDetector()

# Create FastAPI application
app = FastAPI(
    title="AI Debate Coach API",
    version="1.0"
)

# Request Model
class ArgumentRequest(BaseModel):
    argument: str


# Home Route
@app.get("/")
def home():
    return {
        "message": "AI Debate Coach API Running"
    }


# ======================================
# Module 1: Argument Analysis
# ======================================
@app.post("/argument-analysis")
def argument_analysis(request: ArgumentRequest):
    return analyze_argument(request.argument)


# ======================================
# Module 2: Counterargument Generation
# ======================================
@app.post("/counterargument")
def counterargument(request: ArgumentRequest):
    result = counter_generator.generate(request.argument)

    return {
        "module": "Counterargument Generation Engine",
        "input_argument": request.argument,
        "counterargument": result
    }


# ======================================
# Module 3: Debate Simulation
# ======================================
@app.post("/debate-simulation")
def debate_simulation(request: ArgumentRequest):
    result = debate_simulator.simulate(request.argument)

    return {
        "module": "Debate Simulation Engine",
        "input_argument": request.argument,
        "result": result
    }


# ======================================
# Module 4: Logical Fallacy Detection
# ======================================
@app.post("/logical-fallacy")
def logical_fallacy(request: ArgumentRequest):
    result = fallacy_detector.detect(request.argument)

    return {
        "module": "Logical Fallacy Detection Engine",
        "input_argument": request.argument,
        "result": result
    }