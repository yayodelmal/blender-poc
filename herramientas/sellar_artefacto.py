#!/usr/bin/env python3
"""Sella y verifica artefactos en un registro JSON Lines. Solo biblioteca estándar.

Ver docs/04_procedimientos/INTEGRIDAD.md.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

ROLES = ("produced", "input", "evidence")
VALIDATIONS = ("PASS", "FAIL", "INCONCLUSIVE", "NOT RUN")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_registro(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def seal_file(path):
    if not os.path.isfile(path):
        sys.exit(f"ERROR: no existe el archivo: {path}")
    return {"size_bytes": os.path.getsize(path), "sha256": sha256_of(path)}


def cmd_seal(args):
    existing = read_registro(args.registro)
    if any(r["run_id"] == args.run_id and r["artifact_id"] == args.artifact_id for r in existing):
        sys.exit(f"ERROR: ya existe {args.run_id}/{args.artifact_id} en el registro")
    record = {
        "run_id": args.run_id,
        "artifact_id": args.artifact_id,
        "path": args.path,
        **seal_file(args.path),
        "sealed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "role": args.role,
        "mutable": args.mutable,
        "exit_code": args.exit_code,
        "validation": args.validation,
        "approval": args.approval,
    }
    if args.producer_script:
        record["producer_script"] = args.producer_script
        record["producer_script_sha256"] = seal_file(args.producer_script)["sha256"]
    if args.blender:
        record["blender"] = args.blender
    if args.expected:
        record["expected"] = args.expected
    if args.observed:
        record["observed"] = args.observed
    os.makedirs(os.path.dirname(os.path.abspath(args.registro)), exist_ok=True)
    with open(args.registro, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"SELLADO {args.run_id}/{args.artifact_id} {record['size_bytes']} B {record['sha256']}")


def cmd_verify(args):
    records = read_registro(args.registro)
    if not records:
        sys.exit("ERROR: registro vacío o inexistente")
    failures = 0
    for r in records:
        label = f"{r['run_id']}/{r['artifact_id']}"
        if not os.path.isfile(r["path"]):
            print(f"FALTA     {label} {r['path']}")
            failures += 1
            continue
        now = seal_file(r["path"])
        if now["sha256"] != r["sha256"] or now["size_bytes"] != r["size_bytes"]:
            kind = "CAMBIADO (mutable)" if r.get("mutable") else "CAMBIADO"
            print(f"{kind} {label} sellado={r['sha256'][:12]}/{r['size_bytes']} actual={now['sha256'][:12]}/{now['size_bytes']}")
            failures += 1
        else:
            print(f"OK        {label}")
    sys.exit(1 if failures else 0)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("seal")
    s.add_argument("--registro", required=True)
    s.add_argument("--run-id", required=True)
    s.add_argument("--artifact-id", required=True)
    s.add_argument("--path", required=True)
    s.add_argument("--role", choices=ROLES, required=True)
    s.add_argument("--producer-script")
    s.add_argument("--exit-code", type=int)
    s.add_argument("--blender")
    s.add_argument("--expected")
    s.add_argument("--observed")
    s.add_argument("--validation", choices=VALIDATIONS, default="NOT RUN")
    s.add_argument("--approval")
    s.add_argument("--mutable", action="store_true")
    s.set_defaults(func=cmd_seal)
    v = sub.add_parser("verify")
    v.add_argument("--registro", required=True)
    v.set_defaults(func=cmd_verify)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
