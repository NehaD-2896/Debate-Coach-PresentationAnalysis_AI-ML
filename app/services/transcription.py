from app.config import settings

_model = None


def transcribe_audio(audio_file_path: str) -> str:
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel(
            settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE,
        )
    segments, _info = _model.transcribe(audio_file_path, beam_size=5)
    return " ".join(segment.text.strip() for segment in segments).strip()
