#!/usr/bin/env python3
"""Package puzzle directories and submit them to the remote evaluation endpoint."""
from __future__ import annotations

import argparse
import getpass
import http.client
import json
import os
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

DEFAULT_DIRS = ["01", "02", "03", "04", "05"]
PROFILE_PATH = Path(".profile")


def read_team_name(interactive: bool = True) -> str:
    if PROFILE_PATH.exists():
        for line in PROFILE_PATH.read_text().splitlines():
            if line.startswith("TEAM_NAME="):
                name = line.split("=", 1)[1].strip()
                if name:
                    return name
    if not interactive:
        raise RuntimeError("Team name missing and prompting disabled")
    name = input("Enter team name: ").strip() or getpass.getuser()
    PROFILE_PATH.write_text(f"TEAM_NAME={name}\n")
    return name


def zip_directories(directories: Iterable[str], output: Path) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for directory in directories:
            base = Path(directory)
            if not base.exists():
                raise FileNotFoundError(f"Directory '{directory}' does not exist")
            for path in base.rglob("*"):
                if path.is_file():
                    zf.write(path, arcname=str(path))
                elif path.is_dir() and not any(path.iterdir()):
                    zf.writestr(str(path) + "/", b"")


def build_multipart(metadata: dict, bundle_path: Path) -> tuple[bytes, str]:
    boundary = f"----VestBoundary{uuid.uuid4().hex}"
    parts: list[bytes] = []

    meta_bytes = json.dumps(metadata, separators=(",", ":")).encode("utf-8")
    parts.append(
        (
            f"--{boundary}\r\n"
            "Content-Disposition: form-data; name=\"metadata\"\r\n"
            "Content-Type: application/json\r\n\r\n"
        ).encode("utf-8")
    )
    parts.append(meta_bytes + b"\r\n")

    file_bytes = bundle_path.read_bytes()
    filename = bundle_path.name
    parts.append(
        (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"bundle\"; filename=\"{filename}\"\r\n"
            "Content-Type: application/zip\r\n\r\n"
        ).encode("utf-8")
    )
    parts.append(file_bytes + b"\r\n")

    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(parts)
    return body, boundary


def post_submission(url: str, body: bytes, boundary: str, token: str | None) -> tuple[int, dict | str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http:// or https://")
    connection_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    conn = connection_cls(parsed.netloc, timeout=60)

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"

    conn.request("POST", path, body=body, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    try:
        parsed_body = json.loads(data.decode("utf-8"))
    except Exception:  # pylint: disable=broad-except
        parsed_body = data.decode("utf-8", errors="replace")

    return response.status, parsed_body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Submit solutions to the remote evaluation endpoint")
    parser.add_argument(
        "--url",
        help="Override evaluation endpoint (defaults to EVALUATE_URL env variable)",
    )
    parser.add_argument(
        "--token",
        help="Bearer token for authorization (defaults to EVALUATE_TOKEN env variable)",
    )
    parser.add_argument(
        "--zip",
        dest="zip_path",
        help="Write the bundle to this path before uploading (kept after submission)",
    )
    parser.add_argument(
        "--dirs",
        nargs="+",
        default=DEFAULT_DIRS,
        help="Directories to include in the submission bundle",
    )
    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="Fail instead of prompting for team name if .profile is missing",
    )
    args = parser.parse_args(argv)

    url = args.url or os.environ.get("EVALUATE_URL")
    if not url:
        print("Error: evaluation URL not provided. Set EVALUATE_URL or pass --url.", file=sys.stderr)
        return 2
    token = args.token or os.environ.get("EVALUATE_TOKEN")

    try:
        team_name = read_team_name(interactive=not args.no_prompt)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    # Build ZIP archive
    if args.zip_path:
        bundle_path = Path(args.zip_path).expanduser().resolve()
        zip_directories(args.dirs, bundle_path)
        cleanup = False
    else:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        tmp.close()
        bundle_path = Path(tmp.name)
        cleanup = True
        try:
            zip_directories(args.dirs, bundle_path)
        except Exception:
            bundle_path.unlink(missing_ok=True)
            raise

    metadata = {
        "teamName": team_name,
        "dirs": args.dirs,
    }

    body, boundary = build_multipart(metadata, bundle_path)
    try:
        status, response_body = post_submission(url, body, boundary, token)
    finally:
        if cleanup:
            bundle_path.unlink(missing_ok=True)

    print(f"Server responded with status {status}")
    if isinstance(response_body, dict):
        print(json.dumps(response_body, indent=2))
    else:
        print(response_body)

    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    sys.exit(main())
