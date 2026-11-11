# Preset: Korean domestic conferences (KSC, HCLT, ASK/KIPS, KCC) × RAG and LLM

Status: **prompt only, not calibrated.** No anchors with known outcomes yet.

## Setup used so far
| Item | Value |
|---|---|
| Venues | KSC 2026 (KIISE), HCLT 2026, ASK 2026 (KIPS); one reviewer per venue |
| Reviewer prompt | `presets/domestic-kr_reviewer_prompt.md` |
| What it rates | contribution, novelty, persuasiveness of results, usefulness to the domestic audience; then a verdict (accept, conditional accept, revise and resubmit, reject) and best-paper candidacy |
| Mixed with | 7 published domestic papers from the same area. Outcome labels are only "published", so there is no rejected class. |

## Observations (one manuscript, several versions)
- Scores were consistently higher than overseas reviews: 3–3.5 of 5, against 2.0–2.5 on the ARR scale.
- Verdicts were mostly "accept" or "conditional accept".
- Best-paper candidacy went to papers with direct domestic utility, such as Korean-language models or data, and to papers whose method clearly wins.
- The most common condition was "Korean data or Korean models are missing" (HCLT).

## To calibrate
Collect anchors with known outcomes:
- 6–8 papers that won best-paper awards (awards lists are public)
- 6–8 ordinary accepted papers
- If possible, 6–8 papers that were rejected and later published elsewhere. These are hard to verify; arXiv-only Korean preprints are rare.

Then measure whether the prompt separates award winners from ordinary accepted papers.
