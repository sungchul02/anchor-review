# anchor-review

**Calibrated blind mock peer review for ACL / EMNLP / NAACL (ARR), as a Claude Code skill.**

[한국어 README](README.ko.md)

LLM reviewers give unreliable absolute scores, but they rank papers better than they score them. anchor-review
mixes your manuscript **blind** with same-field papers whose fate is known, then reports where your paper falls among them:
- *anchors* from the main conference
- *anchors* from Findings
- arXiv-only *anchors*, with no publication record

The same run also measures how well the reviewers separated the anchors. Each result therefore comes with its own reliability check.

| Default preset: ARR × RAG / context compression / multi-hop QA | Tuning set (24) | **Held-out set (12)** |
|---|---|---|
| AUC: accepted (main+Findings) vs arXiv-only | 0.84 | **0.89** |
| AUC: main vs Findings | 0.30 | 0.63 (n=4 vs 4) |

It **can** tell whether a paper looks like it belongs in the accepted range. It **cannot** tell main from Findings. That split depends on area-chair quotas and reviewer noise more than on the text, and the skill says so in every report.

## What it does

1. **Venue criteria.** Uses the official ARR review form and guidelines, with sources:
   - Soundness, Excitement and the 9-level Overall scale
   - "Findings = sound and reproducible; main = plus novelty and impact"
   - the reasons reviewers must not use, such as "not SOTA", "too simple" or "negative result"
   
   For other venues, it builds criteria from that venue's official form.
2. **Anchors.** Collects 8 main, 8 Findings and 8 arXiv-only papers in your topic. The arXiv-only status is verified via arXiv metadata, Semantic Scholar, OpenAlex, an ACL Anthology title match and a web search.
3. **Blind copies.** Converts every paper to the same Markdown format:
   - removes authors, venue headers and acknowledgments
   - removes Limitations, Ethics and AI-use sections, which leak the class
   - renames your method if it is identifiable
4. **Reviewers.** Three independent reviewer subagents per paper (ACL, EMNLP, NAACL). They follow the ARR scales, run a separate significance step, and grade flaws by severity. They are not told the purpose, that your paper is included, or that some papers are published.
5. **Report.** Gives your mean score, its percentile against each anchor class, the reliability AUC of the run, and the recurring decisive reasons.

## Three modes

| Mode | When | Cost |
|---|---|---|
| **Setup** (once per venue × field) | First use. Claude collects about 24 anchors in your field, runs a calibration review, and saves a local *profile* if the reliability AUC is ≥ 0.75 | about 15 reviewer subagents, once |
| **Review with profile** | Every later review. Your paper is mixed with 9 anchors sampled from the profile and placed against all calibrated anchors | about 6 reviewer subagents |
| **Default** | You skip setup. Three reviewers score your paper alone; the result is read with the built-in ARR × RAG score bands | 3 reviewer subagents, uncalibrated for your field |

Profiles are stored in `~/.claude/anchor-review/profiles/` and never leave your machine, because they contain other people's papers.

## Install

```text
/plugin marketplace add sungchul02/anchor-review
/plugin install anchor-review@anchor-review
```

Or copy `skills/anchor-review/` into `~/.claude/skills/`.

## Use

```text
Run anchor-review on paper.md for EMNLP. Use the default RAG anchors.
```

```text
Blind-review my draft against main/Findings/arXiv-only papers in machine translation for ACL.
```

For a new field, Claude builds the anchor set with `reference/build_anchors.md`.

### How many papers
| Purpose | Anchors | Reviews | Subagents (≈) |
|---|---|---|---|
| Minimum | 5 + 5 + 5 | 3 per paper | 9–10 |
| Recommended | 8 + 8 + 8 | 3 per paper | 15 |
| New venue or prompt | + held-out 4 + 4 + 4 | 3 per paper | +9 |

### Reading the score (default preset)
| Mean Overall of 3 reviewers | Reading |
|---|---|
| ≥ 3.0 | Accepted range. Only 1 of 12 arXiv-only anchors reached this. |
| 2.5–2.99 | Borderline |
| < 2.5 | Likely not accepted as is. Only 4 of 24 accepted anchors fell here. |

Real ARR reviewers average about 3.2. These reviewers score lower, so read positions, not raw numbers.

## Layout

```
skills/anchor-review/
  SKILL.md                       procedure Claude follows
  reference/reviewer_prompt.md   v2 reviewer prompt (frozen)
  reference/ac_prompt.md         area-chair meta-review prompt
  reference/arr_criteria.md      every rule with its official source
  reference/build_anchors.md     how to build and verify anchors
  presets/acl-arr_rag.md         default preset: setup, results, score bands
  presets/domestic-kr.md         Korean domestic venues (prompt only, uncalibrated)
  scripts/                       extract, anonymize, strip, assign batches, aggregate
```

## Limitations

- **Anchors are a small sample.** 36 papers, one field.
- **"ARXIV-ONLY" means no publication record**, not a confirmed rejection.
- **Reviewers are LLMs.** They catch what a careful reviewer would flag, such as inconsistent metrics, unfair baselines or missing details. They cannot see quotas or the luck of reviewer assignment.
- **No anchor papers or paper lists are distributed.** Claude collects anchors for your topic in each new setup.
- **It is a pre-submission sanity check**, not a substitute for advisors or real reviews. Do not use it to review other people's submissions.

## License

MIT
