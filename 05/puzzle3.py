"""Puzzle 3: split-and-reverse interleave.

The ``garble`` function pulls out all even-indexed characters from the input
(first character = index 0), then appends the odd-indexed characters in reverse
order. ``GARBLE`` is the result of applying this to an undisclosed sentence.
Recover the original sentence.
"""

from __future__ import annotations


def garble(text: str) -> str:
    return text[::2] + text[1::2][::-1]


GARBLE = "hde haelasars esrseuamsoc pe srpndi"

# Find the sentence made entirely of lowercase letters and spaces whose garbled
# form equals GARBLE.
