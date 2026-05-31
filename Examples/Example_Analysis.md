# Example Analysis

This folder includes paired transcription outputs for two sample recordings: a business meeting script and a software tutorial script. The goal is to compare how the transcriber behaves with a blank prompt (`INITIAL_PROMPT = ""`) versus a tuned prompt.

## What we saw

### 01_business_meeting
- Both the blank-prompt output and the tuned-prompt output were very good.
- The meaning stayed the same in both versions.
- The tuned prompt produced slightly cleaner punctuation and casing, but there were no major errors in the no-prompt version.

### 02_software_tutorial
- The tuned prompt produced a clean, complete transcript.
- The blank-prompt output started well, but then added a repeated noise artifact: many lines of `You can click on the link.` after the transcript should have ended.
- That shows the no-prompt approach can still fail on real speech even when the early portion looks correct.

## What this means for you

- A blank initial prompt can work for some recordings, especially if the speech is clear and simple.
- However, it is not consistently reliable across different audio content.
- The tuned `INITIAL_PROMPT` offers better robustness and fewer transcription artifacts.

## Recommendation

For distribution and general use, keep the tuned prompt enabled by default. Use the blank prompt only for quick experiments or controlled demos where you are already comparing prompt behavior.

## Practical takeaway

- If you want consistent results across multiple recordings, use the tuned prompt.
- If you are evaluating how the model behaves in a no-prompt mode, compare outputs side-by-side and watch for repeated text, dropped segments, or other noise.

## Files included in this example set

- `01_business_meeting.md`
- `01_business_meeting_no_prompt.vtt` / `.srt` / `.txt`
- `01_business_meeting_tuned.vtt` / `.srt` / `.txt`
- `02_software_tutorial.md`
- `02_software_tutorial_no_prompt.vtt` / `.srt` / `.txt`
- `02_software_tutorial_tuned.vtt` / `.srt` / `.txt`

These files together demonstrate the value of a tuned prompt for stable transcription results.