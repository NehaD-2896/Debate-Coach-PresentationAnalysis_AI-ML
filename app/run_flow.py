import argparse
import asyncio
import json
from pathlib import Path
from app.agents.presentation_analysis_agent import PresentationAnalysisAgent
from app.services.document_parser import parse_document
from app.services.transcription import transcribe_audio


async def main():
    parser = argparse.ArgumentParser(description="Run Presentation Analysis Engine")
    parser.add_argument("--document", required=True, help="PPTX or PDF presentation")
    parser.add_argument("--audio", required=True, help="Recorded speech audio/video")
    parser.add_argument("--duration", required=True, type=float, help="Actual speaking duration in seconds")
    args = parser.parse_args()

    slides = parse_document(args.document, Path(args.document).name)
    transcript = transcribe_audio(args.audio)
    result = await PresentationAnalysisAgent().run(transcript, Path(args.document).name, slides, args.duration)
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
