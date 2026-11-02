"""Validate optimistic revision base identity without modifying artifacts."""
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
    if len(sys.argv) != 5:
        raise SystemExit("usage: revision_guard_corrected.py EXPECTED_BASE_SHA OBSERVED_BASE_PATH CANDIDATE_PATH CANDIDATE_RECORDED_BASE_SHA")
    expected_base_sha, observed_base_path, candidate_path, candidate_base_sha = sys.argv[1:]
    observed_base_sha = sha256(observed_base_path)
    candidate_file_sha = sha256(candidate_path)
    base_matches = observed_base_sha == expected_base_sha
    candidate_references_base = candidate_base_sha == expected_base_sha
    conflict = not base_matches or not candidate_references_base
    result = {
        "status": "CONFLICT_BLOCKED" if conflict else "BASE_MATCH_PROMOTION_ELIGIBLE",
        "promotion_allowed": not conflict,
        "expected_base_sha256": expected_base_sha,
        "observed_base_path": os.path.abspath(observed_base_path),
        "observed_base_sha256": observed_base_sha,
        "base_matches_expected": base_matches,
        "candidate_path": os.path.abspath(candidate_path),
        "candidate_sha256": candidate_file_sha,
        "candidate_recorded_base_sha256": candidate_base_sha,
        "candidate_references_expected_base": candidate_references_base,
    }
    print("EXP_BPY_002_REVISION_GUARD_CORRECTED " + json.dumps(result, sort_keys=True))
    if conflict:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
