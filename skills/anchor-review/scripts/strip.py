"""Remove sections that reveal whether a paper was published: Limitations, Ethics, Broader Impact and
AI/LLM-usage disclosures. ACL camera-ready papers always have them and arXiv preprints often do not, so
leaving them in would let reviewers guess the class.

Usage:
    python strip.py <in_dir> <out_dir>

A section runs from its "## " heading to the next "## " heading. Body subsections such as
"## 5.5 Limitation of fixed retrieval" are kept, because a numbered heading must be followed by the
keyword directly ("## 6 Limitations").
Disclosure text that is not under its own heading cannot be removed safely, so it is printed for manual removal.
"""
import pathlib
import re
import sys

REMOVED_SECTION = re.compile(
    r"^##\s*(?:[0-9A-Z]+\.?\s+)?"              # optional section number: "6 ", "C ", "8. "
    r"(limitations?"
    r"|ethic(s|al)[^\n]*"
    r"|usage of ai (writing )?assistants?"
    r"|ai writing assistan[^\n]*"
    r"|llm usage disclosure"
    r"|(use|usage) of (ai|llms?|large language models)[^\n]*"
    r"|broader impact[^\n]*)\s*$",
    re.I,
)
LEFTOVER = re.compile(r"(writing assistant|usage of ai|llm usage|chatgpt was used|acknowledg)", re.I)


def strip_sections(text):
    """Return (kept_lines, number_of_removed_sections)."""
    kept, skipping, removed = [], False, 0
    for line in text.splitlines():
        if line.startswith("## "):
            skipping = bool(REMOVED_SECTION.match(line.strip()))
            removed += skipping
        if not skipping:
            kept.append(line)
    return kept, removed


def main(src, dst):
    src, dst = pathlib.Path(src), pathlib.Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob("paper_*.md")):
        kept, removed = strip_sections(f.read_text(encoding="utf-8"))
        (dst / f.name).write_text("\n".join(kept) + "\n", encoding="utf-8")
        leftovers = [ln[:80] for ln in kept if LEFTOVER.search(ln) and not ln.startswith("#")]
        note = f"  | check by hand: {' / '.join(leftovers[:2])}" if leftovers else ""
        print(f"{f.name}: removed {removed} section(s){note}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
