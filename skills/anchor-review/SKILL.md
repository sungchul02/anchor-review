---
name: anchor-review
description: Blind mock peer review of a manuscript for *ACL venues (ACL, EMNLP, NAACL via ARR), calibrated by mixing the manuscript with same-field "anchor" papers whose outcome is known (main conference, Findings, arXiv-only/not accepted). The first use for a venue and field builds and saves a calibrated profile; later reviews reuse it. Users who skip setup get the built-in default criteria. Use when the user asks for a mock review, a blind review, an ARR-style assessment, or "would this get into ACL/EMNLP/NAACL/Findings".
---

# anchor-review

The idea: absolute LLM review scores are unreliable, but their *ordering* is informative. So the target manuscript is
reviewed blind together with papers whose fate is known. The result is reported as a position relative to those anchors.

## Choose the mode first

Run `python scripts/profiles.py list`. Profiles are saved in `~/.claude/anchor-review/profiles/`.

| Situation | Mode |
|---|---|
| A profile exists for the user's venue and field | **B. Review with the saved profile** (normal case) |
| No profile, and the user agrees to the one-time setup | **A. Setup**, then B |
| No profile, and the user does not want setup ("just review it", "use the default") | **C. Default** |

- If there is no profile, ask once: explain that setup collects about 24 anchors and runs about 15 reviewer subagents one time. After that, each review needs only about 6 reviewers.
- If the user declines, use C and say that the result is uncalibrated for their field.
- Never run setup without the user's agreement.

## A. Setup (once per venue × field)

**0. Criteria.**
- For *ACL venues through ARR, use `reference/arr_criteria.md` and `reference/reviewer_prompt.md` as they are.
- For another venue:
  - research its official review form, score definitions, reviewer guidelines and CFP
  - write a criteria file with sources
  - adapt a copy of the reviewer prompt: its scales and its valid/invalid reasons
  - keep the significance step, severity calibration and hiding rules

**1. Anchors.** Follow `reference/build_anchors.md`:
- 8 MAIN, 8 FINDINGS and 8 ARXIV-ONLY papers in the user's topic
- ARXIV-ONLY status verified (arXiv metadata, Semantic Scholar, OpenAlex, Anthology title match, web search)
- a confidential `key.md`

Optionally also build a held-out 4+4+4 set.

**2. Blind copies.** Use `scripts/extract.py`, `anon.py`, `clean.py` and `strip.py` (see "Blind copies" below).

**3. Calibration run.**
- Run `python scripts/assign.py <anchor_subs> <run> <prompt> --per 5 --seed 1`.
- Launch one reviewer subagent per task (see "Reviewers" below).
- Run `python scripts/aggregate.py <run>/reviews key.md --target NONE`.
- **The reliability AUC (accepted vs arXiv-only) must be ≥ 0.75.** If it is lower, look for leaked cues before changing the prompt. A changed prompt is a new version and needs the held-out set.

**4. Save.**
```
python scripts/profiles.py save <name> --venue "<venue>" --field "<field>" --subs <anchor_subs> --key key.md --reviews <run>/reviews [--prompt <prompt>]
```
- `<name>` is short, e.g. `acl-arr__rag`.
- The profile stores the anchors, key, prompt, calibration reviews and the per-class score distribution.
- It is local only. Never publish it, because it holds other people's paper texts.

Then continue with B for the user's manuscript.

## B. Review with a saved profile

1. **Blind copy of the target** (see "Blind copies"). Give it a fresh 4-letter ID that is not in the profile key.
2. **Sample anchors and the target into a new folder:**
   ```
   python scripts/profiles.py sample <name> <run>/subs --targets paper_ABCD.md --per-class 3 --seed <n>
   ```
   - This makes 9 anchors plus the target.
   - Anchors stay in the batch so that reviewers judge the target in context. They also give a fresh reliability check.
3. **Assign reviewers:** `python scripts/assign.py <run>/subs <run> ~/.claude/anchor-review/profiles/<name>/reviewer_prompt.md --per 5 --seed <n>`. With 10 papers this is 6 reviewers.
4. **Run the reviewers** (see "Reviewers").
5. **Aggregate:**
   ```
   python scripts/aggregate.py <run>/reviews ~/.claude/anchor-review/profiles/<name>/key.md --target ABCD --profile ~/.claude/anchor-review/profiles/<name>/profile.json
   ```
   - Report the target's rank and position **against the profile** (all calibrated anchors). This is the main result, e.g. "rank 7–14 of 37".
   - Also report the position within this run, as a consistency check.
   - **Always show the ranking table** that aggregate.py prints at the end. It has the columns 순위, ID, 구분, 평균 Overall, 심사자별 점수, Soundness and 결정 이유, with one line per reviewer. Put the target's row first in your summary, then the full table.

