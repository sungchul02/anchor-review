"""Collect reviewer scores and report (a) how well this run separated the anchor classes and
(b) where each target paper falls among the anchors.

Usage:
    python aggregate.py <reviews_dir> <key.md> --target ID[,ID...] [--ac <ac_dir>]

Inputs
- <reviews_dir>/*.md: reviewer outputs. Each must end with the summary table that reviewer_prompt.md asks for,
  with columns including "Soundness" and "Overall".
- key.md: the confidential anchor key. Rows look like "| ABCD | MAIN | ..." (classes MAIN, FINDINGS, ARXIV-ONLY).
- --target: IDs of the paper(s) being evaluated (not in the key).
- --ac: optional folder of meta-reviews whose last table has a "메타" (meta score) column.
- --profile: optional profile.json saved by profiles.py. The target is then also placed against the
  profile's full calibrated anchor distribution, which is steadier than the few anchors sampled into this run.

How to read the output
- "AUC accepted vs arXiv-only" is the reliability check for this run: the probability that a random
  accepted anchor (MAIN or FINDINGS) outscores a random ARXIV-ONLY anchor (0.5 = chance, 1.0 = perfect).
  Below about 0.75, do not trust the target's position from this run.
- "share below" for a target is the fraction of anchors of each class that scored lower (ties count half).
"""
import argparse
import json
import pathlib
import re
import statistics as st
import sys
from itertools import combinations

CLASSES = ("MAIN", "FINDINGS", "COLING", "ARXIV-ONLY")   # COLING = accepted at the lower-tier venue
RANK = {"MAIN": 2, "FINDINGS": 1, "ARXIV-ONLY": 0}         # ordering used by pairwise_order
ACCEPTED = ("MAIN", "FINDINGS", "COLING")
TARGET = "TARGET"


# ---------------------------------------------------------------------------------------------- reading inputs
def read_key(path):
    """{paper_id: class} from the anchor key table."""
    key = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*([A-Z]{4})\s*\|\s*(MAIN|FINDINGS|COLING|ARXIV-ONLY)\s*\|", line)
        if m:
            key[m.group(1)] = m.group(2)
    return key


def first_number(text):
    """First number in a cell: '3.5' -> 3.5, '1.5–2' -> 1.5, '' -> None."""
    m = re.search(r"\d+(\.\d+)?", text or "")
    return float(m.group(0)) if m else None


def cells(line):
    return [c.strip().strip("*").strip() for c in line.strip().strip("|").split("|")]


def last_table(text, required_columns, known_ids):
    """Rows of the LAST markdown table whose header contains every required column name.

    Only rows whose first cell is a known paper ID (optionally written as paper_ABCD) are kept,
    so other tables inside a review (e.g. a baseline called "EXIT") are never mistaken for papers.
    Returns {paper_id: {header_lowercase: cell}}.
    """
    lines = text.splitlines()
    header_at = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            header = [c.lower() for c in cells(line)]
            if all(any(col in h for h in header) for col in required_columns):
                header_at = i
    if header_at is None:
        return {}

    header = [c.lower() for c in cells(lines[header_at])]
    rows = {}
    for line in lines[header_at + 1:]:
        if not line.strip().startswith("|"):
            break
        row = cells(line)
        if row and re.fullmatch(r"(paper_)?[A-Z]{4}", row[0]) and row[0][-4:] in known_ids:
            rows[row[0][-4:]] = dict(zip(header, row))
    return rows


def column(row, name):
    """Value of the first column whose header contains `name`."""
    return next((v for h, v in row.items() if name in h), None)


def read_reviews(folder, known_ids):
    """{paper_id: [overall, ...]}, {paper_id: [soundness, ...]} over all review files."""
    overall, soundness, reasons, by_reviewer = {}, {}, {}, {}
    for f in sorted(pathlib.Path(folder).glob("*.md")):
        rows = last_table(f.read_text(encoding="utf-8"), ("soundness", "overall"), known_ids)
        if not rows:
            print(f"WARNING: no summary table in {f.name}; rerun that reviewer")
        for pid, row in rows.items():
            for store, col in ((overall, "overall"), (soundness, "soundness")):
                value = first_number(column(row, col))
                if value is not None:
                    store.setdefault(pid, []).append(value)
                    if col == "overall":
                        by_reviewer.setdefault(f.stem, {})[pid] = value
            reason = column(row, "이유") or column(row, "reason")
            if reason:
                reasons.setdefault(pid, []).append(f"[{f.stem}] {reason}")
    return overall, soundness, reasons, by_reviewer


def read_meta(folder, known_ids):
    meta = {}
    for f in sorted(pathlib.Path(folder).glob("*.md")):
        for pid, row in last_table(f.read_text(encoding="utf-8"), ("메타",), known_ids).items():
            meta[pid] = first_number(column(row, "메타"))
    return meta


# ---------------------------------------------------------------------------------------------- metrics
def auc(scores, cls, high, low):
    """P(score of a `high`-class paper > score of a `low`-class paper); ties count half."""
    a = [s for p, s in scores.items() if cls.get(p) in high]
    b = [s for p, s in scores.items() if cls.get(p) in low]
    if not a or not b:
        return None
    return round(sum((x > y) + 0.5 * (x == y) for x in a for y in b) / (len(a) * len(b)), 3)


