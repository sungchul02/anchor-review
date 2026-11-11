---
name: anchor-review
description: Blind mock peer review of a manuscript for *ACL venues (ACL, EMNLP, NAACL via ARR). The manuscript is mixed into a 10-paper bundle with same-field "anchor" papers whose outcome is known (main conference, Findings, accepted at a less selective venue, arXiv-only). Three reviewers, one per venue tier (the target venue, a peer venue of the same level, a slightly easier venue), each review the whole bundle. Output is a ranking with scores and reasons, plus a detailed review of the manuscript. Phase 1 builds venue-tier criteria from real papers with known outcomes; phase 2 runs the blind review with them. Users can run the shipped defaults directly or customize venues, paper counts, tiers and bundle size in config. Use when the user asks for a mock review, a blind review, an ARR-style assessment, or "would this get into ACL/EMNLP/NAACL/Findings".
---

# anchor-review

Absolute LLM review scores are unreliable, but rankings are informative. So the manuscript is read blind inside a bundle of papers whose fate is known, by reviewers set to different venue levels.

## Default setup (what a run looks like)

| Item | Default |
|---|---|
| Bundle | **10 papers**: the target plus 9 anchors (3 MAIN, 2 FINDINGS, 2 COLING-accepted, 2 ARXIV-ONLY; 3/3/3 if there are no COLING anchors) |
| Reviewers | **3, one per tier**, each reading **all 10 papers** in its own random order (`presets/tiers.json`) |
| Tiers for target ACL | target: ACL · peer (same level): EMNLP · lower (slightly easier): COLING |
| Scoring | every reviewer scores every paper; a paper's score is the **mean of the 3 reviewers**, and ranking and reading use that mean |
| Output | (1) ranking table: rank, ID, class, mean score, each tier's score, decisive reasons; (2) target's rank against the saved profile; (3) a detailed review of the target |

Change the target venue with `--target-venue` (keys in `presets/tiers.json`; add your own). Change the bundle with `profiles.py sample --mix`.

## Two phases

1. **Build criteria (once per venue × field).**
   - Read papers whose outcome is known, *with* their labels, and write one criteria file per reviewer tier. This is phase 1.
2. **Blind review (each manuscript).**
   - Mix the manuscript with anchors under hidden names.
   - Every tier reviewer reads the whole bundle with its tier's criteria.
   - Average the scores and analyze the result. This is phase 2.

Settings live in `config/default.json`. A user copy at `~/.claude/anchor-review/config.json` overrides any key: target venue, field, papers per class for phase 1, bundle size and mix, tiers file, criteria folder and score bands.

## Choose the path first

| Situation | Path |
|---|---|
| The user is fine with the defaults (ACL tiers × RAG field) | **Default:** use the shipped criteria `presets/criteria/acl-rag/`, then go to phase 2 |
| The user wants another venue, field, paper counts, tiers or bundle size | **Custom:** edit the config, run phase 1, then phase 2 |
| Saved criteria and a profile exist for that venue × field (`profiles.py list`) | Go straight to phase 2 |

- Phase 1 costs about 4 analyst subagents plus 1 synthesis subagent, with about 40 papers read once.
- Phase 2 costs one reviewer subagent per tier, each reading the whole bundle. The default is 3 reviewers × 10 papers.
- Before running phase 1, state the cost and ask the user once.

## Phase 1. Build criteria

1. **Anchors.**
   - Collect papers per class as set in `criteria_building.anchors_per_class`. The default is 12 MAIN, 12 FINDINGS, 6 COLING and 12 ARXIV-ONLY, in the user's field.
   - Follow `reference/build_anchors.md`, which includes verifying that ARXIV-ONLY papers have no publication record.
   - Make anonymized copies with `extract.py`, `anon.py`, `clean.py` and `strip.py`.
   - Write a confidential `key.md`.
2. **Venue facts.**
   - Each tier in `presets/tiers.json` needs a sourced acceptance rate and scale meaning.
   - For a venue that is not listed, research its official review form, guidelines, CFP and acceptance rate, and add an entry.
