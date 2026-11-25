"""Render every pose, check the data and write the single-file site.

Steps:
  1. Render every card's drawing.
  2. Run the data checks in checks.py (and stop on any problem).
  3. Fill template.html with the CSS, JS and pose data, and write the page.

    python build.py                 # writes ../index.html
    python build.py -o site.html    # write somewhere else
    python build.py --only 12 45    # also print these cards' titles and tags (quick sanity check)
    python build.py --lock          # record new pose numbers (or a deliberate rename) in pose_numbers.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402
from poses.catalog import CARDS, GROUPS  # noqa: E402

SELF_CLOSING = re.compile(r"></(path|rect|circle|line|polygon|ellipse)>")


def log_step(message: str) -> None:
    """Print a progress line to stderr."""
    print(f"[*] {message}", file=sys.stderr)


def read(name: str) -> str:
    """Return the text of a file in this folder."""
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def tidy(text: str) -> str:
    """Swap straight apostrophes for typographic ones in visible text."""
    return text.replace("'", "’")


def render_all(cards) -> dict:
    """Draw every card. Outputs: {number: SVG markup} with empty elements self-closed to save space."""
    return {c.n: SELF_CLOSING.sub("/>", c.draw()) for c in cards}


def card_json(c, markup: str) -> dict:
    """The page's record for one card (field names are documented in AGENTS.md)."""
    rec = {"n": c.n, "t": tidy(c.title), "g": c.tags, "p": tidy(c.pose), "f": tidy(c.frame), "a": markup}
    if c.alt:
        rec["d"] = tidy(c.alt)  # optional: only hand-written descriptions, never a copy of the tips
    return rec


def write_page(cards, rendered: dict, out: str) -> int:
    """Fill the template and write the page. Outputs: page size in bytes. Side effects: writes out."""
    data = {"groups": [[g, ts] for g, ts in GROUPS], "cards": [card_json(c, rendered[c.n]) for c in cards]}
    # "</" inside the JSON would end the <script> element early.
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = read("template.html")
    # Inline the stylesheet and script so the page stays one self-contained file.
    page = page.replace("__CSS__", read("styles.css").rstrip("\n"))
    page = page.replace("__JS__", read("app.js").rstrip("\n"))
    page = page.replace("__COUNT__", str(len(cards))).replace("__DATA__", blob)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    return len(page.encode())


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the pose guide page.")
    ap.add_argument("-o", "--out", default=os.path.join(HERE, "..", "index.html"))
    ap.add_argument("--only", nargs="*", type=int, default=[])
    ap.add_argument("--lock", action="store_true", help="record every pose number and title in pose_numbers.json")
    args = ap.parse_args()

    # Step 1: draw every pose.
    log_step("Step 1/3: rendering %d poses" % len(CARDS))
    rendered = render_all(CARDS)
    for c in CARDS:
        if c.n in args.only:
            print(c.n, c.title, c.tags)

    # Step 2: check the data. With --lock, the numbers file is rewritten instead of checked.
    log_step("Step 2/3: checking pose data")
    problems = checks.run_all(CARDS, GROUPS, rendered, lock=not args.lock)
    if problems:
        for p in problems:
            print("  - " + p, file=sys.stderr)
        log_step("FAILED: %d problem(s); nothing written" % len(problems))
        sys.exit(1)
    if args.lock:
        checks.write_lock(CARDS)
        log_step("recorded %d pose numbers in pose_numbers.json" % len(CARDS))

    # Step 3: write the page.
    log_step("Step 3/3: writing the page")
    size = write_page(CARDS, rendered, args.out)
    log_step("Done: wrote %s: %d poses, %.2f MB" % (os.path.normpath(args.out), len(CARDS), size / 1e6))


if __name__ == "__main__":
    main()
