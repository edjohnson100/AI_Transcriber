# Examples

This folder contains recording scripts and their resulting transcription outputs, demonstrating both transcription quality and the impact of a tuned `INITIAL_PROMPT`.

## How to Use These Scripts

1. Read through the script to get comfortable with it.
2. Record yourself reading it — 60 to 90 seconds, any decent microphone works.
3. Save the audio file into the project root folder.
4. Run the transcription **twice**: once with no prompt, once with the provided prompt.

**Run with no prompt:** temporarily set `INITIAL_PROMPT = ""` in `ai_transcriber.py`, then:
```bash
python ai_transcriber.py "your_recording.m4a"
```
Rename the output files to `*_no_prompt.vtt` / `*_no_prompt.txt` before the second run.

**Run with the tuned prompt:** paste the provided prompt into `INITIAL_PROMPT`, then run again.

5. Drop all four output files (two `.vtt`, two `.txt`) into this folder alongside the script.

---

## Examples in This Folder

| Script | Demonstrates |
|--------|-------------|
| [01_business_meeting.md](01_business_meeting.md) | Business jargon, acronyms, proper nouns (Salesforce, Jira, OKRs) |
| [02_software_tutorial.md](02_software_tutorial.md) | Technical terms, file paths, product names, CLI commands |