## C. Default (no setup)

Use the built-in criteria and score bands of `presets/acl-arr_rag.md`. They were calibrated for ARR × RAG/compression/multi-hop QA.
1. Make the blind copy of the target.
2. Put it alone in a folder and run `assign.py` with `reference/reviewer_prompt.md` and `--per 1`. This gives 3 reviewers.
3. Read the mean Overall with the preset's bands:
   - ≥ 3.0: accepted range
   - 2.5–2.99: borderline
   - < 2.5: likely not accepted as is
4. Say clearly in the report:
   - no anchors were used
   - the bands come from another field's calibration
   - setup (mode A) would give a calibrated position

## Blind copies (all modes)
- Every paper must have the same Markdown form:
  - `# Paper XXXX` / `## Title` / title / `## Abstract` / body
  - the appendix is kept and the references are dropped
- Remove authors, affiliations, venue headers, acknowledgments, arXiv stamps and identifying URLs.
- `strip.py` removes the Limitations, Ethics and AI-use sections, which leak the class. Remove by hand any leftovers it flags.
- **Target paper.** Rename an identifying method name or self-citation consistently, e.g. "Author et al. (year)" → "prior work (year)". Replace placeholder markers with current values. Never change a claim.
- Use a neutral folder name (e.g. `arr2027/subs/`). It must not reveal the purpose.

## Reviewers (all modes)
- Launch one subagent per task file with only this brief: "Your reviewing assignment is in `<task file>`. Read that file first and follow it exactly. Do not open any other file except the submissions it lists. When done, reply with only the final summary table."
- **Do not tell reviewers:**
  - the purpose of the review
  - that a target paper is included
  - that some papers are published
  - any earlier scores
- No web search. If a reviewer breaks a rule, discard that review and rerun the task.
- Optional area chair: `reference/ac_prompt.md` (fill its placeholders by hand). Aggregate with `--ac <dir>`.

## What it can and cannot tell
- The default profile (ARR × RAG, 36 anchors) separates **accepted vs arXiv-only**:
  - AUC 0.84 on the tuning set
  - AUC 0.89 on the held-out set
  - AUC 0.86 on all 36
- It **cannot** separate main from Findings: AUC 0.30–0.63. That split depends on area-chair quotas and reviewer noise (α≈0.3).
- Report "accepted range or not" and the percentile against each anchor class. Never give a confident main/Findings verdict.
- Write the report in the user's language. The reviews are in Korean by default; change the language line in the prompt if needed.

## How many papers
| Purpose | Anchors | Reviewer subagents (≈) |
|---|---|---|
| Setup, minimum | 5 + 5 + 5 | 9 |
| Setup, recommended | 8 + 8 + 8 | 15 |
| Setup with held-out validation | + 4 + 4 + 4 | +9 |
| Each later review (mode B) | 3 + 3 + 3 sampled, plus the target | 6 |
| Default (mode C) | none | 3 |

## Files
- `reference/reviewer_prompt.md`: v2 reviewer prompt (frozen). It has the ARR scales, a significance step, severity calibration, and the valid and invalid reasons.
- `reference/ac_prompt.md`: meta-review prompt.
- `reference/arr_criteria.md`: sources for every rule.
- `reference/build_anchors.md`: how to build and verify anchors.
- `presets/acl-arr_rag.md`: default criteria and score bands (mode C), plus the calibration record.
- `presets/domestic-kr.md`: Korean domestic venues (prompt only, uncalibrated).
- `scripts/`: `extract.py`, `anon.py`, `clean.py`, `strip.py`, `assign.py`, `aggregate.py`, `profiles.py`. See `scripts/README.md`.
- `~/.claude/anchor-review/profiles/<name>/`: saved profiles (local only).

## Changing the prompt
- Do not edit `reviewer_prompt.md` to make one manuscript look better.
- Any change is a new version. Re-run setup steps 3–4 for it, and validate it on a held-out set.
