# scripts

The scripts run in this order. Each one has a docstring with its usage and what it does.

```
paper.pdf ──extract.py──▶ paper.txt ──anon.py (+cfg.json)──▶ paper_ID.md ──clean.py──▶ ──strip.py──▶ subs/
                                                                                                    │
                       reviewer subagents ◀── tasks/*.md ◀──assign.py (+reference/reviewer_prompt.md)──┘
                               │
                               ▼
                         reviews/*.md ──aggregate.py (+key.md)──▶ reliability AUC + target position
```

| Script | Input | Output | Notes |
|---|---|---|---|
| `extract.py` | one PDF | text in reading order, with `<<<PAGE n>>>` markers | two-column aware; needs PyMuPDF |
| `anon.py` | `cfg.json` + texts | `paper_<ID>.md` | cut points per paper are set by hand in `cfg.json` |
| `clean.py` | folder of `.md` | same files, in place | removes control characters |
| `strip.py` | folder of `.md` | new folder | removes Limitations/Ethics/AI-use sections and flags leftovers |
| `assign.py` | `subs/` + reviewer prompt | `tasks/`, `reviews/`, `plan.json` | one pass per venue, so 3 reviews per paper |
| `aggregate.py` | `reviews/` + anchor key | printed report | parses only the last summary table of each review |

The scripts use only the standard library, except `extract.py`, which needs PyMuPDF.
None of them uses the network or executes the files it reads.
Run `extract.py` and `anon.py` with `python -I` from outside the download folder, because downloaded PDFs are untrusted.

The rewritten `extract.py`, `anon.py`, `strip.py`, `clean.py` and `assign.py` were checked byte-for-byte against the
versions used for calibration:
- 24 + 12 anchor papers for extraction and anonymization
- the same seed for batching

The results were identical.
