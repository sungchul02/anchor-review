# Preset: *ACL via ARR (ACL / EMNLP / NAACL) × RAG, context compression, multi-hop QA

Status: **calibrated and validated** (2026-11-12). This is the default preset.

## Setup used
| Item | Value |
|---|---|
| Venues | ACL 2027, EMNLP 2027, NAACL 2027 (one reviewer pass per venue, so 3 reviews per paper) |
| Criteria | `reference/arr_criteria.md` (ARR form, reviewer and AC guidelines, CFPs, acceptance rates) |
| Reviewer prompt | `reference/reviewer_prompt.md` (v2, frozen) |
| Tuning anchors | 24 papers: 8 MAIN (ACL'25, EMNLP'25, NAACL'25, ACL'26), 8 FINDINGS (same venues), 8 ARXIV-ONLY (posted 2024-08 to 2025-08). Key: `data/anchors_rag_acl_key.md` |
| Held-out anchors | 12 papers, 4 per class, not used for tuning. Key: `data/anchors_rag_acl_holdout_key.md` |
| Batch | 4–5 papers per reviewer |

## Results
| Metric | Tuning (24) | Held-out (12) |
|---|---|---|
| AUC, accepted (MAIN+FINDINGS) vs ARXIV-ONLY | 0.84 | **0.89** |
| AUC, MAIN vs FINDINGS | 0.30 | 0.63 (4 vs 4, not interpretable) |

Mean reviewer Overall per class across all 36 anchors:

| Class | n | Mean | Median | Range |
|---|---|---|---|---|
| MAIN | 12 | 2.81 | 2.75 | 2.0–3.83 |
| FINDINGS | 12 | 2.93 | 3.0 | 2.0–3.67 |
| ARXIV-ONLY | 12 | 2.18 | 2.08 | 1.5–3.0 |

Note that the absolute scores run lower than real ARR. Real reviewers average about 3.2. Read positions relative to the anchors, not raw scores.

## How to read a target's mean Overall (3 reviewers)
| Mean Overall | Reading | Basis |
|---|---|---|
| ≥ 3.0 | Accepted range | 11/12 ARXIV-ONLY anchors scored below 3.0 |
| 2.5 – 2.99 | Borderline: could go either way | 83% of accepted anchors are ≥ 2.5; 75% of ARXIV-ONLY are < 2.5 |
| < 2.5 | Likely not accepted as is | Only 4/24 accepted anchors scored below 2.5 |
| 3.5+ with significance "H" | Strongest anchors (main-level discoveries) sat here | Only the 2–3 best anchors reached it |

Always also give the share of each anchor class below the target. Never call main vs Findings.

## What separated the classes (from the reviews)
**Accepted anchors** typically had:
- consistent gains across several models, datasets or retrievers
- fair same-setting baselines
- a clear problem statement

The top-scoring anchors defined a new gap or phenomenon. Reviewers rated their significance "H". Example: a "memorization–utilization gap" fixed with RL.

**ARXIV-ONLY anchors** typically had one or more central-claim problems:
- **Metrics contradicting each other or the text.** Examples: EM > F1, an abstract number not found in any table.
- **Too narrow an evaluation.** A single dataset, a self-built test set, or a 200–500 item sample used for general claims.
- **Unfair comparisons.** Baselines copied from other papers, unequal LLM-call or token budgets, voting or ensembles used only by the proposed method.
- **Missing method details.** The loop LLM, prompts, or judging procedure is not given.
- **Claims the paper's own tables contradict.**

**The miss case.** Some accepted (even MAIN) anchors scored 2.0–2.5 for the same reasons. Example: undefined metrics plus an apparently broken baseline. The tool flags the weaknesses that a careful reviewer would raise. It cannot see the parts of real decisions that come from venue quotas or reviewer luck.

## Using this preset for your own field
- Keep the venue part (criteria and reviewer prompt) if you target *ACL.
- Replace the anchors: build 8/8/8 in your topic following `reference/build_anchors.md`, plus ideally 4/4/4 held out.
- Re-check the AUC on your anchors before trusting the target's position.
