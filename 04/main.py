from __future__ import annotations

import sys
from typing import List, Optional

from grid_api import run_dancing_grid


def read_matrix(n: int, it) -> List[List[int]]:
    return [[int(next(it)) for _ in range(n)] for _ in range(n)]


def build_feeds(a: List[List[int]], b: List[List[int]]) -> tuple[List[List[Optional[int]]], List[List[Optional[int]]]]:
    """Construct feeds for the Dancing Grid.

    TODO: Replace this placeholder with logic that schedules values so the grid
    accumulators equal A x B after N ticks.
    """
    n = len(a)
    left = [[None for _ in range(n)] for _ in range(n)]
    top = [[None for _ in range(n)] for _ in range(n)]
    return left, top


def main() -> None:
    tokens = sys.stdin.read().strip().split()
    if not tokens:
        raise SystemExit("Empty input")
    it = iter(tokens)
    n = int(next(it))
    a = read_matrix(n, it)
    b = read_matrix(n, it)
    left_feed, top_feed = build_feeds(a, b)
    result = run_dancing_grid(left_feed, top_feed)
    for row in result:
        print(" ".join(str(x) for x in row))


if __name__ == "__main__":
    main()
