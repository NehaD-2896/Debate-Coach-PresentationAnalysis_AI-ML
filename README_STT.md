# Speech-to-Text integration

This adds a real Whisper-based speech-to-text module without replacing the
existing four-module orchestration contract.

## Files

- `app/agents/speech_to_text_agent.py` — `SpeechToTextAgent` using `faster-whisper`.
- `orchestration/speech_to_text_adapter.py` — adapter for the existing workflow.
- `tests/test_speech_to_text_agent.py` — tests the contract without downloading a model.
- `orchestration/debate_workflow_stt_patch.py` — exact changes to add `run_audio()` to the current workflow.

## Install

```powershell
pip install faster-whisper
```

For CPU on Windows, the defaults are:

```text
STT_MODEL_SIZE=small
STT_DEVICE=cpu
STT_COMPUTE_TYPE=int8
```

These can be set in `.env`; do not commit `.env`.

## Flow

Audio file -> SpeechToTextAgent -> transcript -> existing four-stage workflow.

The existing `run(argument)` behavior remains unchanged. `run_audio(audio)` is
an optional entry point so current tests and callers are not broken.
