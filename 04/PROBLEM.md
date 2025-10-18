# The Dancing Grid

You are given two `N × N` integer matrices `A` and `B`. Your goal is to produce `C = A × B` using a magical grid of
multiply–accumulate processors. The grid operates for exactly `N` ticks. On each tick:

- Every row `r` receives a single value on its left edge.
- Every column `c` receives a single value on its top edge.
- Each cell multiplies the value currently inside it from the left with the value currently inside it from the top (if
  both are present) and adds the product to its running total. Afterwards, the left value moves one cell to the right
  and the top value moves one cell down for the next tick.

Values simply propagate; you cannot pause them once they enter the grid.

## What You Can Control

You may preprocess or rearrange copies of `A` and `B` however you like. When you are ready, call the helper
`run_dancing_grid(left_feed, top_feed)` provided in `grid_api.py`.

- `left_feed` must be a list of `N` lists. `left_feed[r][t]` is the value injected into row `r` at tick `t`.
- `top_feed` must be a list of `N` lists. `top_feed[c][t]` is the value injected into column `c` at tick `t`.
- Each list entry may be an integer or `None`. Supplying `None` skips injection for that row/column on that tick.
- After `N` ticks, `run_dancing_grid` returns the `N × N` matrix of cell accumulators.

The challenge is to choose `left_feed` and `top_feed` so that, despite the rigid grid rules, the accumulators match
`A × B` exactly at the end of the `N` ticks.

You may **not** modify `run_dancing_grid` or the grid mechanics. Your solver should transform the inputs and call the
helper as many times as needed.

## Input

Standard input provides `N`, followed by matrix `A` and matrix `B` in row-major order:

```
N
A[0][0] A[0][1] ... A[0][N-1]
A[1][0] ...
...
B[0][0] ...
...
```

## Output

Print the resulting matrix `C` in row-major order—`N` lines, each with `N` integers separated by spaces.

## Tools in `04/`

- `grid_api.py` exposes `run_dancing_grid`, the only interface to the grid.
- `run.sh` is a stub—edit it so it runs your solver.

## Example

Remember: you can manipulate the feeds however you want, but the grid itself always runs for exactly `N` ticks.
