# Tiled Matrix Multiplication

You are given two square matrices `A` and `B`, each of dimension `2^d × 2^d`, where `d ≥ 0`.
Your goal is to compute `C = A × B` using a recursive divide-and-conquer algorithm that repeatedly splits matrices
into quadrants.

## Input Format

1. First line: integer `d` (`0 ≤ d ≤ 6`).
2. Next `2^d` lines: matrix `A`, one row per line, with entries separated by spaces.
3. Final `2^d` lines: matrix `B`, in the same row-major format.

All matrix entries are integers in the range `[-10^4, 10^4]`.

## Output Format

Print matrix `C` in row-major order: `2^d` lines, each containing `2^d` space-separated integers.

## Requirements

- Implement the multiplication using a recursive quadrant layout. Let `A11` denote the top-left quadrant, `A12` the
  top-right, `A21` the bottom-left, and `A22` the bottom-right (and similarly for `B` and `C`).
- The recursion should follow the identities:
  - `C11 = A11·B11 + A12·B21`
  - `C12 = A11·B12 + A12·B22`
  - `C21 = A21·B11 + A22·B21`
  - `C22 = A21·B12 + A22·B22`
- Base case occurs when `d = 0` (each matrix is 1×1).

## Sample

Input
```
1
1 2
3 4
5 6
7 8
```

Output
```
19 22
43 50
```

The sample corresponds to multiplying two 2×2 matrices.
