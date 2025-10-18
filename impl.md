# Repo implementation

This repo is for a coding event that I'm gonna run. Basically, I will have people clone this repo and try to solve the problems.
The idea is that in each folder (01/ 02/ 03/ 04/ 05/) people can write their solutions in code and edit the `run.sh` to give a 
standardized way to run the code. Then, we have some `evaluate.py` script or something along those lines that will run test cases
and assign a score. It should then post the result to some endpoint and update a scoreboard.

The scoreboard should be a submodule in this repo so that people don't have to clone a whole NextJS app. We should make it with
create-next-app and it can be very simple. Just a scoreboard with a public POST endpoint to register users and update their scores.

## Implementation

There are three separate things I need you to help implement. A way for each problem to actually be codeable, an evaluation script,
and the scoreboard.

### A way for each problem to actually be codeable.

If you look at each of the problem statements in the file, some are pretty straightfoward to code and some are not. For example,
in `01/` it's pretty simple to code it. However, in `04/` (the systolic array one) it's pretty difficult to set this problem up.
We need a way to provide the FMA cells and a way to evaluate the runtime of the team's solution. I think that's nontrivial because
if you had actual hardware the systolic array would be O(N) but when implementing a systolic array in code it's still O(N^3). 

Please look through every single problem and propose a solution for making it codeable.

### Evaluation script

Once every single problem is codeable, we need an evaluation script as well. It should run all of the `run.sh` against a bunch of
pregenerated test cases and assign a score. Also, the first time someone runs it it should prompt them for their team name and then
register it in the scoreboard database. I think the way we should handle that at least is in the root of the `vest-puzzles/` directory
we can just have a file called `.profile` that it reads from. And then if it detects a duplicate team name it should just not create
a new one. And then subsequent evaluations can be submitted via the name stored in `.profile`.

We also need to generate test cases for every single problem, and figure out how to evaluate correctness and time complexity for `04/`.
Please propose a solution for this as well.

### Scoreboard

We should have a submodule for the scoreboard that's a nextjs app that's deployed to vercel. I think we can just use an upstash redis
instance to store the team names and their scores. The app should just be a scoreboard, and expose one endpoint for upserting a team's
score. On registration it would just be upserting a team with score 0. The scoreboard needs to update in real time every time a team
score gets updated.

Please propose a solution for this.
