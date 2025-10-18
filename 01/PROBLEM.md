# Sneaky Islanders

You are standing in front of a line of 10 islanders. Each islander `i` states:

> "Exactly `N_i` of us are telling the truth."

where `N_i` is the integer the islander provides.

## Task

Given the 10 integers `N_0, N_1, ..., N_9` (one per islander, in order), determine which islanders are telling the
truth.

## Input Format

- Input is exactly one line containing 10 space-separated integers.
- Every integer is in the inclusive range `[0, 10]`.

## Output Format

- First line: a single integer `T` representing the number of islanders whose statements are truthful.
- Second line: `T` space-separated indices (0-based) of the islanders who are telling the truth. List the indices in
  strictly increasing order.
- If there is no consistent assignment, output `0` on the first line and leave the second line empty (either produce an
  empty line or omit it entirely).

If multiple assignments are valid, print any one of them.

## Notes

- An islander tells the truth when their reported `N_i` equals the total count of truthful islanders.