3. **Analysts, one per class.**
   - Fill `reference/criteria_analyst_prompt.md` with {N}, {DIR} (that class's papers), {CLASS_DESC}, {FIELD} and {OUT}.
   - Run one subagent per class. Each reads its papers with the outcome known and writes per-paper notes plus a "Common pattern" section with counts.
4. **Synthesis.**
   - Fill `reference/criteria_synthesis_prompt.md` with the analyses, `reference/arr_criteria.md`, the tiers file, the target key and the output folder.
   - Run one subagent. It writes `tier_<tier>_<venue>.md` for each tier plus `README.md`.
   - The files contain no paper titles or IDs.
   - Check this with a search before use.
5. **Profile (optional, for ranking against all anchors).**
   - Run `profiles.py save` with the anchors, the key and any calibration reviews.
   - Keep the profile local only, because it holds other people's papers.

## Phase 2. Blind review

1. **Target copy.** Make the blind copy of the target with a fresh 4-letter ID (see "Blind copies").
2. **Bundle.**
   - With a profile, run `python scripts/profiles.py sample <name> <run>/subs --targets paper_ABCD.md --seed <n>`. This gives the default 9 anchors plus the target. Set `--mix` from `review.bundle_mix`.
   - Without anchors (the shipped default criteria only), the bundle is the target alone.
     - The scores are then read with the bands.
     - There is no ranking.
3. **Assign.**
   ```
   python scripts/assign.py <run>/subs <run> reference/reviewer_prompt.md --tiers presets/tiers.json --target-venue ACL --criteria-dir <criteria folder> --seed <n>
   ```
   This produces one task per tier, each covering the whole bundle, with that tier's criteria inserted.
4. **Reviewers.** Run one subagent per task (see "Reviewers").
5. **Aggregate.**
   - Run `python scripts/aggregate.py <run>/reviews <key.md> --target ABCD [--profile <profile>/profile.json]`.
   - Then run `python scripts/extract_target.py <run>/reviews ABCD <run>/target_reviews.md`.
6. **Report, in this order:**
   1. **The target's row:**
      - its rank in the bundle
      - its rank against the profile (e.g. "5–7 of 37")
      - its mean score and each tier's score
      
      Read the scores with `review.score_bands`:
      - ≥ 3.0: accepted range
      - 2.5–2.99: borderline
      - < 2.5: likely not accepted as is
   2. **The full ranking table** (mean, each tier's score, each tier's reason).
   3. **A detailed review of the target**, synthesized from `target_reviews.md`:
      - summary
      - significance per tier
      - each central claim and its evidence verdict per tier
      - strengths
      - weaknesses (major or minor, with sections)
      - the reviewers' questions
      - what would raise the score
      - where the tiers disagree
   4. **Reliability:**
      - the bundle AUC and the per-tier AUC lines
      - any tier below 0.75 is weak in this run
      - any anchor class that the tier misjudged, e.g. accepted COLING anchors scored as rejects by the COLING reviewer
7. Save the report where the user keeps review notes.

## Blind copies (all modes)
- Every paper gets the same Markdown form:
  - `# Paper XXXX` / `## Title` / title / `## Abstract` / body
  - the appendix is kept and the references are dropped
- Use `scripts/extract.py`, `anon.py`, `clean.py` and `strip.py`. Remove by hand the leftovers that `strip.py` flags.
- Remove authors, affiliations, venue headers, acknowledgments, arXiv stamps and identifying URLs.
- **Target paper.** Rename an identifying method name or self-citation consistently, e.g. "Author et al. (year)" → "prior work (year)". Replace placeholder markers with current values. Never change a claim.
- Use a neutral folder name, e.g. `arr2027/subs/`.

## Reviewers (all modes)
- Launch one subagent per task file with only this brief: "Your reviewing assignment is in `<task file>`. Read that file first and follow it exactly. Do not open any other file except the submissions it lists. When done, reply with only the final summary table."
- **Reviewers work paper by paper.** They append each paper's review to their file before opening the next paper, so a long bundle does not overflow their context.
- **Do not tell reviewers:**
  - the purpose of the review
  - that a target paper is included
  - that some papers are published
  - any earlier scores
- No web search. If a reviewer breaks a rule or skips papers, discard that review and rerun the task.

## What it can and cannot tell
- **Earlier calibration** (ARR × RAG, split batches of 5, 36 anchors):
  - accepted vs arXiv-only: AUC 0.84 on tuning, 0.89 on held-out
  - main vs Findings: not separable
- **First run of the two-phase tiered protocol** (default criteria, 10-paper bundle, 3 tiers):
  - bundle AUC accepted vs arXiv-only: 0.79
  - per tier: EMNLP 0.96, COLING 0.68, ACL 0.64
  - Known weakness: the COLING tier criteria came from only 6 papers. In that run they scored two real COLING-accepted anchors as rejects.
  - Treat results from the COLING tier as provisional until its criteria are rebuilt from more papers.
- Report "accepted range or not" and the rank. Never give a confident main/Findings verdict.

## Files
- `config/default.json`: all defaults (venue, field, papers per class, bundle, tiers, criteria folder, score bands). The user copy goes to `~/.claude/anchor-review/config.json`.
- `presets/criteria/acl-rag/`: shipped phase-1 criteria for the ACL / EMNLP / COLING tiers in the RAG field. They contain no paper titles.
- `presets/tiers.json`: reviewer tiers per target venue, with sourced acceptance rates.
- `presets/acl-arr_rag.md`: score bands and the earlier calibration record.
- `presets/domestic-kr.md`: Korean domestic venues (uncalibrated).
- `reference/criteria_analyst_prompt.md` and `reference/criteria_synthesis_prompt.md`: the phase-1 prompts.
- `reference/reviewer_prompt.md`: the phase-2 reviewer prompt (v3). It has slots for the venue note and the tier criteria, writes paper by paper, and keeps the ARR scales, the significance step, the severity calibration and the valid/invalid reasons.
- `reference/reviewer_prompt_v2.md`: the version validated in the earlier split-batch runs.
- `reference/ac_prompt.md`, `reference/arr_criteria.md`, `reference/build_anchors.md`.
- `scripts/`: `extract.py`, `anon.py`, `clean.py`, `strip.py`, `assign.py`, `aggregate.py`, `extract_target.py`, `profiles.py`. See `scripts/README.md`.

## Changing prompts, criteria or tier notes
- Never edit a prompt, criteria file or tier note to make one manuscript look better.
- Any change is a new version. Rebuild it from papers (phase 1), and check reliability on a bundle of anchors before relying on it.
