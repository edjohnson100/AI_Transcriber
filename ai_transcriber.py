# ==============================================================================
# SCRIPT: ai_transcriber.py
# AUTHOR: Ed Johnson / Claude
# DATE:   2026-05-31
# VERSION: 1.1.0 (format selection: VTT / SRT / TXT / All)
# CONTEXT: AI_Transcriber — Standalone Distribution Tool
# HARDWARE TARGET: Mac (whisper.cpp) & Windows (openai-whisper Python package)
#
# --- CHANGELOG (v1.0.0 -> v1.1.0) ---
# 1. Added SRT (SubRip) and plain TXT output formats.
# 2. Replaced custom [H:MM:SS -> H:MM:SS] .txt with plain text (no timestamps).
# 3. Added format selection menu: VTT / SRT / TXT / All (default).
# ==============================================================================

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Prime the Whisper model with vocabulary, context, or punctuation style.
INITIAL_PROMPT = "Hello everyone! Welcome to our session. Please maintain professional capitalization and punctuation throughout."

MEDIA_EXTENSIONS = {'.mp4', '.m4a', '.wav', '.mp3', '.mkv', '.mov', '.flv', '.aac'}

SCRIPT_DIR = Path(__file__).parent.resolve()
IS_MAC     = platform.system() == "Darwin"

# Mac: whisper.cpp binary and model paths
WHISPER_EXEC   = SCRIPT_DIR / "whisper.cpp" / "build" / "bin" / "whisper-cli"
MODEL_PATH     = SCRIPT_DIR / "whisper.cpp" / "models" / "ggml-large-v3-turbo.bin"
VAD_MODEL_PATH = SCRIPT_DIR / "whisper.cpp" / "models" / "ggml-silero-v5.1.2.bin"

# Python whisper model options (Windows / Mac fallback when whisper.cpp unavailable)
PYTHON_MODELS = {
    "1": ("tiny",   "Tiny   [~75MB]  (Fastest, lower accuracy)"),
    "2": ("base",   "Base   [~150MB] (Good balance for testing)"),
    "3": ("small",  "Small  [~500MB] (Better accuracy)"),
    "4": ("medium", "Medium [~1.5GB] (Great for podcasts/interviews)"),
    "5": ("large",  "Large  [~3GB]   (Best possible, very slow)"),
    "6": ("turbo",  "Turbo  [~800MB] (Best speed/accuracy balance) [Default]"),
}
DEFAULT_PYTHON_MODEL = "turbo"

# True only when the whisper.cpp binary and model file are both present on Mac
WHISPER_CPP_AVAILABLE = IS_MAC and WHISPER_EXEC.exists() and MODEL_PATH.exists()

