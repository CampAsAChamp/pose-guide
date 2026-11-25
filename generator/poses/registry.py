"""The card registry: the @card decorator, the tag codes and the Card record.

Every pose module decorates its drawing functions with @card, which appends a
Card to REG. This module imports nothing else from the package, so any module
(including samples.py, which the scene helpers depend on) can use it without
an import cycle.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

# Short tag codes used in @card, one per filter group, in group order.
TAGS = {"S": "Solo", "P": "Partner", "G": "Group",
        "St": "Standing", "Le": "Leaning", "Wa": "Walking", "Se": "Seated", "Cr": "Crouching", "Ly": "Lying",
        "Ac": "Action", "Mx": "Mixed Levels",
        "W": "Wide", "F": "Full Length", "T": "Three-Quarter", "U": "Waist Up", "C": "Close-Up",
        "Str": "Street", "Par": "Park", "Bea": "Beach", "Fie": "Field", "Vie": "Viewpoint", "Wat": "Waterfront",
        "Ste": "Steps", "Caf": "Café", "Hom": "Home", "Stu": "Studio",
        "f": "Facing Camera", "s": "Side-On", "b": "Back to Camera"}

# The filter groups shown on the page, in order. Each card has exactly one tag from each.
GROUPS = [
    ("People", ["Solo", "Partner", "Group"]),
    ("Pose", ["Standing", "Leaning", "Walking", "Seated", "Crouching", "Lying", "Action", "Mixed Levels"]),
    ("Shot", ["Wide", "Full Length", "Three-Quarter", "Waist Up", "Close-Up"]),
    ("Setting", ["Street", "Park", "Beach", "Field", "Viewpoint", "Waterfront", "Steps", "Café", "Home", "Studio"]),
    ("Angle", ["Facing Camera", "Side-On", "Back to Camera"]),
]


@dataclass(frozen=True)
class Card:
    """One pose card.

    n: pose number (the #pose-N link), fixed forever once published.
    title, pose, frame: visible text (title, posing tip, framing tip).
    tags: one tag name per group, in GROUPS order.
    draw: returns the inner SVG markup for a 600 x 800 viewBox.
    alt: optional description of the drawing for screen readers.
    """
    n: int
    title: str
    tags: list
    draw: Callable[[], str]
    pose: str
    frame: str
    alt: Optional[str] = None


REG: list = []


def card(n: int, title: str, tags: str, pose: str, frame: str, alt: Optional[str] = None):
    """Register the decorated drawing function as pose number n.

    tags is a space-separated string of codes from TAGS, e.g. "S St F Str f".
    Raises ValueError for an unknown tag code so the mistake names the card.
    """
    names = []
    for code in tags.split():
        if code not in TAGS:
            raise ValueError("pose %s %r: unknown tag code %r (see TAGS in poses/registry.py)" % (n, title, code))
        names.append(TAGS[code])

    def deco(fn):
        REG.append(Card(n, title, names, fn, pose, frame, alt))
        return fn
    return deco
