# Example 02 — Software Tutorial Walkthrough

**What this demonstrates:** How a tuned prompt improves accuracy on technical
terminology, CLI commands, file paths, and product names that Whisper commonly
garbles (e.g. "V T T" instead of "VTT", "whisper" instead of "Whisper",
misheard flag names or path separators).

---

## INITIAL_PROMPT to Use

```
This is a software tutorial video. The presenter walks through step-by-step
instructions using technical terminology, file paths, and command-line tools.
References include Python, Whisper, FFmpeg, virtual environments, and VTT files.
Preserve exact capitalization for all product names, commands, and technical terms.
```

---

## Recording Script

*Read in a clear, measured tutorial pace — as if walking a beginner through
a setup process on screen. Aim for 70 to 85 seconds.*

---

Alright, let's walk through how to transcribe your first file using AI Transcriber.

First, make sure your virtual environment is activated. On Windows, run
`venv_win\Scripts\activate` in your terminal. On Mac, it's
`source venv_mac/bin/activate`.

Once you're in, type `python ai_transcriber.py` and hit Enter. The script will
scan your current folder and list any audio or video files it finds.

If you have multiple files, you can type A to process all of them at once, or
enter the number next to the file you want to start with.

On Windows, you'll see a model selection menu first. I recommend starting with
Turbo — it gives you the best balance of speed and accuracy without requiring
a huge amount of RAM.

The script extracts the audio track using FFmpeg, runs it through Whisper, and
saves two output files: a dot-vtt file in WebVTT format for subtitle players,
and a dot-txt file with timestamped text you can read directly in any editor.

Both files are saved alongside your original recording. That's it — pretty
straightforward once the environment is set up.

---

## Output Files

After transcribing, save your outputs here with these names:

| File | Description |
|------|-------------|
| `02_software_tutorial_no_prompt.vtt` | Transcribed with `INITIAL_PROMPT = ""` |
| `02_software_tutorial_no_prompt.txt` | Transcribed with `INITIAL_PROMPT = ""` |
| `02_software_tutorial_tuned.vtt` | Transcribed with the prompt above |
| `02_software_tutorial_tuned.txt` | Transcribed with the prompt above |

## What to Look For

Compare how Whisper handles these words across the two runs:

- `FFmpeg` / `Whisper` / `Python` — correct product name casing?
- `VTT` / `WebVTT` — rendered as an acronym or spelled out oddly?
- `venv_win` / `venv_mac` / `ai_transcriber.py` — file and folder names intact?
- `Turbo` — recognized as a model name rather than a generic adjective?
- Path separators (`\` on Windows, `/` on Mac) — handled correctly in context?
