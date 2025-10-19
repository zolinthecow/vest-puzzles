from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time
import ssl
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple, cast
from urllib import request, error

PROFILE_PATH = Path(".profile")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)
LATEST_RESULTS_PATH = RESULTS_DIR / "latest.json"


@dataclass
class TestCase:
    name: str
    input_data: str
    metadata: Dict[str, object] = field(default_factory=dict)


@dataclass
class ProblemResult:
    score: float
    max_score: float
    details: List[str]
    passed: int
    total: int
    elapsed: float


@dataclass
class ProblemSpec:
    pid: str
    name: str
    folder: Path
    generator: Callable[[], Iterable[TestCase]]
    verifier: Callable[[TestCase, str, float], tuple[bool, str]]
    timeout: float
    weight: float


def ensure_team_profile() -> str:
    if PROFILE_PATH.exists():
        content = PROFILE_PATH.read_text().strip()
        if content.startswith("TEAM_NAME="):
            return content.split("=", 1)[1].strip()
    team_name = input("Enter team name: ").strip()
    PROFILE_PATH.write_text(f"TEAM_NAME={team_name}\n")
    return team_name


def run_script(folder: Path, timeout: float, input_data: str, extra_env: Optional[Dict[str, str]] = None) -> tuple[str, float]:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    start = time.time()
    proc = subprocess.run(
        ["bash", "-lc", "./run.sh"],
        cwd=str(folder),
        input=input_data.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
        env=env,
    )
    elapsed = time.time() - start
    stdout = proc.stdout.decode(errors="ignore")
    if proc.returncode != 0:
        stderr = proc.stderr.decode(errors="ignore")
        raise RuntimeError(
            f"run.sh exited with {proc.returncode} in {folder}.\nSTDERR:\n{stderr.strip()}"
        )
    return stdout, elapsed


def list_problems(problems: Dict[str, ProblemSpec]) -> None:
    print("Available problems:")
    for pid, spec in problems.items():
        print(f"  {pid}: {spec.name}")


def judge_problem(spec: ProblemSpec, verbose: bool) -> ProblemResult:
    total_tests = 0
    passed_tests = 0
    details: List[str] = []
    start = time.time()
    for test in spec.generator():
        total_tests += 1
        try:
            stdout, elapsed = run_script(spec.folder, spec.timeout, test.input_data)
            ok, message = spec.verifier(test, stdout, elapsed)
        except Exception as exc:  # pylint: disable=broad-except
            ok = False
            message = str(exc)
            elapsed = 0.0
        if ok:
            passed_tests += 1
            if verbose:
                details.append(f"[{test.name}] PASS ({elapsed:.2f}s)")
        else:
            details.append(f"[{test.name}] FAIL: {message}")
            if verbose:
                details[-1] += f" ({elapsed:.2f}s)"
    elapsed_total = time.time() - start
    score = spec.weight * (passed_tests / total_tests if total_tests else 0.0)
    return ProblemResult(
        score=score,
        max_score=spec.weight,
        details=details,
        passed=passed_tests,
        total=total_tests,
        elapsed=elapsed_total,
    )


def submit_scoreboard(
    url: str,
    payload: dict,
    secret: Optional[str] = None,
    verbose: bool = False,
) -> None:
    headers = {"Content-Type": "application/json"}
    if secret:
        headers["Authorization"] = f"Bearer {secret}"
    req = request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    context: Optional[ssl.SSLContext] = None
    for attempt in range(2):
        try:
            if context is None:
                resp = request.urlopen(req, timeout=5)
            else:
                resp = request.urlopen(req, timeout=5, context=context)
            with resp:
                body = resp.read().decode()
            if verbose:
                print(f"Scoreboard response: {body}")
            return
        except error.URLError as exc:
            ssl_error = isinstance(exc.reason, ssl.SSLError)
            if ssl_error and context is None:
                if verbose:
                    print("Warning: certificate verification failed; retrying without verification.")
                context = ssl._create_unverified_context()  # type: ignore[attr-defined]
                continue
            print(f"Warning: scoreboard submission failed: {exc}")
            return


# -------------------- Problem Generators & Verifiers --------------------

def generate_01_cases() -> Iterable[TestCase]:
    data_sets: List[List[int]] = [
        [0, 2, 6, 5, 4, 2, 3, 5, 1, 1],
        [6, 1, 8, 4, 10, 9, 5, 9, 3, 1],
        [10, 5, 2, 5, 5, 3, 10, 4, 10, 10],
        [1, 9, 10, 2, 8, 3, 2, 7, 6, 4],
        [4, 1, 3, 9, 5, 3, 10, 7, 6, 10],
    ]
    for idx, arr in enumerate(data_sets, start=1):
        yield TestCase(
            name=f"01_case_{idx}",
            input_data=" ".join(str(x) for x in arr) + "\n",
            metadata={"statements": arr},
        )


