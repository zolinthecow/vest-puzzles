# Vest Puzzles

Welcome to the Vest puzzles event! Each numbered folder (`01/`–`05/`) contains a problem statement (`PROBLEM.md`) and a
`run.sh`. Edit the script to compile/run your solution in the language of your choice—other than the special cases
below, nothing else is imposed.

| Puzzle | Notes |
| ------ | ----- |
| 01 – Sneaky Islanders | Input/output spec only—provide your own tooling. |
| 02 – Tiled Matrix Multiplication | Recursion-focused matrix multiply. Includes a single illustrative sample in the statement. |
| 03 – Conductors' Fugue | Reconstruct a cyclic melody from cadence/pickup logs plus a long fragment. |
| 04 – The Dancing Grid | Import `grid_api.run_dancing_grid`, preprocess feeds, and let the grid run for exactly N ticks. |
| 05 – Ungarbling | Inspect `puzzle1.py`–`puzzle3.py`, decode the sentences, and list them in `SOLUTION.md`. |

## Evaluation

Official scoring happens through the remote `POST /api/evaluate` endpoint inside the scoreboard Next.js app. Use
`submit.py` to package your solutions and upload them:

```bash
python3 submit.py --zip submissions.zip
```

By default the script reads `EVALUATE_URL`; override with `--url https://your-app.vercel.app/api/evaluate` if needed.
Set `EVALUATE_TOKEN` when the endpoint expects bearer auth. The helper reads `.profile` for your team name (prompting if
it doesn’t exist) and streams progress as the server evaluates each puzzle.

### Local Spot Checks

You can still run `python3 evaluate.py` for quick feedback during development, but leaderboard results only count once
they’ve been processed by the remote service. Use familiar flags like `--problem` and `--verbose` to target specific
puzzles locally.

## Scoreboard Submodule

The directory `scoreboard/` is reserved for the live leaderboard (Next.js on Vercel backed by Upstash Redis). Replace
the placeholder with an actual Git submodule when the app is ready:

```bash
git submodule add <scoreboard-repo-url> scoreboard
```

Inside that repo, expose:

- `/api/submit` for upserting scores (authenticated via HMAC token)
- `/api/scoreboard` for public leaderboard data
- Optional `/api/reset` for admin resets

Document required environment variables in `scoreboard/.env.example` and provide npm scripts (`dev`, `lint`, `test`,
`start`).

## Repository Docs

Additional implementation details live in `docs/implementation_proposal.md`. Refer to that design doc when extending
the evaluator, adding private test cases, or wiring the scoreboard deployment pipeline.

Good luck, and have fun solving!
