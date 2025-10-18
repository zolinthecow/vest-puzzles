from __future__ import annotations

from typing import Iterable, List, Optional


def run_dancing_grid(
    left_feed: Iterable[Iterable[Optional[int]]],
    top_feed: Iterable[Iterable[Optional[int]]],
) -> List[List[int]]:
    """Simulate the Dancing Grid for exactly N ticks.

    Args:
        left_feed: N sequences of length N. left_feed[r][t] is injected on the left
            edge of row r at tick t. Use None to skip injection on that tick.
        top_feed: N sequences of length N. top_feed[c][t] is injected on the top
            edge of column c at tick t. Use None to skip injection on that tick.

    Returns:
        The N x N matrix of accumulators after N ticks.
    """

    left = [list(row) for row in left_feed]
    top = [list(col) for col in top_feed]
    if not left or not top or len(left) != len(top):
        raise ValueError("left_feed and top_feed must have the same non-zero length")

    n = len(left)
    if any(len(row) != n for row in left):
        raise ValueError("Each row in left_feed must have length N")
    if any(len(col) != n for col in top):
        raise ValueError("Each column in top_feed must have length N")

    accumulators: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]
    a_pipe: List[List[Optional[int]]] = [[None for _ in range(n)] for _ in range(n)]
    b_pipe: List[List[Optional[int]]] = [[None for _ in range(n)] for _ in range(n)]

    for tick in range(n):
        next_a_pipe: List[List[Optional[int]]] = [[None for _ in range(n)] for _ in range(n)]
        next_b_pipe: List[List[Optional[int]]] = [[None for _ in range(n)] for _ in range(n)]
        for r in range(n):
            for c in range(n):
                if c == 0:
                    a_val = left[r][tick]
                else:
                    a_val = a_pipe[r][c - 1]
                if r == 0:
                    b_val = top[c][tick]
                else:
                    b_val = b_pipe[r - 1][c]

                if a_val is not None and b_val is not None:
                    accumulators[r][c] += int(a_val) * int(b_val)

                next_a_pipe[r][c] = a_val
                next_b_pipe[r][c] = b_val
        a_pipe = next_a_pipe
        b_pipe = next_b_pipe

    return accumulators