ALL_FORMATS = {'vtt', 'srt', 'txt'}


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def _fmt_ts(seconds):
    """Float seconds → VTT timestamp HH:MM:SS.mmm."""
    ms = int((seconds % 1) * 1000)
    s  = int(seconds) % 60
    m  = int(seconds // 60) % 60
    h  = int(seconds // 3600)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def _fmt_ts_srt(seconds):
    """Float seconds → SRT timestamp HH:MM:SS,mmm (comma separator per SRT spec)."""
    ms = int((seconds % 1) * 1000)
    s  = int(seconds) % 60
    m  = int(seconds // 60) % 60
    h  = int(seconds // 3600)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ==============================================================================
# MENUS
# ==============================================================================

def select_output_format():
    """Interactive menu for choosing output format(s). Returns a set of format strings."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n--- SELECT OUTPUT FORMAT ---")
    print("  1. VTT  — WebVTT subtitles (web / HTML5 video players)")
    print("  2. SRT  — SubRip subtitles (DaVinci Resolve, Premiere, YouTube, VLC)")
    print("  3. TXT  — Plain text (no timestamps; great for reading or LLMs)")
    print("  A. All  — All three formats [Default]")
    print("----------------------------")
    choice = input("Enter choice (1/2/3/A) [Default: All]: ").strip().lower()
    if choice in ('', 'a'):
        return ALL_FORMATS
    if choice == '1':
        return {'vtt'}
    if choice == '2':
        return {'srt'}
    if choice == '3':
        return {'txt'}
    print("Invalid choice. Defaulting to All.")
    return ALL_FORMATS

def select_python_model():
    """Interactive menu for choosing a Python whisper model size."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n--- SELECT WHISPER MODEL ---")
    for key, (_, desc) in PYTHON_MODELS.items():
        print(f"  {key}. {desc}")
    print("----------------------------")
    choice = input("Enter number (1-6) [Default: turbo]: ").strip()
    if choice == "":
        return DEFAULT_PYTHON_MODEL
    if choice in PYTHON_MODELS:
        return PYTHON_MODELS[choice][0]
    print("Invalid choice. Defaulting to 'turbo'.")
    return DEFAULT_PYTHON_MODEL


# ==============================================================================
# TRANSCRIPTION ENGINES
# ==============================================================================

def run_whisper_cpp(audio_path, base_path, formats):
    """Mac: transcribe via whisper.cpp C++ binary, then move output files to final paths."""
    env = os.environ.copy()
    build_path = SCRIPT_DIR / "whisper.cpp" / "build"
    lib_paths  = [str(build_path / "src"), str(build_path / "ggml" / "src")]
    env["DYLD_LIBRARY_PATH"] = ":".join(lib_paths) + ":" + env.get("DYLD_LIBRARY_PATH", "")

    vad_args = (["--vad", "--vad-model", str(VAD_MODEL_PATH), "-vt", "0.30"]
                if VAD_MODEL_PATH.exists() else [])

    fmt_flags = []
    if 'vtt' in formats: fmt_flags.append('-ovtt')
    if 'srt' in formats: fmt_flags.append('-osrt')
    if 'txt' in formats: fmt_flags.append('-otxt')

    cmd = [
        str(WHISPER_EXEC), "-m", str(MODEL_PATH), "-f", str(audio_path),
        *fmt_flags, "-pc", "-t", "8", "-bs", "4", "-bo", "4", "-et", "2.4",
        *vad_args,
        "-mc", "1024", "-ml", "256",
        "--prompt", INITIAL_PROMPT,
    ]
    subprocess.run(cmd, env=env)

    # whisper.cpp appends the extension to the full input filename (e.g. temp_audio.wav.srt)
    success = False
    for fmt in formats:
        whisper_out = audio_path.with_name(f"{audio_path.name}.{fmt}")
        if whisper_out.exists():
            shutil.move(str(whisper_out), str(base_path.with_suffix(f'.{fmt}')))
            success = True
    return success


def run_whisper_python(audio_path, base_path, formats, model):
    """Windows / Mac-fallback: transcribe with a pre-loaded openai-whisper model."""
    try:
        import torch
        fp16 = torch.cuda.is_available()
    except ImportError:
        fp16 = False

    print(f"   🤖 Transcribing ({'GPU/fp16' if fp16 else 'CPU — this may take a while'})...")

    result = model.transcribe(
        str(audio_path),
        language="en",
        fp16=fp16,
        verbose=True,
        beam_size=4,
        best_of=4,
        temperature=0.0,
        initial_prompt=INITIAL_PROMPT,
        compression_ratio_threshold=2.4,
        no_speech_threshold=0.6,
        condition_on_previous_text=True,
    )

    segments = result["segments"]

    if 'vtt' in formats:
        with open(base_path.with_suffix('.vtt'), 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            for seg in segments:
                f.write(f"{_fmt_ts(seg['start'])} --> {_fmt_ts(seg['end'])}\n")
                f.write(f"{seg['text'].strip()}\n\n")

    if 'srt' in formats:
        with open(base_path.with_suffix('.srt'), 'w', encoding='utf-8') as f:
            for i, seg in enumerate(segments, 1):
                f.write(f"{i}\n")
                f.write(f"{_fmt_ts_srt(seg['start'])} --> {_fmt_ts_srt(seg['end'])}\n")
                f.write(f"{seg['text'].strip()}\n\n")

    if 'txt' in formats:
        with open(base_path.with_suffix('.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(seg['text'].strip() for seg in segments))

    return True


# ==============================================================================
# FILE PROCESSING
# ==============================================================================

def process_file(file_path, formats, whisper_model=None):
    """Extracts audio via FFmpeg, then routes to the appropriate Whisper engine."""
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    print("-" * 50)
    print(f"⚙️  Processing: {file_path.name}")

    temp_wav = file_path.with_name(f"temp_audio_{file_path.stem}.wav")

    print("   ⏳ Extracting audio via FFmpeg...")
    subprocess.run([
        "ffmpeg", "-i", str(file_path),
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        "-y", str(temp_wav), "-loglevel", "error"
    ])

    if WHISPER_CPP_AVAILABLE:
        success = run_whisper_cpp(temp_wav, file_path, formats)
    else:
        success = run_whisper_python(temp_wav, file_path, formats, whisper_model)

    if success:
        for fmt in sorted(formats):
            out = file_path.with_suffix(f'.{fmt}')
            if out.exists():
                print(f"   ✅ Saved: {out.name}")
    else:
        print(f"   ❌ Transcription failed for {file_path.name}.")

    if temp_wav.exists():
        temp_wav.unlink()


# ==============================================================================
# FILE SELECTION
# ==============================================================================

def scan_and_menu():
    """Scans cwd for media files and presents an interactive selection menu."""
    cwd = Path.cwd()
    candidates = [f for f in cwd.iterdir() if f.is_file() and f.suffix.lower() in MEDIA_EXTENSIONS]

    if not candidates:
        print(f"\n📭 No media files found in {cwd}")
        return []

    print("\n📋 Found the following media files:")
    for idx, f in enumerate(candidates, 1):
        print(f"  [{idx}] {f.name}")
    print("  [A] All files")
    print("  [Q] Quit")

    while True:
        choice = input("\nSelect a file to transcribe (number, A, or Q): ").strip().lower()
        if choice == 'q':
            print("🛑 Exiting.")
            sys.exit(0)
        elif choice == 'a':
            return candidates
        elif choice.isdigit() and 1 <= int(choice) <= len(candidates):
            return [candidates[int(choice) - 1]]
        else:
            print("⚠️  Invalid choice. Please enter a valid number, 'A', or 'Q'.")


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    files_to_process = ([Path(arg) for arg in sys.argv[1:]]
                        if len(sys.argv) > 1 else scan_and_menu())

    if not files_to_process:
        sys.exit(0)

    formats = select_output_format()

    # Load Python whisper model once before the loop (skipped on Mac with whisper.cpp)
    whisper_model = None
    if not WHISPER_CPP_AVAILABLE:
        model_name = select_python_model()
        print(f"\n📦 Loading '{model_name}' model (may download on first run)...")
        try:
            import whisper  # type: ignore[import-untyped]
            whisper_model = whisper.load_model(model_name)
        except ImportError:
            print("❌ openai-whisper not installed. Run: pip install openai-whisper torch")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)
        engine_label = f"openai-whisper [{model_name}]"
    else:
        engine_label = f"whisper.cpp [{MODEL_PATH.stem}]"

    fmt_label = ', '.join(f.upper() for f in sorted(formats))
    print(f"\n🚀 Starting Transcription Queue  [{engine_label}]  [{fmt_label}]\n")

    for f in files_to_process:
        process_file(f, formats, whisper_model=whisper_model)

    print("-" * 50)
    print("\n🎉 All finished!\n")