def pairwise_order(scores, cls):
    """Share of anchor pairs from different classes ordered MAIN > FINDINGS > ARXIV-ONLY."""
    anchors = [p for p in scores if cls.get(p) in RANK]
    ok = total = 0
    for a, b in combinations(anchors, 2):
        if RANK[cls[a]] == RANK[cls[b]]:
            continue
        hi, lo = (a, b) if RANK[cls[a]] > RANK[cls[b]] else (b, a)
        total += 1
        ok += 1.0 if scores[hi] > scores[lo] else 0.5 if scores[hi] == scores[lo] else 0.0
    return round(ok / total, 3) if total else None


def share_below(scores, cls, target):
    """For each anchor class, the fraction of its papers scoring below the target (ties count half)."""
    s = scores[target]
    out = {}
    for c in CLASSES:
        v = [x for p, x in scores.items() if cls.get(p) == c]
        if v:
            out[c] = round(sum((x < s) + 0.5 * (x == s) for x in v) / len(v), 2)
    return out


def class_means(scores, cls):
    out = {}
    for c in CLASSES:
        v = [x for p, x in scores.items() if cls.get(p) == c]
        if v:
            out[c] = (round(st.mean(v), 2), len(v))
    return out


# ---------------------------------------------------------------------------------------------- report
def report(name, scores, cls, targets):
    print(f"== {name}")
    print("  class means (mean, n):", class_means(scores, cls))
    print("  AUC accepted vs arXiv-only (reliability):", auc(scores, cls, ACCEPTED, ("ARXIV-ONLY",)))
    print("  AUC main vs Findings (not expected to work):", auc(scores, cls, ("MAIN",), ("FINDINGS",)))
    print("  pairwise order MAIN > FINDINGS > ARXIV-ONLY:", pairwise_order(scores, cls))
    for t in targets:
        if t in scores:
            print(f"  target {t}: score {scores[t]}, share of each anchor class below it: {share_below(scores, cls, t)}")
        else:
            print(f"  target {t}: no scores found")


def report_against_profile(path, scores, targets):
    """Place each target against the anchor scores stored in a saved profile, including its rank."""
    info = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    print(f"== against profile {info['name']} ({info['anchors']} anchors, reliability AUC {info['reliability_auc']})")
    if not info.get("reliable"):
        print("  WARNING: this profile was not reliable at calibration time")
    pool = [x for d in info["per_class"].values() for x in d["scores"]]
    for t in targets:
        if t not in scores:
            continue
        s = scores[t]
        below = {c: round(sum((x < s) + 0.5 * (x == s) for x in d["scores"]) / d["n"], 2)
                 for c, d in info["per_class"].items()}
        higher, tied = sum(x > s for x in pool), sum(x == s for x in pool)
        rank = f"{higher + 1}" if not tied else f"{higher + 1}-{higher + tied + 1} (tied with {tied})"
        print(f"  target {t}: score {s}, rank {rank} of {len(pool) + 1}, share of each anchor class below it: {below}")


def report_reviewers(by_reviewer, cls):
    """Each reviewer's own calibration on the anchors it scored (tiered runs: one line per venue tier)."""
    print("== per reviewer")
    for name, scores in sorted(by_reviewer.items()):
        print(f"  {name}: AUC accepted vs arXiv-only {auc(scores, cls, ACCEPTED, ('ARXIV-ONLY',))},"
              f" class means {class_means(scores, cls)}")


def ranking_table(mean_overall, overall, soundness, reasons, cls, by_reviewer):
    """Markdown table: rank, ID, class, mean Overall, each reviewer's Overall, Soundness, decisive reasons."""
    order = sorted(mean_overall, key=lambda p: -mean_overall[p])
    lines = ["| 순위 | ID | 구분 | 평균 Overall | 심사자별 | Soundness | 결정 이유 |", "|---|---|---|---|---|---|---|"]
    for p in order:
        rank = 1 + sum(mean_overall[q] > mean_overall[p] for q in order)  # ties share the best rank
        label = "★ 대상 원고" if cls.get(p) == TARGET else cls.get(p, "?")
        sound = round(st.mean(soundness[p]), 2) if soundness.get(p) else "-"
        why = " / ".join(reasons.get(p, [])).replace("|", "/")
        each = " · ".join(f"{name} {s[p]}" for name, s in sorted(by_reviewer.items()) if p in s)
        lines.append(f"| {rank} | {p} | {label} | {mean_overall[p]:.2f} | {each} | {sound} | {why} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reviews")
    ap.add_argument("key")
    ap.add_argument("--target", required=True, help="comma-separated target paper IDs")
    ap.add_argument("--ac", help="folder with meta-reviews (optional)")
    ap.add_argument("--profile", help="profile.json from profiles.py (optional)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # Korean reasons on Windows consoles

    cls = read_key(args.key)
    targets = args.target.split(",")
    cls.update({t: TARGET for t in targets})
    known = set(cls)

    overall, soundness, reasons, by_reviewer = read_reviews(args.reviews, known)
    mean_overall = {p: round(st.mean(v), 3) for p, v in overall.items()}
    report("reviewer mean Overall", mean_overall, cls, targets)
    if args.ac:
        meta = {p: s for p, s in read_meta(args.ac, known).items() if s is not None}
        report("AC meta score", meta, cls, targets)

    if args.profile:
        report_against_profile(args.profile, mean_overall, targets)
    print("  reviews per paper:", sorted({len(v) for v in overall.values()}))
    print()
    report_reviewers(by_reviewer, cls)
    print()
    print(ranking_table(mean_overall, overall, soundness, reasons, cls, by_reviewer))


if __name__ == "__main__":
    main()
