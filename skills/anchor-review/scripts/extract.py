"""Extract text from a two-column paper PDF in reading order.

Usage:
    python -I extract.py <paper.pdf> <out.txt>

Run it from outside the download folder: downloaded PDFs are untrusted.
Requires PyMuPDF >= 1.24 (`pip install pymupdf`).

Output: plain text with one line per PDF text block. A marker line `<<<PAGE n>>>` comes before each page;
`anon.py` uses these markers to drop page numbers.

Reading order on each page:
1. Drop page numbers: blocks containing only digits in the top 6% or bottom 10% of the page.
2. Split the page into horizontal bands at every full-width block (title, wide table or figure caption).
3. Inside each band, read the left column top to bottom, then the right column.
"""
import os
import sys

import pymupdf

HEADER_ZONE = 0.06  # top share of the page height where page numbers may appear
FOOTER_ZONE = 0.90  # page numbers may also appear below this share of the page height

FULL, LEFT, RIGHT = 0, 1, 2


def column_of(block, page_width):
    """FULL if the block crosses the page center, otherwise LEFT or RIGHT."""
    x0, x1 = block[0], block[2]
    if x0 < page_width * 0.45 and x1 > page_width * 0.55:
        return FULL
    return LEFT if x0 < page_width * 0.5 else RIGHT


def is_page_number(block, page_height):
    y0, text = block[1], block[4].strip()
    return text.isdigit() and (y0 > page_height * FOOTER_ZONE or y0 < page_height * HEADER_ZONE)


def blocks_in_reading_order(page):
    width, height = page.rect.width, page.rect.height
    # A block is (x0, y0, x1, y1, text, block_no, block_type); block_type 0 means text.
    blocks = [b for b in page.get_text("blocks") if b[6] == 0 and not is_page_number(b, height)]
    blocks.sort(key=lambda b: (b[1], b[0]))

    full_width = [b for b in blocks if column_of(b, width) == FULL]
    bands = [[] for _ in range(len(full_width) + 1)]
    for b in blocks:
        if column_of(b, width) != FULL:
            above = sum(1 for f in full_width if f[1] <= b[1])  # full-width blocks above this one
            bands[above].append(b)

    ordered = []
    for i, band in enumerate(bands):
        if i > 0:
            ordered.append(full_width[i - 1])
        ordered += sorted((b for b in band if column_of(b, width) == LEFT), key=lambda b: b[1])
        ordered += sorted((b for b in band if column_of(b, width) == RIGHT), key=lambda b: b[1])
    return ordered


def main(src, dst):
    doc = pymupdf.open(src)
    lines = []
    for page_no, page in enumerate(doc, start=1):
        lines.append(f"\n<<<PAGE {page_no}>>>\n")
        lines += [b[4].strip() + "\n" for b in blocks_in_reading_order(page)]
    with open(dst, "w", encoding="utf8") as f:
        f.write("\n".join(lines))
    print(f"{os.path.basename(src)}: {len(doc)} pages")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
