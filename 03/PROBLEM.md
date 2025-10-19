# Divisible Subarray

You are given an array of `N` integers `a_1, a_2, …, a_N`. Determine whether
there exists a non-empty contiguous subarray whose sum is divisible by `N`. If
such a subarray exists, output one example using 1-based indices.

This is the classic pigeonhole-principle result: for every array there is at
least one valid subarray. Your program must find (and print) any one of them.

## Input

```
N
a_1 a_2 … a_N
```

- `1 ≤ N ≤ 2 · 10^5`
- `|a_i| ≤ 10^9`

## Output

Print `YES` on the first line. On the second line print two integers `l r`
(`1 ≤ l ≤ r ≤ N`) such that `a_l + a_{l+1} + … + a_r` is divisible by `N`.

If for some reason your program believes no such subarray exists, print `NO`
(in official tests, `YES` will always be the correct answer).

## Example

**Input**
```
5
3 1 4 2 2
```

**Output**
```
YES
2 3
```

Explanation: `a_2 + a_3 = 1 + 4 = 5`, and `5` is divisible by `N = 5`.
