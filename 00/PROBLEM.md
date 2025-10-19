# Two-Sum Warmup

Given a list of integers and a target value, find two **distinct** indices whose
values add up to the target. Each puzzle instance is guaranteed to have exactly
one valid answer.

## Input Format

- First line: integer `N` (`2 ≤ N ≤ 200`).
- Second line: `N` space-separated integers `a_0 ... a_{N-1}`.
- Third line: integer `T` — the target sum.

## Output Format

Print two space-separated indices `i j` (0-based, `i < j`) such that
`a_i + a_j = T`.

If no such pair exists (should not occur in official tests), output `-1 -1`.

## Example

**Input**
```
5
2 7 11 15 9
9
```

**Output**
```
0 1
```

Either order (`1 0`) is acceptable as long as the indices are distinct and sum
to the target.