def verifier_01(test: TestCase, stdout: str, _elapsed: float) -> tuple[bool, str]:
    lines = [line.strip() for line in stdout.strip().splitlines() if line.strip()]
    if not lines:
        return False, "No output produced"
    try:
        truthful_count = int(lines[0])
    except ValueError:
        return False, "First line must be an integer count"

    indices: List[int] = []
    if truthful_count > 0:
        if len(lines) < 2:
            return False, "Missing index list"
        try:
            indices = [int(x) for x in lines[1].split()]
        except ValueError:
            return False, "Index list must contain integers"
        if len(indices) != truthful_count:
            return False, "Number of indices does not match declared truthful count"
        if sorted(indices) != indices:
            return False, "Indices must be in increasing order"
        if len(set(indices)) != len(indices):
            return False, "Duplicate indices detected"
        if any(i < 0 or i >= 10 for i in indices):
            return False, "Index out of range"
    else:
        indices = []

    statements = cast(List[int], test.metadata["statements"])
    valid_assignments = []
    for t in range(11):
        truth = [i for i, val in enumerate(statements) if val == t]
        if len(truth) == t:
            valid_assignments.append((t, truth))
    if not valid_assignments:
        return truthful_count == 0 and not indices, "No valid assignments exist"
    for t_val, truth in valid_assignments:
        if truthful_count == t_val and indices == truth:
            return True, ""
    return False, "Output does not match any valid assignment"


def generate_matrix(size: int, seed: int) -> List[List[int]]:
    rng = random.Random(seed)
    return [[rng.randint(-9, 9) for _ in range(size)] for _ in range(size)]


def generate_02_cases() -> Iterable[TestCase]:
    configs: List[Tuple[int, int]] = [(1, 101), (2, 202), (3, 303)]
    for idx, (d, seed) in enumerate(configs, start=1):
        n = 2 ** d
        a = generate_matrix(n, seed)
        b = generate_matrix(n, seed + 1)
        lines = [str(d)]
        lines.extend(" ".join(str(x) for x in row) for row in a)
        lines.extend(" ".join(str(x) for x in row) for row in b)
        yield TestCase(
            name=f"02_case_{idx}",
            input_data="\n".join(lines) + "\n",
            metadata={"d": d, "A": a, "B": b},
        )


def verifier_02(test: TestCase, stdout: str, _elapsed: float) -> tuple[bool, str]:
    d = cast(int, test.metadata["d"])
    n = 2 ** d
    lines = [line.strip() for line in stdout.strip().splitlines() if line.strip()]
    if len(lines) != n:
        return False, f"Expected {n} output lines, got {len(lines)}"
    try:
        matrix = [[int(x) for x in line.split()] for line in lines]
    except ValueError:
        return False, "Output must contain integers"
    for row in matrix:
        if len(row) != n:
            return False, "Row length mismatch"
    expected = multiply_naive(
        cast(List[List[int]], test.metadata["A"]),
        cast(List[List[int]], test.metadata["B"]),
    )
    if matrix != expected:
        return False, "Matrix product mismatch"
    return True, ""


