"""Puzzle 2: modular triple streams.

The helpers below describe the garbling pipeline used on a hidden ASCII string.
Each list records a stream of numbers derived from the same sentence.
Reconstruct the original string that produced the data.
"""

from __future__ import annotations

from typing import Dict, List


def garble(text: str) -> Dict[str, List[int]]:
    return {
        "a": [((ord(ch) * 12) % 8) + idx for idx, ch in enumerate(text)],
        "b": [((ord(ch) * 12) % 7) + idx for idx, ch in enumerate(text)],
        "c": [((ord(ch) * 12) % 36) + idx for idx, ch in enumerate(text)],
    }


GARBLE = {
    "a": [4, 5, 2, 7, 4, 9, 10, 11, 8, 9, 10, 15, 12, 17, 14, 15, 20, 17, 22, 19, 24, 21, 22, 27, 28, 29, 30, 27, 32, 29, 34],
    "b": [6, 2, 3, 5, 7, 5, 7, 8, 14, 15, 13, 13, 14, 14, 15, 21, 18, 18, 20, 23, 24, 27, 25, 23, 26, 29, 28, 31, 30, 30, 31],
    "c": [12, 25, 2, 3, 16, 5, 30, 19, 32, 33, 10, 23, 24, 37, 14, 39, 28, 17, 18, 43, 32, 45, 34, 23, 36, 37, 26, 51, 40, 29, 42],
}

# Recover the original string whose garbled data matches GARBLE.
# Hint: all letters are lowercase and the sentence contains spaces.
