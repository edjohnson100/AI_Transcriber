# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Transcriber is a local AI audio/video transcription tool built on OpenAI Whisper. It converts audio/video files to text entirely offline — no cloud upload. The sole user-facing script is `ai_transcriber.py`.

## Running the Script

```powershell
# Interactive menu — scans current directory for media files
python ai_transcriber.py

# Direct file mode (drag-and-drop)
python ai_transcriber.py "file1.mp3" "file2.mp4"
```

## Environment Setup

Platform-specific venvs (`venv_win`, `venv_mac`) are created by `setup.py`:

```powershell
python setup.py   # creates venv_win on Windows, venv_mac on Mac
```

Dependencies are in `requirements_win.txt` (openai-whisper, torch) and `requirements_mac.txt` (openai-whisper as fallback only).

## Architecture

**`ai_transcriber.py`** — Single user-facing script. At startup it checks for a compiled `whisper.cpp` binary (`whisper.cpp/build/bin/whisper-cli`). If found (Mac), it routes transcription through the C++ binary. If not (Windows, or Mac without the build), it falls back to the `openai-whisper` Python package. In both cases, FFmpeg extracts audio to a 16kHz mono WAV first, then Whisper processes that file. At the start of each session the user selects an output format: `.vtt` (WebVTT), `.srt` (SubRip), `.txt` (plain text, no timestamps), or All (default). Selected files are saved alongside the source file.

**`transcribe_base.py` / `transcribe_timestamps.py`** — Minimal reference examples with hardcoded filenames. Not user-facing.

## Key Configuration (top of ai_transcriber.py)

- `INITIAL_PROMPT` — Primes Whisper with vocabulary and punctuation style for the content type.
- `MEDIA_EXTENSIONS` — Set of file extensions the interactive menu will scan for.
- `WHISPER_EXEC` / `MODEL_PATH` / `VAD_MODEL_PATH` — Paths to the whisper.cpp binary and models (Mac only).
- `PYTHON_MODELS` / `DEFAULT_PYTHON_MODEL` — Model menu options for the Python fallback path.
- `WHISPER_CPP_AVAILABLE` — Computed at import time; controls which engine is used.
- `ALL_FORMATS` — `{'vtt', 'srt', 'txt'}` — the full set returned when the user selects All.
- `select_output_format()` — Interactive menu presented at the start of every session; returns a subset of `ALL_FORMATS`.

## Whisper Parameters (Python path)

The Python fallback uses tuned parameters: `temperature=0.0` (deterministic), `beam_size=4`, `best_of=4`, `initial_prompt`, `compression_ratio_threshold=2.4`, `no_speech_threshold=0.6`. Match these if updating the whisper.cpp CLI flags on the Mac path.

## Platform Notes

- Mac path sets `DYLD_LIBRARY_PATH` to point at whisper.cpp's shared libraries before spawning the subprocess.
- Windows path checks `torch.cuda.is_available()` and enables `fp16` only when a GPU is present.
- Whisper model weights (Python path) are cached in `~/.cache/whisper/` (Mac) or `%LOCALAPPDATA%\whisper` (Windows), not in the project directory.
