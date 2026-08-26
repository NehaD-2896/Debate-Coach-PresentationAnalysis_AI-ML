# Presentation Analysis Engine — Advanced Reference-Style Module

An advanced, independently integrable Presentation Analysis Engine modeled on the supplied Reference ZIP workflow.

## Core workflow
1. Upload the real PPTX/PDF you will present.
2. Click **Start presenting**.
3. The browser records microphone audio directly with `MediaRecorder`.
4. Click **Stop & Analyze**; duration is calculated automatically.
5. Fast/Whisper transcribes the real recording locally.
6. The backend extracts the real slide text with `python-pptx` / `pdfplumber`.
7. **Groq is the primary LLM** for evidence-grounded delivery + content analysis.
8. The UI displays the combined report and slide-specific feedback.

## Advanced AI behavior
The Groq prompt is explicitly grounded in the extracted slides and transcript. It produces:
- confidence, clarity and engagement scores
- grammar issues based on the transcript
- delivery strengths and improvement actions
- structure, content clarity, claim-support and flow scores
- slide-by-slide takeaway
- explicit supporting detail actually present in the slide
- slide-specific improvement feedback
- transcript-to-slide alignment when evidence permits

The model is instructed not to invent facts, visuals, audience reactions or evidence that are absent from the supplied inputs.

## Configure Groq
Copy `.env.example` to `.env` and set:

```env
GROQ_API_KEY=your_real_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Groq is used first. Gemini is optional fallback if configured.

## Run backend
```powershell
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

Health: http://127.0.0.1:8010/health
Swagger: http://127.0.0.1:8010/docs

## Run frontend
```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Integration contract
`POST /api/v1/presentation/analyze-full` accepts:
- `document`: PPTX/PDF
- `audio`: recorded WebM/audio
- `duration_seconds`: actual recording duration

The normal browser UI supplies all three automatically. The API remains directly usable by your teammate's integration.

The response is designed for the Performance Scoring Engine and contains delivery metrics, content metrics, transcript, slide feedback and AI-provider metadata. The final cross-module performance score remains the responsibility of the Performance Scoring Engine.
