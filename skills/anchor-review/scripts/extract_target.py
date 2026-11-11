"""Collect every reviewer's full review of the target paper into one file, for the final detailed report.

Usage:
    python extract_target.py <reviews_dir> <TARGET_ID> <out.md>

Each review file contains one section per paper, headed "## paper_<ID>" (the reviewer prompt asks for this;
other heading levels or "<ID>" alone are accepted too). The section ends at the next heading of the same or a
higher level that names another paper, or at the summary table.
"""
import pathlib
import re
import sys


def target_section(text, target):
    lines = text.splitlines()
    start = level = None
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,4})\s.*\b(paper_)?" + target + r"\b", line)
        if m:
            start, level = i, len(m.group(1))
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        m = re.match(r"^(#{1,4})\s", line)
        names_other = re.search(r"\b(paper_)?[A-Z]{4}\b", line) and target not in line
        if (m and len(m.group(1)) <= level and (names_other or "요약" in line or "summary" in line.lower())) \
                or line.strip().startswith("| ID"):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def main(reviews_dir, target, out):
    parts = []
    for f in sorted(pathlib.Path(reviews_dir).glob("*.md")):
        section = target_section(f.read_text(encoding="utf-8"), target)
        if section:
            parts.append(f"# Reviewer: {f.stem}\n\n{section}\n")
        else:
            print(f"WARNING: no section for {target} in {f.name}")
    pathlib.Path(out).write_text("\n".join(parts), encoding="utf-8")
    print(f"{len(parts)} reviews of {target} -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
