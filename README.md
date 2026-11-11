# anchor-review

**Calibrated blind mock peer review for ACL / EMNLP / NAACL (ARR), as a Claude Code skill.**

[한국어 README](README.ko.md)

LLM reviewers give unreliable absolute scores, but they rank papers better than they score them. anchor-review
mixes your manuscript **blind** with same-field papers whose fate is known, then reports where your paper falls among them:
- *anchors* from the main conference
- *anchors* from Findings
- arXiv-only *anchors*, with no publication record

The same run also measures how well the reviewers separated the anchors. Each result therefore comes with its own reliability check.

| Earlier calibration: ARR × RAG / context compression / multi-hop QA | Tuning set (24) | **Held-out set (12)** |
|---|---|---|
| AUC: accepted (main+Findings) vs arXiv-only | 0.84 | **0.89** |
| AUC: main vs Findings | 0.30 | 0.63 (n=4 vs 4) |

It **can** tell whether a paper looks like it belongs in the accepted range. It **cannot** tell main from Findings. That split depends on area-chair quotas and reviewer noise more than on the text, and the skill says so in every report.

## How it works

**Phase 1: build criteria from real papers (once per venue × field).**
- Claude collects papers with known outcomes in your field. The default is 12 main-conference, 12 Findings, 6 accepted at a slightly easier venue (COLING) and 12 arXiv-only.
  - ARXIV-ONLY status is verified through arXiv, Semantic Scholar, OpenAlex, an Anthology match and a web search.
- Analyst subagents read each class *with labels* and record what those papers have in common: contribution type and size, evidence breadth, and which flaws coexisted with acceptance.
- A synthesis step turns this into one criteria file per reviewer tier. The files follow the official ARR scales and say which features earned which score at that venue. No paper titles are included.

**Phase 2: blind review (each manuscript).**
- Your paper is mixed with anchors into a **10-paper bundle**: yours plus 3 main, 2 Findings, 2 COLING and 2 arXiv-only.
  - Authors, venue marks and the Limitations, Ethics and AI-use sections are removed.
  - Your method name can be renamed.
- **Three reviewers, one per venue tier**, each read **all 10 papers** with their tier's criteria:
  - the target venue (ACL)
  - a peer venue at the same level (EMNLP)
  - a slightly easier venue (COLING)
- Each paper's score is the **mean of the three reviewers**.
- The report gives:
  - your rank
  - the full ranking table with each tier's score and reason
  - a detailed review of your paper: claims vs evidence, strengths, weaknesses by severity, questions, what would raise the score, and where the tiers disagree
  - a reliability check: how well each tier separated the anchors

Reviewers never learn the purpose, that your paper is included, or that some papers are published. No web search is allowed.

## Defaults vs custom

| You want | Do |
|---|---|
| Just a review now | Use the shipped criteria (`presets/criteria/acl-rag/`, ACL tiers × RAG field) and go to phase 2 |
| Another venue, field, paper counts, tiers, number of reviewers or bundle size | Copy `config/default.json` to `~/.claude/anchor-review/config.json`, edit it, run phase 1, then phase 2 |

Approximate cost: phase 1 is about 5 subagents (4 analysts + 1 synthesis) reading about 40 papers once. Phase 2 is 3 reviewers × 10 papers.

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
  SKILL.md                              procedure Claude follows
  config/default.json                   all defaults (copy to ~/.claude/anchor-review/config.json to customize)
  presets/criteria/acl-rag/             shipped phase-1 criteria: ACL / EMNLP / COLING tiers, RAG field
  presets/tiers.json                    reviewer tiers per target venue, with sourced acceptance rates
  presets/acl-arr_rag.md                score bands and the earlier calibration record
  presets/domestic-kr.md                Korean domestic venues (prompt only, uncalibrated)
  reference/criteria_analyst_prompt.md  phase 1: per-class analysis of known-outcome papers
  reference/criteria_synthesis_prompt.md phase 1: analyses -> per-tier criteria
  reference/reviewer_prompt.md          phase 2 reviewer prompt (v3, tier note + criteria slots)
  reference/arr_criteria.md             every ARR rule with its official source
  reference/build_anchors.md            how to collect and verify anchors
  scripts/                              extract, anonymize, strip, assign, aggregate, extract_target, profiles
```

## Limitations

- **The tiered protocol has been checked once.** On a 10-paper bundle the AUC was 0.79 overall: EMNLP tier 0.96, ACL 0.64, COLING 0.68. The COLING criteria come from only 6 papers and were too strict, so treat that tier as provisional.

- **Anchors are a small sample.** 36 papers, one field.
- **"ARXIV-ONLY" means no publication record**, not a confirmed rejection.
- **Reviewers are LLMs.** They catch what a careful reviewer would flag, such as inconsistent metrics, unfair baselines or missing details. They cannot see quotas or the luck of reviewer assignment.
- **No anchor papers or paper lists are distributed.** Claude collects anchors for your topic in each new setup.
- **It is a pre-submission sanity check**, not a substitute for advisors or real reviews. Do not use it to review other people's submissions.

## License

MIT
