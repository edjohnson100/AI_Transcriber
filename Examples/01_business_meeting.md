# Example 01 — Business Meeting Update

**What this demonstrates:** How a tuned prompt dramatically improves accuracy on
business jargon, acronyms, and tool names that Whisper commonly mishears or
lowercases (e.g. "okrs" instead of "OKRs", "salesforce" instead of "Salesforce").

---

## INITIAL_PROMPT to Use

```
This is a recorded business meeting. Attendees are discussing Q3 results, OKRs,
project roadmaps, and action items. Speakers may reference tools like Salesforce,
Jira, Slack, Confluence, and DevOps pipelines. Use professional capitalization
and punctuation throughout.
```

---

## Recording Script

*Read naturally, as if giving a status update to your team on a Zoom call.
Aim for a conversational pace — about 60 to 75 seconds.*

---

Okay everyone, let me give you a quick update on where we stand heading into Q3.

So, we wrapped up the Salesforce integration last week — big win for the team.
The data is now flowing cleanly into the pipeline and our KPIs are looking much
stronger than they did at the Q2 review.

On the Jira board, we've got three OKRs still in progress. The first two are on
track to close by end of sprint. The third — the stakeholder reporting dashboard
— has slipped a bit. We're working with the UX team to finalize the wireframes,
and I'm expecting sign-off by Thursday.

For action items coming out of today: Sarah needs to update the Confluence page
with the new workflow, and Marcus should loop in DevOps about the staging
environment before we push to production.

I'll drop a full written summary in Slack by end of day. Any questions before we
move on?

---

## Output Files

After transcribing, save your outputs here with these names:

| File | Description |
|------|-------------|
| `01_business_meeting_no_prompt.vtt` | Transcribed with `INITIAL_PROMPT = ""` |
| `01_business_meeting_no_prompt.txt` | Transcribed with `INITIAL_PROMPT = ""` |
| `01_business_meeting_tuned.vtt` | Transcribed with the prompt above |
| `01_business_meeting_tuned.txt` | Transcribed with the prompt above |

## What to Look For

Compare how Whisper handles these words across the two runs:

- `OKRs` / `KPIs` / `Q3` / `Q2` — does it capitalize correctly?
- `Salesforce` / `Jira` / `Slack` / `Confluence` — does it recognize product names?
- `DevOps` — does it render as one word with correct casing?
- Punctuation — does the tuned version produce cleaner sentence breaks?
