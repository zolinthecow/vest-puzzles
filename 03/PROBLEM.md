# Divisible Subarray

You are given an array of `N` integers `a_1, a_2, …, a_N`. Determine whether
there exists a non-empty contiguous subarray whose sum is divisible by `N`.

It is a known fact (pigeonhole principle) that for any array there is always at
least one such subarray. Your program should therefore output `YES` for every
valid input. However, to keep the statement complete, the required output format
still asks for a simple `YES`/`NO` decision.

## Input

```
N
a_1 a_2 … a_N
```

- `1 ≤ N ≤ 2 · 10^5`
- `|a_i| ≤ 10^9`

## Output

Print `YES` if there exists a contiguous subarray whose sum is divisible by `N`,
otherwise print `NO`. (In official tests the answer will always be `YES`.)

## Example

**Input**
```
5
3 1 4 2 2
```

**Output**
```
YES
```
