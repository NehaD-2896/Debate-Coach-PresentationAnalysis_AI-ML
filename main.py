from fastapi import FastAPI
from pydantic import BaseModel

from argument_analysis.analyzer import analyze_argument
from counterargument_generation.generator import CounterArgumentGenerator
from debate_simulation.simulator import DebateSimulator
from logical_fallacy_detection.detector import LogicalFallacyDetector
from performance_scoring.scorer import PerformanceScorer


# ======================================
# Initialize AI Modules
# ======================================

counter_generator = CounterArgumentGenerator()

debate_simulator = DebateSimulator()

fallacy_detector = LogicalFallacyDetector()

performance_scorer = PerformanceScorer()


# ======================================
# FastAPI Application
# ======================================

app = FastAPI(
    title="AI Debate Coach API",
    version="1.0"
)


# ======================================
# Request Model
# ======================================

class ArgumentRequest(BaseModel):
    argument: str



# ======================================
# Home API
# ======================================

@app.get("/")
def home():

    return {
        "message": "AI Debate Coach API Running",
        "modules": [
            "Argument Analysis Engine",
            "Counterargument Generation Engine",
            "Debate Simulation Engine",
            "Logical Fallacy Detection Engine",
            "Performance Scoring Engine"
        ]
    }



# ======================================
# Module 1: Argument Analysis Engine
# ======================================

@app.post("/argument-analysis")
def argument_analysis(request: ArgumentRequest):

    result = analyze_argument(
        request.argument
    )

    return {
        "module": "Argument Analysis Engine",
        "input_argument": request.argument,
        "result": result
    }



# ======================================
# Module 2: Counterargument Generation Engine
# ======================================

@app.post("/counterargument")
def counterargument(request: ArgumentRequest):

    result = counter_generator.generate(
        request.argument
    )

    return {
        "module": "Counterargument Generation Engine",
        "input_argument": request.argument,
        "counterargument": result
    }



# ======================================
# Module 3: Debate Simulation Engine
# ======================================

@app.post("/debate-simulation")
def debate_simulation(request: ArgumentRequest):

    result = debate_simulator.simulate(
        request.argument
    )

    return {
        "module": "Debate Simulation Engine",
        "input_argument": request.argument,
        "result": result
    }



# ======================================
# Module 4: Logical Fallacy Detection Engine
# ======================================

@app.post("/logical-fallacy")
def logical_fallacy(request: ArgumentRequest):

    result = fallacy_detector.detect(
        request.argument
    )

    return {
        "module": "Logical Fallacy Detection Engine",
        "input_argument": request.argument,
        "result": result
    }



# ======================================
# Module 5: Performance Scoring Engine
# ======================================

@app.post("/performance-score")
def performance_score(request: ArgumentRequest):

    result = performance_scorer.evaluate(
        request.argument
    )

    return {
        "module": "Performance Scoring Engine",
        "input_argument": request.argument,
        "result": result
    }