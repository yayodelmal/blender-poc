"""Check an optimistic base revision without changing any file."""
import hashlib
import json
import os
import sys


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: revision_guard.py EXPECTED_BASE_SHA BASE_PATH OBSERVED_REVISION_PATH")
    expected_base_sha, base_path, observed_path = sys.argv[1:]
    base_sha = sha256(base_path)
    observed_sha = sha256(observed_path)
    base_intact = base_sha == expected_base_sha
    observed_matches_base = observed_sha == expected_base_sha
    conflict = not base_intact or not observed_matches_base
    result = {
        "status": "CONFLICT_BLOCKED" if conflict else "NO_CONFLICT",
        "promotion_allowed": not conflict,
        "expected_base_sha256": expected_base_sha,
        "base_path": os.path.abspath(base_path),
        "base_sha256_observed": base_sha,
        "observed_revision_path": os.path.abspath(observed_path),
        "observed_revision_sha256": observed_sha,
        "base_intact": base_intact,
        "observed_revision_matches_expected_base": observed_matches_base,
    }
    print("EXP_BPY_002_REVISION_GUARD " + json.dumps(result, sort_keys=True))
    if not base_intact:
        raise RuntimeError("Accepted base artifact changed; stop promotion")
    if not conflict:
        raise RuntimeError("Expected conflict was not detected")


if __name__ == "__main__":
    main()
