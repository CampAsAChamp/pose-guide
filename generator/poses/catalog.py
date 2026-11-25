"""The pose catalogue: every registered card, sorted by pose number.

Importing the card modules runs their @card decorators, which fill
registry.REG. Each Card's number is written in its decorator, so the order
of the imports below does not matter.
"""
from . import samples, cards_b, cards_c, cards_d, cards_e, cards_f, cards_g, cards_h, cards_i  # noqa: F401
from .registry import GROUPS, REG, Card  # noqa: F401  (re-exported for build.py and preview.py)

CARDS = sorted(REG, key=lambda c: c.n)
