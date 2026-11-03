#!/usr/bin/env python3
"""Sella de una vez los artefactos de una carpeta de run, con las reglas de INTEGRIDAD.md.

Uso:  python3 herramientas/sellar_carpeta.py CARPETA_RUN --validation PASS [--input RUTA ...]

Registra en CARPETA_RUN/registro_artefactos.jsonl: artifacts/ (produced), evidencias/, scripts/ y logs/
(evidence) y cada --input (input). No incluye reports/ (regla 7) ni profiles/. Los hashes y tamaños los
calcula sellar_artefacto.py; aquí no se teclea ninguno. Se detiene si el registro ya existe (los registros
no se reescriben) y termina verificando todo.
"""
import argparse
import fnmatch
import os
import sys
from datetime import datetime, timezone
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sellar_artefacto as sa  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETAS = (("artifacts", "produced"), ("evidencias", "evidence"), ("scripts", "evidence"), ("logs", "evidence"))
OMITIR = (".DS_Store", ".blend1")
MUTABLES = ["*.3mf"]  # una aplicación (Creality Print) puede reescribirlos: se registran con mutable=true


def rel(p):
    return os.path.relpath(os.path.abspath(p), REPO)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("carpeta")
    ap.add_argument("--validation", choices=sa.VALIDATIONS, required=True)
    ap.add_argument("--input", action="append", default=[], help="archivo de entrada ya existente (repetible)")
    ap.add_argument("--mutable", action="append", default=[], help="patrón de nombre (fnmatch) a registrar como mutable; *.3mf ya lo es")
    ap.add_argument("--exit-code", type=int, default=0, help="código de salida del proceso productor")
    ap.add_argument("--blender", help="texto de versión/hash de Blender (opcional)")
    ap.add_argument("--expected", help="parámetros esperados, texto libre (opcional)")
    ap.add_argument("--observed", help="resumen de lo medido, texto libre (opcional)")
    a = ap.parse_args()

    carpeta = os.path.abspath(a.carpeta)
    registro = os.path.join(carpeta, "registro_artefactos.jsonl")
    if os.path.exists(registro):
        sys.exit(f"ERROR: ya existe {rel(registro)}; los registros no se reescriben. Usar una carpeta de run nueva.")
    run_id = os.path.basename(carpeta)

    items = []
    for sub, role in CARPETAS:
        base = os.path.join(carpeta, sub)
        for raiz, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in sorted(files):
                if f in OMITIR or f.endswith(OMITIR):
                    continue
                items.append((os.path.join(raiz, f), role))
    for p in a.input:
        items.append((os.path.abspath(p), "input"))
    if not items:
        sys.exit("ERROR: no hay nada que sellar")

    ids = set()
    with open(registro, "a", encoding="utf-8") as out:
        for path, role in items:
            aid = os.path.relpath(path, carpeta).replace(os.sep, "_") if role != "input" else "input_" + os.path.basename(path)
            if aid in ids:
                sys.exit(f"ERROR: artifact_id repetido: {aid}")
            ids.add(aid)
            rec = {
                "run_id": run_id, "artifact_id": aid, "path": rel(path), **sa.seal_file(path),
                "sealed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "role": role, "mutable": any(fnmatch.fnmatch(os.path.basename(path), g) for g in MUTABLES + a.mutable), "exit_code": a.exit_code, "validation": a.validation, "approval": None,
            }
            for k, v in (("blender", a.blender), ("expected", a.expected), ("observed", a.observed)):
                if v:
                    rec[k] = v
            out.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"SELLADOS {len(items)} artefactos en {rel(registro)}")

    class V:
        pass
    v = V()
    v.registro = registro
    try:
        sa.cmd_verify(v)
    except SystemExit as e:
        raise SystemExit(e.code)


if __name__ == "__main__":
    main()
