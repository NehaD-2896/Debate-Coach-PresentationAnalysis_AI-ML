import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import settings
from app.agents.presentation_analysis_agent import PresentationAnalysisAgent
from app.services.document_parser import parse_document
from app.services.transcription import transcribe_audio

app = FastAPI(
    title="Agentic AI Debate Coach — Presentation Analysis Engine",
    version="1.0.0",
    description="Presentation speech, delivery and content intelligence module designed for integration with the debate platform.",
)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
agent = PresentationAnalysisAgent()


class TextPresentationRequest(BaseModel):
    transcript: str = Field(min_length=1)
    filename: str = "typed_presentation"
    duration_seconds: float | None = None
    slides: list[dict] = Field(default_factory=list)


@app.get("/health")
def health():
    return {"status": "ok", "engine": "presentation_analysis_engine", "llm_providers": agent_providers()}


def agent_providers():
    from app.llm_client import LLMClient
    return LLMClient().providers


@app.post("/api/v1/presentation/analyze-text")
async def analyze_text(body: TextPresentationRequest):
    return await agent.run(body.transcript, body.filename, body.slides, body.duration_seconds)


@app.post("/api/v1/presentation/analyze-full")
@app.post("/api/v1/presentation/analyze")
async def analyze_full(
    document: UploadFile = File(...),
    audio: UploadFile = File(...),
    duration_seconds: float = Form(...),
):
    doc_suffix = os.path.splitext(document.filename or "presentation.pptx")[1] or ".pptx"
    audio_suffix = os.path.splitext(audio.filename or "speech.webm")[1] or ".webm"
    doc_path = audio_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=doc_suffix) as f:
            f.write(await document.read()); doc_path = f.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=audio_suffix) as f:
            f.write(await audio.read()); audio_path = f.name
        slides = parse_document(doc_path, document.filename)
        transcript = transcribe_audio(audio_path)
        if not transcript.strip():
            raise HTTPException(status_code=422, detail="No speech could be transcribed from the audio file.")
        return await agent.run(transcript, document.filename or "presentation", slides, duration_seconds)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        for path in (doc_path, audio_path):
            if path and os.path.exists(path):
                os.remove(path)


@app.post("/api/v1/presentation/analyze-document")
async def analyze_document(
    document: UploadFile = File(...),
    transcript: str = Form(...),
    duration_seconds: float | None = Form(None),
):
    suffix = os.path.splitext(document.filename or "presentation.pptx")[1] or ".pptx"
    path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(await document.read()); path = f.name
        slides = parse_document(path, document.filename)
        return await agent.run(transcript, document.filename or "presentation", slides, duration_seconds)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        if path and os.path.exists(path):
            os.remove(path)