def multiply_naive(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    n = len(a)
    res = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = a[i][k]
            for j in range(n):
                res[i][j] += aik * b[k][j]
    return res


def generate_00_cases() -> Iterable[TestCase]:
    cases: List[Tuple[List[int], int, Tuple[int, int]]] = [
        ([2, 7, 11, 15], 9, (0, 1)),
        ([3, 2, 4, 8, 5], 6, (1, 2)),
        ([-3, 4, 3, 90], 0, (0, 2)),
        ([1, 5, 1, 5], 10, (1, 3)),
        ([6, -2, 5, -1, 4], 3, (1, 4)),
    ]
    for idx, (arr, target, pair) in enumerate(cases, start=1):
        n = len(arr)
        lines = [str(n), " ".join(str(x) for x in arr), str(target)]
        yield TestCase(
            name=f"00_case_{idx}",
            input_data="\n".join(lines) + "\n",
            metadata={"array": arr, "target": target, "pair": pair},
        )


def verifier_00(test: TestCase, stdout: str, _elapsed: float) -> tuple[bool, str]:
    arr = cast(List[int], test.metadata["array"])
    target = cast(int, test.metadata["target"])
    expected = cast(Tuple[int, int], test.metadata["pair"])
    tokens = stdout.strip().split()
    if len(tokens) < 2:
        return False, "Expected two indices"
    try:
        i, j = int(tokens[0]), int(tokens[1])
    except ValueError:
        return False, "Indices must be integers"
    n = len(arr)
    if not (0 <= i < n and 0 <= j < n):
        return False, "Index out of range"
    if i == j:
        return False, "Indices must be distinct"
    if arr[i] + arr[j] != target:
        return False, "Indices do not sum to target"
    if {i, j} != set(expected):
        return False, "Incorrect index pair"
    return True, ""




def _find_divisible_subarray(arr: List[int]) -> Tuple[int, int]:
    n = len(arr)
    prefix = 0
    seen: Dict[int, int] = {0: 0}
    for i in range(1, n + 1):
        prefix = (prefix + arr[i - 1]) % n
        if prefix in seen:
            start_idx = seen[prefix] + 1
            return start_idx, i
        seen[prefix] = i
    raise ValueError("No divisible subarray found")


def generate_03_cases() -> Iterable[TestCase]:
    rng = random.Random(606)
    base_cases = [
        [3, 1, 4, 2, 2],
        [5, -2, 7, 3, 9, -4],
        [10, 10, 10],
        [1, 2, 3, 4, 5, 6, 7],
    ]
    cases: List[List[int]] = base_cases[:]
    for _ in range(8):
        n = rng.randint(2, 40)
        arr = [rng.randint(-20, 20) for _ in range(n)]
        cases.append(arr)

    for idx, arr in enumerate(cases, start=1):
        l, r = _find_divisible_subarray(arr)
        n = len(arr)
        lines = [str(n), " ".join(str(x) for x in arr)]
        yield TestCase(
            name=f"03_case_{idx}",
            input_data="\n".join(lines) + "\n",
            metadata={"array": arr, "pair": (l, r)},
        )


def verifier_03(test: TestCase, stdout: str, _elapsed: float) -> tuple[bool, str]:
    arr = cast(List[int], test.metadata["array"])
    n = len(arr)
    tokens = stdout.strip().split()
    if not tokens:
        return False, "No output produced"
    first = tokens[0].upper()
    if first == "NO":
        return False, "A solution always exists"
    if first == "YES":
        tokens = tokens[1:]
    if len(tokens) < 2:
        return False, "Expected indices after YES"
    try:
        l, r = int(tokens[0]), int(tokens[1])
    except ValueError:
        return False, "Indices must be integers"
    if not (1 <= l <= r <= n):
        return False, "Indices out of range"
    sub_sum = sum(arr[l - 1 : r])
    if sub_sum % n != 0:
        return False, "Subarray sum is not divisible by N"
    return True, ""



def generate_04_cases() -> Iterable[TestCase]:
    rng = random.Random(505)
    configs: List[int] = [2, 3, 4]
    for idx, n in enumerate(configs, start=1):
        a = generate_matrix(n, rng.randint(0, 10_000))
        b = generate_matrix(n, rng.randint(0, 10_000))
        lines = [str(n)]
        lines.extend(" ".join(str(x) for x in row) for row in a)
        lines.extend(" ".join(str(x) for x in row) for row in b)
        yield TestCase(
            name=f"04_case_{idx}",
            input_data="\n".join(lines) + "\n",
            metadata={"A": a, "B": b},
        )


def verifier_04(test: TestCase, stdout: str, _elapsed: float) -> tuple[bool, str]:
    matrix_output = [line.strip() for line in stdout.strip().splitlines() if line.strip()]
    a_matrix = cast(List[List[int]], test.metadata["A"])
    b_matrix = cast(List[List[int]], test.metadata["B"])
    n = len(a_matrix)
    if len(matrix_output) != n:
        return False, f"Expected {n} rows, got {len(matrix_output)}"
    try:
        matrix = [[int(x) for x in row.split()] for row in matrix_output]
    except ValueError:
        return False, "Output must contain integers"
    if any(len(row) != n for row in matrix):
        return False, "Row length mismatch"
    expected = multiply_naive(a_matrix, b_matrix)
    if matrix != expected:
        return False, "Matrix product mismatch"
    return True, ""




def generate_05_cases() -> Iterable[TestCase]:
    answers: List[str] = [
        'the dancing grid keeps time',
        'melodies travel along diagonals',
        'hidden phrase leaps across measures',
    ]
    for idx, answer in enumerate(answers, start=1):
        yield TestCase(
            name=f"05_puzzle_{idx}",
            input_data='',
            metadata={'answer': answer, 'index': idx - 1},
        )




def verifier_05(test: TestCase, stdout: str, _elapsed: float) -> tuple[bool, str]:
    lines = [line.rstrip("\n") for line in stdout.splitlines() if not line.startswith('#')]
    idx = cast(int, test.metadata['index'])
    answer = cast(str, test.metadata['answer'])
    if idx >= len(lines):
        return False, f'Missing line {idx + 1} in SOLUTION.md'
    got = lines[idx].strip()
    if not got:
        return False, f'Line {idx + 1} is empty'
    if got != answer:
        return False, f'Line {idx + 1} is incorrect'
    return True, ''






PROBLEMS: Dict[str, ProblemSpec] = {
    "00": ProblemSpec(
        pid="00",
        name="Two-Sum Warmup",
        folder=Path("00"),
        generator=generate_00_cases,
        verifier=verifier_00,
        timeout=3.0,
        weight=10.0,
    ),
    "01": ProblemSpec(
        pid="01",
        name="Sneaky Islanders",
        folder=Path("01"),
        generator=generate_01_cases,
        verifier=verifier_01,
        timeout=5.0,
        weight=20.0,
    ),
    "02": ProblemSpec(
        pid="02",
        name="Tiled Matrix Multiplication",
        folder=Path("02"),
        generator=generate_02_cases,
        verifier=verifier_02,
        timeout=8.0,
        weight=25.0,
    ),
    "03": ProblemSpec(
        pid="03",
        name="Five Card Magic",
        folder=Path("03"),
        generator=generate_03_cases,
        verifier=verifier_03,
        timeout=5.0,
        weight=20.0,
    ),
    "04": ProblemSpec(
        pid="04",
        name="The Dancing Grid",
        folder=Path("04"),
        generator=generate_04_cases,
        verifier=verifier_04,
        timeout=20.0,
        weight=20.0,
    ),
    "05": ProblemSpec(
        pid="05",
        name="Ungarbling",
        folder=Path("05"),
        generator=generate_05_cases,
        verifier=verifier_05,
        timeout=300.0,
        weight=5.0,
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Vest Puzzles evaluator")
    parser.add_argument(
        "--problem",
        choices=PROBLEMS.keys(),
        nargs="*",
        help="Run only the specified problem IDs",
    )
    parser.add_argument("--list", action="store_true", help="List available problems")
    parser.add_argument("--no-submit", action="store_true", help="Skip scoreboard submission")
    parser.add_argument("--verbose", action="store_true", help="Show per-test details")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list:
        list_problems(PROBLEMS)
        return 0

    selected = set(args.problem) if args.problem else set(PROBLEMS.keys())

    team_name = ensure_team_profile()

    summary: Dict[str, ProblemResult] = {}
    total_score = 0.0
    total_max = 0.0

    for pid in selected:
        spec = PROBLEMS[pid]
        print(f"Running {pid} – {spec.name}")
        result = judge_problem(spec, verbose=args.verbose)
        summary[pid] = result
        total_score += result.score
        total_max += spec.weight
        print(
            f"  {result.passed}/{result.total} tests passed · "
            f"score {result.score:.1f}/{spec.weight:.1f} · elapsed {result.elapsed:.2f}s"
        )
        if result.details and args.verbose:
            for line in result.details:
                print("    "+line)
        elif result.details and result.passed != result.total:
            print("    " + result.details[0])

    print(f"Total score: {total_score:.1f}/{total_max:.1f}")

    results_payload = {
        "team": team_name,
        "teamName": team_name,
        "total": total_score,
        "max_total": total_max,
        "timestamp": time.time(),
        "problems": {
            pid: {
                "score": res.score,
                "max_score": res.max_score,
                "passed": res.passed,
                "total": res.total,
                "details": res.details,
            }
            for pid, res in summary.items()
        },
    }
    LATEST_RESULTS_PATH.write_text(json.dumps(results_payload, indent=2))

    scoreboard_url = os.environ.get("SCOREBOARD_URL")
    if not scoreboard_url:
        scoreboard_url = "https://vest-puzzles-scoreboard.vercel.app/api/submit"
    if scoreboard_url and not args.no_submit:
        submit_scoreboard(scoreboard_url, results_payload, verbose=args.verbose)
    elif not scoreboard_url:
        print("No SCOREBOARD_URL configured; skipping submission.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
