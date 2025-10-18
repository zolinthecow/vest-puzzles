# Ungarbling

Each puzzle in this folder hides a sentence that was transformed by a small
piece of Python code. Inspect the code, understand how the transformation
works, and recover the original sentence.

## Files

- `puzzle1.py` – modular offset puzzle
- `puzzle2.py` – triple-stream modular puzzle
- `puzzle3.py` – split-and-reverse interleave puzzle
- `SOLUTION.md` – submit your three decoded sentences here

The `GARBLE` constant in each Python file stores the data you are given. The
helper function in that file shows how the data was generated from the hidden
sentence. Reverse the process to recover the original string.

## Submission

Create or edit `SOLUTION.md` so it contains exactly three lines:

1. Solution to `puzzle1`
2. Solution to `puzzle2`
3. Solution to `puzzle3`

Do not add extra whitespace or commentary—just the sentences.

## Running

`run.sh` simply prints `SOLUTION.md`. The evaluator compares your answers to the
expected strings.
