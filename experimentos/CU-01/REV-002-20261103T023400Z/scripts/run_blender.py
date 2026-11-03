"""Run Blender with a fresh, experiment-local profile and metadata log."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

EXP_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
BLENDER = Path("/Applications/Blender.app/Contents/MacOS/Blender")
EXPECTED_SHA256 = "732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80"
RUN_ID = "CU-01-REV-002-20261103T023400Z"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    if len(sys.argv) < 3 or sys.argv[2] != "--":
        raise SystemExit("usage: run_blender.py LABEL -- BLENDER_ARGUMENTS...")
    label = sys.argv[1]
    observed_sha = sha256(BLENDER)
    if observed_sha != EXPECTED_SHA256:
        raise SystemExit(f"Blender hash mismatch: {observed_sha}")
    command = [str(BLENDER), *sys.argv[3:]]
    profile = EXP_DIR / "profiles" / label
    for child in ("home", "config", "scripts", "data", "tmp"):
        (profile / child).mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({
        "HOME": str(profile / "home"),
        "BLENDER_USER_CONFIG": str(profile / "config"),
        "BLENDER_USER_SCRIPTS": str(profile / "scripts"),
        "BLENDER_USER_DATAFILES": str(profile / "data"),
        "TMPDIR": str(profile / "tmp"),
    })
    start = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds")
    start_ns = time.monotonic_ns()
    result = subprocess.run(command, cwd=REPO_ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    duration_ms = (time.monotonic_ns() - start_ns) / 1_000_000
    end = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds")
    metadata = {
        "run_id": RUN_ID,
        "label": label,
        "command": command,
        "cwd": str(REPO_ROOT),
        "profile": str(profile),
        "blender_sha256": observed_sha,
        "blender_version": "Blender 5.4.0 Alpha (build 745ab9a3e3c5)",
        "start_utc": start,
        "end_utc": end,
        "duration_ms": round(duration_ms, 3),
        "exit_code": result.returncode,
        "log": str((EXP_DIR / "logs" / f"{label}.log").relative_to(REPO_ROOT)),
    }
    log_path = EXP_DIR / "logs" / f"{label}.log"
    meta_path = EXP_DIR / "logs" / f"{label}.meta.json"
    if log_path.exists() or meta_path.exists():
        raise FileExistsError(f"refusing to overwrite run logs for {label}")
    log_path.write_text(result.stdout + "\nRUN_META " + json.dumps(metadata, sort_keys=True) + "\n", encoding="utf-8")
    meta_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result.stdout, end="")
    print("RUN_META " + json.dumps(metadata, sort_keys=True))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
