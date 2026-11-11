---
name: anchor-review
description: Blind mock peer review of a manuscript for *ACL venues (ACL, EMNLP, NAACL via ARR), calibrated by mixing the manuscript with same-field "anchor" papers whose outcome is known (main conference, Findings, arXiv-only/not accepted). Reviewers follow the official ARR form and guidelines; the report says where the manuscript falls among the anchors and whether it is in the accepted range. Use when the user asks for a mock review, a blind review, an ARR-style assessment, or "would this get into ACL/EMNLP/NAACL/Findings".
---

# anchor-review

The idea: absolute LLM review scores are unreliable, but their *ordering* is informative. So the target manuscript is
reviewed blind together with papers whose fate is known. The result is reported as a position relative to those anchors.
In the same run, the anchors measure how well the reviewers separate the classes.

## What it can and cannot tell
Calibrated with v2 of the reviewer prompt on 24 anchor papers in RAG, compression and multi-hop QA (8 per class). Validated on 12 held-out anchors that were not used for tuning.
- **It can tell accepted papers (main or Findings) from arXiv-only papers.**
  - AUC 0.84 on the tuning set.
  - AUC 0.89 on the held-out set.
- **It cannot tell main from Findings.**
  - AUC 0.30.
  - The main/Findings split in real ARR depends on SAC quotas and reviewer noise (α≈0.3) more than on the text.
- Always report the target as "accepted range or not" plus a percentile against each anchor class. Never as a confident main/Findings verdict.

## Presets (defaults)
- **`presets/acl-arr_rag.md`**: *ACL via ARR × RAG, compression and multi-hop QA. This is the default.
  - Calibrated and validated: 36 anchors, held-out AUC 0.89.
  - Includes the score bands that tell how to read a target's mean.
- **`presets/domestic-kr.md`**: Korean domestic conferences (KSC, HCLT, ASK).
  - Prompt only; not calibrated.
- If the user names no venue or field, use the default and say so. Users can switch the venue, the field, or both. A changed field needs new anchors (step 1). A changed venue needs new criteria (step 0).

## How many papers
| Purpose | Anchors | Reviews |
|---|---|---|
| Minimum | 5 MAIN + 5 FINDINGS + 5 ARXIV-ONLY + target(s) | 3 per paper |
| Recommended (used in the default preset) | 8 + 8 + 8 + target(s) | 3 per paper, 4–5 papers per reviewer |
| New venue or prompt version | add a held-out set of 4 + 4 + 4 | 3 per paper |

- With 25 papers, 5 per batch and 3 venues, one run is 15 reviewer subagents. A held-out check of 12 papers is 9 more.
- Fewer than 5 per class makes the AUC too noisy to judge reliability.

## Steps

### 0. Venue criteria
- **For *ACL venues through ARR,** use `reference/arr_criteria.md` and `reference/reviewer_prompt.md` as they are.
- **For another venue** (NeurIPS, ICLR, CVPR, a journal, a domestic conference):
  - Research the venue's official review form, score definitions, reviewer guidelines and call for papers first.
  - Write a matching criteria file with sources.
  - Adapt the scales and the valid/invalid reasons in a copy of the reviewer prompt.
  - Keep the structure: the significance step, severity calibration, and the hiding rules.
  - Treat the copy as an unvalidated version until it passes the anchor check in step 5.

### 1. Anchors
- Build the anchor set for the target's own topic by following `reference/build_anchors.md`. The repository ships no paper list.
  - If you keep anchor keys from earlier runs locally, for example in `data/`, you may reuse them for the same field.
  - Never redistribute the anchor texts.
- A new set should have:
  - same topic as the target
  - 8 MAIN, 8 FINDINGS and 8 ARXIV-ONLY papers
  - ARXIV-ONLY status verified through arXiv metadata, Semantic Scholar, OpenAlex, Anthology title match and a web search
- Keep the key confidential. Reviewers must never see it.

### 2. Blind copies
- Convert every paper, the target included, to the same Markdown form:
  - `# Paper XXXX` / `## Title` / title / `## Abstract` / body
  - appendix kept, references dropped
  - Use `scripts/extract.py`, `scripts/anon.py` and `scripts/clean.py`.
- Remove authors, affiliations, venue headers, acknowledgments, arXiv stamps, identifying URLs and self-citations that reveal the authors.
- Run `scripts/strip.py` on all files. It removes Limitations, Ethics and AI-assistant sections, which otherwise leak the class. Also delete any AI-writing-assistant paragraph left inside an appendix.
- **Target paper.** If the user has a named method or prior paper that could identify them, rename it consistently, for example their method → a neutral name, and "Author et al. (year)" → "prior work (year)". Replace placeholder markers with their current values. Do not change any claim.
- Give every file a fresh random 4-letter ID. Put all files in one neutral folder, e.g. `arr2027/subs/`. The folder name must not reveal the purpose.

### 3. Reviewers
- Run `python scripts/assign.py <subs> <run_dir> reference/reviewer_prompt.md --per 5 --seed <n>`.
  - One pass per venue (ACL, EMNLP, NAACL), so each paper gets 3 independent reviews.
- Launch one subagent per task file. Brief each one only with: "Your reviewing assignment is in `<task file>`. Read that file first and follow it exactly. Do not open any other file except the submissions it lists. When done, reply with only the final summary table."
- **Do not tell reviewers:**
  - the purpose of the review
  - that a target paper is included
  - that some papers are published
  - the scores of earlier runs
- Reviewers may not search the web. If a reviewer breaks the rules (opens other files, searches, guesses provenance), discard that review and rerun the task.

### 4. Area chair (optional)
`reference/ac_prompt.md` turns three reviews into a meta-review and drops arguments that ARR lists as invalid. Give it the papers and the review files.

### 5. Aggregate
- Run `python scripts/aggregate.py <run_dir>/reviews <key.md> --target <ID>[,<ID>]`.
- Report:
  - the class means and AUCs for this run. If AUC accepted-vs-arXiv < 0.75, say that this run is not reliable.
  - each target's mean Overall and Soundness
  - the share of each anchor class scoring below the target
  - the recurring decisive reasons quoted from the reviews
- For the user's own language, translate the summary; the reviews themselves are written in Korean by default. Change the language line in `reference/reviewer_prompt.md` if needed.

## Files
- `reference/reviewer_prompt.md`: v2 reviewer prompt, frozen. It contains:
  - the ARR scales
  - a separate significance step
  - severity calibration
  - valid (R/M) and invalid (H) reasons
- `reference/ac_prompt.md`: meta-review prompt.
- `reference/arr_criteria.md`: sources for every rule (ARR form, reviewer and AC guidelines, CFPs, acceptance rates, empirical studies).
- `reference/build_anchors.md`: how to build and verify an anchor set.
- `scripts/`: `extract.py`, `anon.py`, `clean.py`, `strip.py`, `assign.py`, `aggregate.py`.
- `data/` (optional, local only): your own anchor keys from earlier runs.

## Changing the prompt
- Do not edit `reviewer_prompt.md` to make one manuscript look better.
- Any change is a new version. Re-measure it on the anchor set and on a held-out anchor set before using it.
