from __future__ import annotations

import sys
from typing import List


def solve(statements: List[int]) -> List[int]:
    candidates: List[List[int]] = []
    for t in range(11):
        truthful = [i for i, val in enumerate(statements) if val == t]
        if len(truthful) == t:
            candidates.append(truthful)
    if not candidates:
        return []
    candidates.sort(key=lambda arr: (len(arr), arr))
    return candidates[0]


def main() -> None:
    tokens = sys.stdin.read().strip().split()
    if len(tokens) != 10:
        raise SystemExit("Expected 10 integers")
    statements = [int(tok) for tok in tokens]
    truthful = solve(statements)
    print(len(truthful))
    if truthful:
        print(" ".join(str(i) for i in truthful))
    else:
        print()


if __name__ == "__main__":
    main()
