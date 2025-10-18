# Conductors' Fugue

Maestro Aria composed a looping melody of length `N`, using notes from `{a, b, c, d, e, f, g}`. The apprentices tried to
transcribe it, but ended up with three partial logs instead of the full score:

1. **Cadence log** – every time a certain beat came around (unknown to us), they wrote down the note heard on that beat
   and the note three beats later. Each entry is an ordered pair `(x, y)` interpreted as:
   > whenever the melody plays note `x` at one of the monitored beats, the note three steps ahead (modulo `N`) is `y`.

   The log covers exactly one residue class modulo 3 of the loop (e.g. all beats congruent to `r (mod 3)`), but the
   entries appear in arbitrary order.

2. **Pickup log** – for that same set of beats, another apprentice wrote down the note immediately *before* each of the
   monitored notes. Each entry `(x, z)` means:
   > immediately before every occurrence of note `x` at those beats, the melody plays note `z`.

   The order is arbitrary; the set of monitored beats matches the cadence log.

3. **Run fragment** – a visiting conductor captured a contiguous fragment of the melody (wrapping allowed). The fragment
   appears exactly as the melody plays it, but the starting index within the loop is unknown. Its length `M` satisfies
   `ceil(N / 2) ≤ M ≤ N`.

Your task is to reconstruct the entire melody in the original forward order.

## Input Format

```
N
C
x1 y1
x2 y2
...
xC yC
P
u1 v1
u2 v2
...
uP vP
M
fragment
```

- `N` – length of the melody loop (`3 ≤ N ≤ 10^5`).
- `C` – number of cadence entries (equal to the number of monitored beats).
- Next `C` lines – cadence pairs `(xi, yi)` with `xi, yi ∈ {a,…,g}`.
- `P` – number of pickup entries (`P = C`).
- Next `P` lines – pickup pairs `(ui, vi)` with `ui, vi ∈ {a,…,g}`.
- `M` – length of the run fragment (`ceil(N / 2) ≤ M ≤ N`).
- `fragment` – a string of length `M`, the contiguous slice of the melody.

You may assume the logs are consistent and describe exactly one melody loop.

## Output Format

Output the complete melody as a string of length `N`, starting from the first note in the original loop (i.e., aligned
with the run fragment’s orientation). Do not print additional whitespace.

## Example

```
Input
12
4
c f
f a
a d
d g
4
c b
f c
a f
d a
7
cadfgac

Output
cadfgacdfgba
```

In this example, the cadence log states that every monitored `c` is followed three beats later by `f`, every monitored
`f` by `a`, and so on. The pickup log reveals the notes immediately preceding those monitored beats. Once you combine the
three interleaving progressions and align them using the run fragment `cadfgac`, the full melody `cadfgacdfgba` is
recovered.
