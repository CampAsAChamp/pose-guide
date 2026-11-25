"""Draw a contact sheet of selected poses so you can eyeball new or edited cards.

Steps:
  1. Pick the cards named on the command line (all of them if none are named).
  2. Write preview.html: each drawing with the thirds grid over it and its number and title.
  3. With --png, screenshot the sheet to preview.png in headless Chrome.

    python preview.py 12 45 199          # writes preview.html
    python preview.py 12 45 --png        # also writes preview.png (needs an installed Chrome; see chrome.py)
    python preview.py --range 190 200
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from chrome import headless_cmd  # noqa: E402
from poses.catalog import CARDS  # noqa: E402

GRID = ('<g stroke="#FFFFFF" stroke-width="1.5" opacity="0.7"><line x1="200" y1="0" x2="200" y2="800"/>'
        '<line x1="400" y1="0" x2="400" y2="800"/><line x1="0" y1="266.7" x2="600" y2="266.7"/>'
        '<line x1="0" y1="533.3" x2="600" y2="533.3"/></g>')
CELL_W, CELL_H, COLS = 250, 352, 6  # one figure plus its caption and gap, in CSS pixels


def log_step(message: str) -> None:
    """Print a progress line to stderr."""
    print(f"[*] {message}", file=sys.stderr)


def pick(nums, span) -> list:
    """Cards whose numbers are in nums or the inclusive span; every card if neither is given."""
    want = set(nums)
    if span:
        want |= set(range(span[0], span[1] + 1))
    return [c for c in CARDS if not want or c.n in want]


def write_sheet(cards, out: str) -> None:
    """Write the contact sheet HTML. Side effects: writes out."""
    cells = "".join(
        '<figure style="margin:0"><svg width="240" height="320" viewBox="0 0 600 800">%s%s</svg>'
        '<figcaption style="font:13px system-ui">%d %s</figcaption></figure>' % (c.draw(), GRID, c.n, c.title)
        for c in cards)
    html = ('<!doctype html><meta charset="utf-8">'
            '<body style="margin:0;padding:10px;background:#888;display:flex;flex-wrap:wrap;gap:10px">%s</body>' % cells)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)


def screenshot(page: str, png: str, count: int) -> None:
    """Screenshot the sheet at a size that fits every cell. Side effects: writes png; exits 1 on failure."""
    cols = min(COLS, count) or 1
    rows = (count + cols - 1) // cols
    with tempfile.TemporaryDirectory(prefix="pose-preview-") as profile:
        cmd = headless_cmd(profile) + ["--hide-scrollbars", "--window-size=%d,%d" % (20 + cols * CELL_W, 20 + rows * CELL_H),
                                       "--screenshot=" + png, "file://" + page]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0 or not os.path.exists(png):
        log_step("FAILED: Chrome could not take the screenshot:\n" + proc.stderr[-2000:])
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Contact sheet of chosen poses.")
    ap.add_argument("nums", nargs="*", type=int)
    ap.add_argument("--range", nargs=2, type=int)
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args()

    # Step 1: choose cards.
    cards = pick(a.nums, a.range)
    if not cards:
        log_step("FAILED: no poses match %s (numbers run 1 to %d)" % (a.nums or a.range, len(CARDS)))
        sys.exit(1)

    # Step 2: write the sheet.
    out = os.path.join(HERE, "preview.html")
    log_step("Step 1/%d: drawing %d poses into preview.html" % (2 if a.png else 1, len(cards)))
    write_sheet(cards, out)

    # Step 3: optional screenshot.
    if a.png:
        log_step("Step 2/2: screenshotting to preview.png")
        screenshot(out, os.path.join(HERE, "preview.png"), len(cards))
    log_step("Done")


if __name__ == "__main__":
    main()
