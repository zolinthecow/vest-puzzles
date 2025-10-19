# Vest Puzzles

Welcome to the Vest puzzles event! Each numbered folder (`01/`–`05/`) contains a problem statement (`PROBLEM.md`) and a
`run.sh`. Edit the script to compile/run your solution in the language of your choice—other than the special cases
below, nothing else is imposed.

| Puzzle | Notes |
| ------ | ----- |
| 00 – Two-Sum Warmup | Find two indices that sum to a target. |
| 01 – Sneaky Islanders | Input/output spec only—provide your own tooling. |
| 02 – Tiled Matrix Multiplication | Recursion-focused matrix multiply. Includes a single illustrative sample in the statement. |
| 03 – Divisible Subarray | Output a contiguous segment whose sum is divisible by N. |
| 04 – The Dancing Grid | Import `grid_api.run_dancing_grid`, preprocess feeds, and let the grid run for exactly N ticks. |
| 05 – Ungarbling | Inspect `puzzle1.py`–`puzzle3.py`, decode the sentences, and list them in `SOLUTION.md`. |

## Evaluation

Run `python3 evaluate.py`. The script reads `.profile` for your team name (prompting if
missing), executes every `run.sh`, and writes a breakdown to `results/latest.json`.

By default the script also submits to <https://vest-puzzles-scoreboard.vercel.app/api/submit>. To target a different
deployment, override `SCOREBOARD_URL` before running the evaluator:

```bash
export SCOREBOARD_URL="https://your-app.vercel.app/api/submit"
python3 evaluate.py
```

Use `--no-submit` if you want to keep a run local even when the variable is set.

### Local Spot Checks

You can still run `python3 evaluate.py` for quick feedback during development, but leaderboard results only count once
they’ve been pushed to the scoreboard. Use familiar flags like `--problem` and `--verbose` to target specific puzzles.

## Scoreboard Submodule

The `scoreboard/` directory contains the Next.js app that serves the live leaderboard. It accepts JSON submissions at
`/api/submit` and exposes the table via `/api/scoreboard`. See `scoreboard/README.md` for environment variables and
development instructions.

## Repository Docs

Additional implementation details live in `docs/implementation_proposal.md`. Refer to that design doc when extending
the evaluator, adding private test cases, or wiring the scoreboard deployment pipeline.

Good luck, and have fun solving!
