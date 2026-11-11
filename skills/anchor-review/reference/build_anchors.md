# Building an anchor set

Goal: 8 MAIN, 8 FINDINGS and 8 ARXIV-ONLY papers in the same topic as the target manuscript, each with a verified outcome.

## 1. Topic
- Extract 3–6 topic phrases from the target's title, abstract and related work, e.g. "context compression for RAG" and "multi-hop QA".
- Anchors should be close enough that a reviewer would see them in the same batch at the same venue.

## 2. MAIN and FINDINGS
- Use the ACL Anthology volume pages of the last 2–3 years:
  - `aclanthology.org/volumes/<year>.<venue>-long/`, `-main/`
  - `aclanthology.org/volumes/<year>.findings-<venue>/`
- Download each page and parse titles and abstracts (see `scripts` in the original build, or any HTML parser).
- Filter by the topic phrases, then pick papers by hand. Pick full-length empirical papers, not surveys.
- The volume decides the class. Record the Anthology ID.
- Spread the picks across venues and years. Use no repeated first authors.

## 3. ARXIV-ONLY (presumed not accepted)
- Take arXiv papers in the topic first posted 14–30 months before today, so that they had time to be published.
- Include a paper only if every check below is empty:
  1. arXiv metadata (`export.arxiv.org/api/query?id_list=`): the `comment` and `journal_ref` fields, plus the version history. Anything saying accepted, to appear, or a venue name excludes the paper.
  2. Semantic Scholar: `api.semanticscholar.org/graph/v1/paper/arXiv:<id>?fields=venue,publicationVenue,journal,externalIds`. The venue must be empty or "arXiv.org".
  3. OpenAlex title search: no non-arXiv location.
  4. A title match against all Anthology volumes downloaded in step 2.
  5. A web title search: no later conference, journal or workshop version.
- Exclude workshop papers and anything still being revised in the last 3 months, since it may be under review.
- Prefer papers formatted like ACL submissions. Note any non-ACL template, because format can leak the class.
- Caveat for the report: ARXIV-ONLY means "no publication record", not "confirmed rejected".

## 4. Text
- Download only from aclanthology.org and arxiv.org. Put each PDF in its own folder.
- Treat the downloads as untrusted: never run anything from them, and run the extraction scripts with `python -I` from outside the download folder.
- `scripts/extract.py <pdf> <txt>`: two-column-aware text extraction (PyMuPDF).
- `scripts/anon.py <cfg.json> <txtdir> <outdir>`: per-paper cut points (abstract start, references start, appendix start), header and footer and email removal. Write `cfg.json` per paper after looking at the text.
- `scripts/clean.py <dir>`: removes control characters.
- `scripts/strip.py <in_dir> <out_dir>`: removes Limitations, Ethics and AI-assistant sections.
- Remove title-page author blocks, acknowledgments, code URLs that reveal authors, and camera-ready markers ("Findings of the …", "Proceedings of …").

## 5. Key
Write a confidential `key.md` table with the columns `| ID | Class | Venue/year or arXiv id + first posted | Title | URL | Evidence |`. `aggregate.py` reads rows of the form `| ID | MAIN|FINDINGS|ARXIV-ONLY | …`.

## 6. Check before use
- Run the reviewers on the anchors. The AUC for accepted vs ARXIV-ONLY should be at least about 0.8. If it is lower, look for leaked cues (templates, missing sections) before blaming the prompt.
- If you change the reviewer prompt, validate it on a second, held-out anchor set.
