#!/usr/bin/env python3
"""Lanza un script bpy en Blender background con perfil aislado y registro por proceso.

Uso:  python3 herramientas/lanzar_blender.py CARPETA_RUN ETIQUETA SCRIPT [args del script...]

Reemplaza las copias de run_blender.py por experimento. Escribe CARPETA_RUN/logs/ETIQUETA.log y
.meta.json (comando, inicio/fin UTC, duración, código de salida) y usa CARPETA_RUN/profiles/ETIQUETA
como HOME y config de Blender (L-006). Se niega a sobrescribir un log existente.
Ver docs/04_procedimientos/EJECUCION_BLENDER.md.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BLENDER = Path("/Applications/Blender.app/Contents/MacOS/Blender")
BLENDER_SHA256 = "732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80"
FLAGS = ["--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "1"]


def rel(p):
    p = Path(p).resolve()
    return str(p.relative_to(REPO)) if p.is_relative_to(REPO) else str(p)


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    run_dir, label, script, script_args = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve(), sys.argv[4:]
    if not script.is_file():
        sys.exit(f"ERROR: no existe el script {script}")
    digest = hashlib.sha256(BLENDER.read_bytes()).hexdigest()
    if digest != BLENDER_SHA256:
        sys.exit(f"ERROR: el hash de Blender no coincide con ADR-0002: {digest}")
    logs = run_dir / "logs"
    log, meta_path = logs / f"{label}.log", logs / f"{label}.meta.json"
    if log.exists() or meta_path.exists():
        sys.exit(f"ERROR: ya existe el log '{label}'; usar otra etiqueta (no se sobrescribe)")
    logs.mkdir(parents=True, exist_ok=True)

    profile = run_dir / "profiles" / label
    env = os.environ.copy()
    for var, sub in (("HOME", "home"), ("BLENDER_USER_CONFIG", "config"), ("BLENDER_USER_SCRIPTS", "scripts"),
                     ("BLENDER_USER_DATAFILES", "data"), ("TMPDIR", "tmp")):
        (profile / sub).mkdir(parents=True, exist_ok=True)
        env[var] = str(profile / sub)

    command = [str(BLENDER), *FLAGS, "--python", str(script), "--", *script_args]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds")
    t = time.monotonic_ns()
    r = subprocess.run(command, cwd=REPO, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    meta = {
        "run_id": run_dir.name, "label": label, "command": command, "cwd": str(REPO), "profile": rel(profile),
        "blender_sha256": digest, "start_utc": start,
        "end_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds"),
        "duration_ms": round((time.monotonic_ns() - t) / 1e6, 3), "exit_code": r.returncode, "log": rel(log),
    }
    log.write_text(r.stdout + "\nRUN_META " + json.dumps(meta, sort_keys=True) + "\n")
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(r.stdout, end="")
    print(f"[{label}] exit={r.returncode} {meta['duration_ms']} ms -> {rel(log)}")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
