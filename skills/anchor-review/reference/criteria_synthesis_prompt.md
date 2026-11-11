You are writing venue-specific review criteria from analyses of real papers with known outcomes.

Inputs (read only these files, and do not search the web):
- Per-class analyses: {ANALYSES}
  - Each file covers papers that share one outcome and ends with a "Common pattern" section.
- Official criteria and acceptance rates: `{CRITERIA_SOURCES}`
- Reviewer tiers: `{TIERS}` (use the entry "{TARGET}")

Task: for each tier in the tiers file, write one criteria file `{OUT_DIR}/tier_<tier>_<venue first word>.md`, in Korean. For the default ACL tiers the files are `tier_target_ACL.md`, `tier_peer_EMNLP.md` and `tier_lower_COLING.md`. Each file describes what a paper must show to reach each score at THAT venue, grounded in the analyses.

Each file must contain:
1. **이 학회의 기준선.**
   - The acceptance rate, with its source.
   - Which observed outcome classes would typically be accepted here. For example, at COLING most papers like the Findings examples and many like the COLING examples are accepted, while at ACL main only papers like the MAIN examples are.
2. **점수별 기준표** for Overall 4, 3.5, 3, 2.5, 2 and ≤1.5.
   - For each score, give observable characteristics: contribution type and size of step, evidence breadth, and the flaws that are tolerable versus disqualifying.
   - Base every row on patterns from the analyses. Cite which class the pattern came from and how many papers showed it.
3. **이 학회에서 결정적이었던 특징**: 3–6 bullets. Example: "새 현상·문제 정의 + 여러 모델에서 일관됨 → main".
4. **탈락 쪽 신호**: the patterns typical of the ARXIV-ONLY class. Mark which ones the analyses showed to be disqualifying, and which ones accepted papers also had.
5. **주의.** Keep the official ARR rules:
   - the H1–H17 invalid reasons stay invalid
   - "not SOTA" is not a reason unless SOTA is claimed
   - severity calibration applies

Constraints:
- Never mention paper titles, IDs, author names or system names from the analyses. Describe features only, because reviewers must not recognize specific papers.
- Keep each file under about 900 words.
- Be honest about thin evidence. For example, the COLING class has only a few papers. Say how many.

Finally, write `{OUT_DIR}/README.md` (under about 300 words). It states:
- which analyses and how many papers per class the criteria came from
- the date
- that the files were generated from known-outcome papers and should be rebuilt when the venue or field changes
