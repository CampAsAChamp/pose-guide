"""Data checks run by build.py before it writes the page.

Each check returns a list of problems (empty when it passes), so the build can
report every problem at once instead of stopping at the first.

Checks:
  1. Numbers run 1..N with no gaps or repeats.
  2. Every pose number keeps the title recorded in pose_numbers.json, so
     #pose-N links never point at a different pose.
  3. Titles are unique.
  4. Each card has exactly one tag per filter group, in group order.
  5. Visible text has no straight double quotes, and each tip is one or two sentences.
  6. Each drawing parses as SVG/XML.
"""
from __future__ import annotations

import json
import os
import re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.join(HERE, "pose_numbers.json")
SENTENCE_END = re.compile(r"[.!?](?=\s|$)")


def check_numbers(cards) -> list:
    """Numbers must be exactly 1..N. Inputs: sorted cards. Outputs: problems."""
    nums = [c.n for c in cards]
    if nums == list(range(1, len(cards) + 1)):
        return []
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    gaps = sorted(set(range(1, max(nums) + 1)) - set(nums))
    return ["pose numbers must run 1..%d: repeated %s, missing %s" % (len(cards), dupes or "none", gaps or "none")]


def read_lock() -> dict:
    """Load pose_numbers.json as {number: title}. Outputs: {} if the file is missing."""
    if not os.path.exists(LOCK):
        return {}
    with open(LOCK, encoding="utf-8") as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def write_lock(cards) -> None:
    """Record every card's number and title in pose_numbers.json. Side effects: rewrites the file."""
    with open(LOCK, "w", encoding="utf-8") as fh:
        json.dump({str(c.n): c.title for c in cards}, fh, ensure_ascii=False, indent=0)
        fh.write("\n")


def check_lock(cards) -> list:
    """Each locked number keeps its title, and every card is locked. Outputs: problems."""
    lock, problems = read_lock(), []
    by_n = {c.n: c for c in cards}
    for n, title in sorted(lock.items()):
        if n not in by_n:
            problems.append("pose %d %r is in pose_numbers.json but no card has that number" % (n, title))
        elif by_n[n].title != title:
            problems.append("pose %d was %r and is now %r. Pose numbers are public links: give the new card "
                            "a new number, or, for a deliberate rename, run build.py --lock" % (n, title, by_n[n].title))
    new = [c.n for c in cards if c.n not in lock]
    if new:
        problems.append("poses %s are not in pose_numbers.json yet: run build.py --lock to record them" % new)
    return problems


def check_titles(cards) -> list:
    """Titles must be unique. Outputs: problems."""
    seen, problems = {}, []
    for c in cards:
        if c.title in seen:
            problems.append("poses %d and %d share the title %r" % (seen[c.title], c.n, c.title))
        seen.setdefault(c.title, c.n)
    return problems


def check_tags(cards, groups) -> list:
    """Exactly one tag per group, in group order. Outputs: problems."""
    problems = []
    for c in cards:
        if len(c.tags) != len(groups) or any(t not in ts for t, (_, ts) in zip(c.tags, groups)):
            want = " ".join("<%s>" % g for g, _ in groups)
            problems.append("pose %d %r: tags %s should be one per group, in order: %s" % (c.n, c.title, c.tags, want))
    return problems


def check_text(cards) -> list:
    """No straight double quotes; tips are one or two sentences. Outputs: problems."""
    problems = []
    for c in cards:
        for field in ("title", "pose", "frame", "alt"):
            if '"' in (getattr(c, field) or ""):
                problems.append("pose %d %s: use typographic quotes (“ ”) instead of \"" % (c.n, field))
        for field in ("pose", "frame"):
            count = len(SENTENCE_END.findall(getattr(c, field)))
            if not 1 <= count <= 2:
                problems.append("pose %d %s tip has %d sentences; keep it to one or two" % (c.n, field, count))
    return problems


def check_svg(rendered: dict) -> list:
    """Every drawing parses as XML. Inputs: {number: svg markup}. Outputs: problems."""
    problems = []
    for n, markup in sorted(rendered.items()):
        try:
            ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">' + markup + "</svg>")
        except ET.ParseError as e:
            problems.append("pose %d drawing is not valid SVG: %s" % (n, e))
    return problems


def run_all(cards, groups, rendered: dict, lock: bool = True) -> list:
    """Run every check. Inputs: sorted cards, filter groups, rendered SVG by number, and
    whether to check pose_numbers.json. Outputs: all problems found."""
    problems = check_numbers(cards) + check_titles(cards) + check_tags(cards, groups)
    problems += check_text(cards) + check_svg(rendered)
    if lock:
        problems += check_lock(cards)
    return problems
