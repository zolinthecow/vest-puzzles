# Implementation Summary (Language-Agnostic)

This document captures the implemented structure for making each puzzle codeable, running evaluations, and hosting the
scoreboard while preserving language freedom wherever possible.

## 1. Making Each Puzzle Codeable

Repo-wide conventions:
- Each `0X/` folder contains a `PROBLEM.md` with the canonical IO specification and, except for Puzzle 01, exactly one
  illustrative sample. Puzzle 01 intentionally ships without a sample.
- `run.sh` is the only required entry point. Contestants edit the script to compile/run their solution in whatever
  language they like, unless otherwise noted.
- No language-specific scaffolding (e.g., `main.py`) is provided; the repo stays neutral.

### 01 – Sneaky Islanders
- Clear input/output description plus logical notes in `PROBLEM.md`.
- `run.sh` emits an instructional error until teams customize it. No helper code or fixtures are distributed.

### 02 – Tiled Matrix Multiplication
- `PROBLEM.md` specifies the serialization format (`d`, rows of `A`, rows of `B`) and includes a single 2×2 sample.
- `run.sh` is a stub; teams configure it to run their recursive solver.

### 03 – Conductors' Fugue
- Contestants reconstruct a cyclic melody from three complementary logs (cadence pairs, pickup pairs, and a long run
  fragment).
- The puzzle hinges on spotting how the logs describe interleaved residue classes modulo three; once aligned with the
  run fragment the melody is determined.
- `run.sh` stays a stub so teams can wire their solver in any language.

### 04 – The Dancing Grid
- Contestants now import `grid_api.run_dancing_grid(left_feed, top_feed)`. The helper runs the grid for exactly `N` ticks
  while they control the injected values each tick.
- Problem statement explains the feed format (rows × ticks for the left edge, columns × ticks for the top edge) and
  allows `None` to skip injections.
- Teams focus on preprocessing the matrices to align values with the grid wavefront; no JSON protocols or drivers are
  required.

### 05 – Ungarbling
- Three standalone Python files (`puzzle1.py`–`puzzle3.py`) showcase the garbling logic and expose `GARBLE` data.
- Contestants reverse the transformations and record their answers in `SOLUTION.md` (three lines, one per puzzle).
- `run.sh` prints `SOLUTION.md`; the evaluator compares the lines against the expected strings.

## 2. Remote Evaluation Service

Official scoring happens through a remote `POST /api/evaluate` endpoint hosted in the scoreboard Next.js app. Each submission uploads a ZIP archive with the numbered puzzle directories (`01/`–`05/`) and optional metadata. The server:

1. Extracts the archive into a sandboxed workspace.
2. Runs the shared `evaluate.py` harness (same deterministic tests as local) inside a managed process.
3. Routes Puzzle 03 strategy write-ups to GPT-5-mini using organizer-owned credentials so API keys remain private.
4. Stores the resulting scores in Upstash Redis and streams a JSON summary back to the client.

Operational notes:
- Serialize or queue evaluation jobs to avoid resource contention; large events may require dedicated worker pods.
- Enforce per-run time/memory limits equivalent to the local harness.
- Sign responses (e.g., HMAC header) so clients can verify they came from the trusted service.

## 3. Local Tooling

Participants can still run `python3 evaluate.py` for offline feedback, but official results come from the server. A new helper script (`submit.py`) bundles the directories, reads `.profile` for the team name, and uploads the ZIP via `POST /api/evaluate`. Environment variable `EVALUATE_URL` controls the destination; `EVALUATE_TOKEN` can carry an optional bearer credential.

## 4. Scoreboard Submodule Placeholder

- `scoreboard/` remains a placeholder for the Next.js app. The app must expose:
  - `POST /api/evaluate` – handles uploads, orchestrates evaluation, and persists scores.
  - `GET /api/scoreboard` – returns the current leaderboard.
  - `POST /api/submit` – optional direct score upsert (used internally by the evaluator).
  - `POST /api/reset` – admin reset endpoint.
- Required environment variables: Upstash credentials, GPT-5-mini API key/endpoint, HMAC secret, maximum upload size, and any job-queue configuration.



With this setup the repo remains language-agnostic, the evaluation harness is self-contained, and the scoreboard flow
is documented pending submodule wiring.
This setup keeps contestant workflows language-agnostic while centralizing official scoring behind the Next.js evaluation service.
