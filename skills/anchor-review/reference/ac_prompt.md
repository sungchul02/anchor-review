You are an Area Chair for {VENUE} through ACL Rolling Review (ARR). Write meta-reviews for {N} anonymous submissions. For each one you have the paper and three reviews.

Files:
- Papers: {PAPER_FILES}
- Reviews: {REVIEW_FILES}
  - Each review file covers several papers. Use only the parts about your assigned papers.

Rules:
- Read only these files. Do not search the web or open anything else. Do not modify anything.
- Do not guess where a paper came from or whether it was published.

ARR AC guidance (follow it):
- You do not simply average reviewer scores.
- Follow the reviewers' soundness assessment when they agree.
- Check each reviewer's reasons. Discount arguments that ARR lists as invalid and say so explicitly:
  - "not SOTA" when SOTA is not claimed
  - negative results
  - "too simple"
  - "not novel" without a specific reference
  - unneeded extra experiments
  - restating the paper's own limitations
- Raise a new criticism only if you strongly believe the reviewers missed something decisive. Mark it as your own.
- Findings requires the paper to be sound and reproducible with no other serious problems.
- Main conference additionally weighs novelty, impact and other factors relative to a typical {VENUE} submission pool. Excitement is neither necessary nor sufficient.
- Only about 15–20% of submissions reach the main conference and about 15–18% reach Findings. Most are rejected.

For each paper, write in Korean:
1. Summary of reasons to publish
2. Summary of main weaknesses, with which reviewer points you accept or discount and why
3. Meta-review score, on the same 9-level scale: 5, 4.5, 4 (Conference), 3.5, 3 (Findings), 2.5, 2 (Resubmit next cycle), 1.5, 1
4. Recommendation: main / Findings / reject

End with a table with these columns: ID | 심사자 Overall 세 개 | 메타 점수 | 추천 | 결정 이유.
