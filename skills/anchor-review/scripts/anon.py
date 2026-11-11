"""Turn extracted paper text into the anonymized Markdown form used for blind review.

Usage:
    python -I anon.py <cfg.json> <txt_dir> <out_dir>

cfg.json maps a paper ID (4 random capital letters) to settings that you fill in by hand
after reading each .txt from extract.py:

    {
      "ABCD": {
        "file":  "2025.acl-long.131.txt",   # extracted text in <txt_dir>
        "title": "Paper title",
        "abs":   12,      # 1-based line where the abstract starts (everything above it, i.e. authors, is dropped)
        "refs":  1746,    # 1-based line where References start (references are dropped)
        "app":   2423,    # optional: line where the appendix starts (kept)
        "heads": ["Exact heading line", ...],  # optional: lines to force into headings
        "del":   ["regex", ...],                # optional: regexes deleted from every paragraph
        "roman": true                           # optional: headings look like "A. Method" (IEEE style)
      }
    }

Writes <out_dir>/paper_<ID>.md:
    # Paper ABCD / ## Title / title / ## Abstract / body with ## headings

What is removed automatically:
- page markers and page numbers
- running headers and footers (proceedings lines, arXiv stamps)
- author footnotes (equal contribution, corresponding author, internship)
- lines containing e-mail addresses
- the Acknowledgments section

Limitations, Ethics and AI-use sections are removed afterwards by strip.py.
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

RUNNING_HEADER = re.compile(
    r"(Proceedings of the .*(Association|Conference|Meeting)"
    r"|Findings of the Association for Computational Linguistics"
    r"|©\s?20\d\d Association|Association for Computational Linguistics$"
    r"|^Preprint\. Under review\.|arXiv:\d{4}\.\d{4,5}v\d+\s+\[|Work in progress"
    r"|^(NAACL|EMNLP|ACL) 20\d\d, pages|^BCorresponding)"
)
AUTHOR_FOOTNOTE = re.compile(
    r"^\s*[\*∗†‡§¶0-9]+\s*.*(qual contribution|ontributed equally|orresponding|nternship"
    r"|Work done|Project lead|Now at|Core contributor)",
    re.I,
)
EMAIL = re.compile(r"[\w.\-{},]+@[\w\-]+(\.[\w\-]+)*\.[A-Za-z]{2,}\b")  # not "Recall@1.5"
ACK_HEADING = re.compile(r"^(Acknowledg(e)?ments?|ACKNOWLEDG\w*)\s*$")
# A short block like these ends the Acknowledgments section.
SECTION_AFTER_ACK = re.compile(r"^(Limitations|Ethic|Appendix|[A-H](\.\d+)*\s*$|[A-H]\s+[A-Z])")
KNOWN_HEADINGS = {
    "Limitations", "Ethics Statement", "Ethical Considerations", "Ethical considerations", "Ethics statement",
    "Conclusion", "Conclusions", "Appendix", "Broader Impact", "Abstract",
}
SECTION_NUMBER = r"(([1-9]|1[0-2])(\.\d{1,2})*|[A-H](\.\d{1,2})*)"   # 3, 3.2, A, B.1
NUMBER_ONLY = re.compile(SECTION_NUMBER + r"\.?")                     # a heading number on its own line
NUMBERED_HEADING = re.compile(r"^(" + SECTION_NUMBER + r"\.?\s+)[A-Z][A-Za-z\-]")
ROMAN_HEADING = re.compile(r"[IVX]+\. [A-Z][A-Z \-]+")                # "III. METHOD"
LETTER_HEADING = re.compile(r"[A-H]\. [A-Z][A-Za-z \-()]+")           # "A. Setup" (only with roman: true)
HEADING_MARK = "##H##H"


def split_blocks(lines):
    """Group lines into blocks separated by blank lines."""
    blocks, cur = [], []
    for ln in lines:
        if ln.strip() == "":
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(ln.rstrip())
    if cur:
        blocks.append(cur)
    return blocks


def drop_page_markers(blocks):
    """Remove <<<PAGE n>>> markers and the page-number block that sits right before one."""
    kept = []
    for i, b in enumerate(blocks):
        if b[0].startswith("<<<PAGE"):
            continue
        nxt = blocks[i + 1][0] if i + 1 < len(blocks) else "<<<PAGE"
        if len(b) == 1 and re.fullmatch(r"\d{1,5}", b[0].strip()) and nxt.startswith("<<<PAGE"):
            continue
        kept.append(b)
    return kept


def drop_acknowledgments(blocks):
    kept, skipping = [], False
    for b in blocks:
        text = " ".join(b).strip()
        if ACK_HEADING.match(text):
            skipping = True
            continue
        if skipping:
            ends_ack = (text in KNOWN_HEADINGS or SECTION_AFTER_ACK.match(text)) and len(text) < 60
            if not ends_ack:
                continue
            skipping = False
        kept.append(b)
    return kept


def join_lines(lines):
    """Join a block into one paragraph, undoing end-of-line hyphenation."""
    s = lines[0]
    for ln in lines[1:]:
        s = s[:-1] + ln if s.endswith("-") and ln[:1].islower() else s + " " + ln
    return s.strip()


def to_paragraphs(blocks, cfg):
    """Clean each block. Return paragraphs; forced headings are prefixed with HEADING_MARK."""
    forced = set(cfg.get("heads", []))
    out = []
    for b in blocks:
        b = [ln for ln in b if not RUNNING_HEADER.search(ln) and not AUTHOR_FOOTNOTE.match(ln) and not EMAIL.search(ln)]
        while b and (
            b[0].strip() in forced
            or ROMAN_HEADING.fullmatch(b[0].strip())
            or (LETTER_HEADING.fullmatch(b[0].strip()) and cfg.get("roman"))
        ):
            out.append(HEADING_MARK + b[0].strip())
            b = b[1:]
        if not b:
            continue
        s = join_lines(b)
        for pattern in cfg.get("del", []):
            s = re.sub(pattern, "", s).strip()
        if s:
            out.append(s)
    return out


def looks_like_heading(s):
    if s in KNOWN_HEADINGS:
        return True
    return (
        len(s) < 80
        and NUMBERED_HEADING.match(s) is not None
        and not s.endswith(".")
        and len(s.split()) <= 12
        and not re.search(r"\d{4}", s)       # a year: probably a sentence or a citation
        and not re.search(r"[=<>%]", s)      # math or results: not a heading
    )


def to_markdown(pid, title, paragraphs):
    md = ["# Paper " + pid, "", "## Title", "", title, "", "## Abstract", ""]
    pending_number = None  # a heading number ("3.2") waiting for its title on the next line
    for s in paragraphs:
        if s == "":
            continue
        if s.startswith(HEADING_MARK):
            if pending_number is not None:
                md += [pending_number, ""]
                pending_number = None
            md += ["## " + s[len(HEADING_MARK):], ""]
            continue
        if pending_number is not None:
            if len(s) < 80 and re.match(r"^[A-Z][^.]*$", s) and len(s.split()) <= 12:
                md += ["## " + pending_number + " " + s, ""]
                pending_number = None
                continue
            md += [pending_number, ""]
            pending_number = None
        if NUMBER_ONLY.fullmatch(s):
            pending_number = s
            continue
        md += ["## " + s, ""] if looks_like_heading(s) else [s, ""]
    return "\n".join(md)


def anonymize(pid, cfg, txt_dir):
    lines = open(os.path.join(txt_dir, cfg["file"]), encoding="utf8").read().split("\n")
    start, refs, appendix = cfg["abs"], cfg["refs"], cfg.get("app")
    body = lines[start - 1:refs - 1] + (lines[appendix - 1:] if appendix else [])

    blocks = drop_acknowledgments(drop_page_markers(split_blocks(body)))
    paragraphs = to_paragraphs(blocks, cfg)
    if not paragraphs:
        return None
    paragraphs[0] = re.sub(r"^(Abstract|ABSTRACT)[—:.\-\s]*", "", paragraphs[0])
    return to_markdown(pid, cfg["title"], paragraphs)


def main(cfg_path, txt_dir, out_dir):
    cfgs = json.load(open(cfg_path, encoding="utf8"))
    os.makedirs(out_dir, exist_ok=True)
    for pid, cfg in cfgs.items():
        md = anonymize(pid, cfg, txt_dir)
        if md is None:
            print(pid, "EMPTY: check the abs/refs line numbers")
            continue
        with open(os.path.join(out_dir, f"paper_{pid}.md"), "w", encoding="utf8") as f:
            f.write(md)
        print(pid, len(md.split()), "words")


if __name__ == "__main__":
    main(*sys.argv[1:4])
