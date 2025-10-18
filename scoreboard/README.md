# Scoreboard Submodule Placeholder

This directory is reserved for the live scoreboard application. Convert it into a Git submodule that points to the
Next.js project used for the event (for example: `vest-puzzles-scoreboard`).

## Setup Checklist

1. Create the scoreboard repository (Next.js + App Router).
2. Add it here as a submodule:
   ```bash
   git submodule add <scoreboard-repo-url> scoreboard
   ```
3. Provide an `.env.example` inside the scoreboard repo containing:
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`
   - `SCOREBOARD_HMAC_SECRET`
   - Optional: `SCOREBOARD_ADMIN_TOKEN`
4. Deploy the app on Vercel and record the public submission endpoint. Teams need this URL when running
   `evaluate.py` (export it as `SCOREBOARD_URL`).
5. Document npm scripts (`dev`, `lint`, `test`, `start`) and any additional setup steps in the submodule README.

Until the submodule is added, this placeholder ensures the directory exists so instructions in the main repo remain
consistent.

## API Checklist

The app should expose the following endpoints once implemented:

- `POST /api/evaluate` – accepts multipart uploads (metadata + bundle ZIP), runs evaluation, and stores scores.
- `GET /api/scoreboard` – public leaderboard feed.
- `POST /api/submit` – optional internal hook if you need to push scores separately.
- `POST /api/reset` – admin-only reset.

Store secrets in Vercel env vars (`UPSTASH_*`, `GPT5_API_KEY`, `EVALUATE_HMAC_SECRET`, etc.) and keep the GPT key server-side only.
