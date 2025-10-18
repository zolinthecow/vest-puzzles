"""Puzzle 1: modular offsets.

The function below shows how a plain-text string is garbled. The list ``GARBLE``
was produced by running ``garble(SECRET)`` for some ASCII string ``SECRET``.
Recover the original string.
"""

from __future__ import annotations

from typing import List


def garble(text: str) -> List[int]:
    return [(ord(ch) + idx) % 11 for idx, ch in enumerate(text)]


GARBLE = [6, 6, 4, 2, 5, 3, 6, 7, 3, 9, 3, 10, 5, 6, 9, 5, 4, 3, 9, 10, 0, 4, 10, 7, 8, 2, 6]

# Recover the ASCII string whose garbled representation is GARBLE.
# Tip: every character stayed printable in the original sentence.
