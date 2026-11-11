"""Remove control characters (except tab and newline) that PDF extraction leaves in Markdown files.

Usage:
    python clean.py <dir>        # rewrites every *.md in <dir> in place
"""
import pathlib
import re
import sys

CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def main(folder):
    for f in pathlib.Path(folder).glob("*.md"):
        text = f.read_text(encoding="utf8")
        f.write_text(CONTROL_CHARS.sub("", text), encoding="utf8")


if __name__ == "__main__":
    main(sys.argv[1])
