from __future__ import annotations

import sys
from typing import List, Optional

from grid_api import run_dancing_grid


def read_matrix(n: int) -> List[List[int]]:
    matrix = []
    for _ in range(n):
        row = list(map(int, sys.stdin.readline().split()))
        if len(row) != n:
            raise ValueError("Each matrix row must have exactly N integers")
        matrix.append(row)
    return matrix


def build_feeds(a: List[List[int]], b: List[List[int]]) -> tuple[List[List[Optional[int]]], List[List[Optional[int]]]]:
    """Construct placeholder feeds for run_dancing_grid.

    Replace this logic with your preprocessing so that the grid accumulators equal A x B.
    """
    n = len(a)
    left_feed: List[List[Optional[int]]] = [[None for _ in range(n)] for _ in range(n)]
    top_feed: List[List[Optional[int]]] = [[None for _ in range(n)] for _ in range(n)]

    # TODO: populate left_feed and top_feed with your schedule.
    # This stub simply injects zeros and will not compute the correct product.
    return left_feed, top_feed


def main() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        raise SystemExit("Input is empty")
    it = iter(data)
    n = int(next(it))

    # Reconstruct matrices row by row using the iterator for clarity.
    a = [[int(next(it)) for _ in range(n)] for _ in range(n)]
    b = [[int(next(it)) for _ in range(n)] for _ in range(n)]

    left_feed, top_feed = build_feeds(a, b)
    c = run_dancing_grid(left_feed, top_feed)

    for row in c:
        print(" ".join(str(x) for x in row))


if __name__ == "__main__":
    main()
