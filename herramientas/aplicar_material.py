#!/usr/bin/env python3
"""Ruta corta para cambios solo de apariencia: aplica un material a un .blend.

Un solo proceso de Blender. Comprueba que la geometría no cambió, escribe un
.blend nuevo (nunca sobrescribe) y añade una línea a registro_variantes.jsonl.
Ver .claude/skills/blender-color/SKILL.md.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BLENDER = Path("/Applications/Blender.app/Contents/MacOS/Blender")
BLENDER_SHA256 = "732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80"
REGISTRO = REPO / "variantes" / "registro_variantes.jsonl"
BPY_SCRIPT = Path(__file__).with_name("_aplicar_material_bpy.py")
COLORES = {
    "blanco": "ffffff", "negro": "000000", "gris": "808080", "rojo": "d32f2f",
    "verde": "388e3c", "azul": "1976d2", "amarillo": "fbc02d", "naranja": "f57c00",
}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_color(text):
    hex_ = COLORES.get(text.lower(), text.lstrip("#"))
    if len(hex_) != 6 or any(c not in "0123456789abcdefABCDEF" for c in hex_):
        sys.exit(f"ERROR: color no válido: {text} (nombre conocido {sorted(COLORES)} o hex RRGGBB)")
    # Blender espera lineal; sRGB -> lineal por canal.
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return [lin(int(hex_[i:i + 2], 16)) for i in (0, 2, 4)] + [1.0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fuente", help=".blend de origen (no se modifica)")
    ap.add_argument("--color", required=True, help="nombre (blanco, negro...) o hex RRGGBB")
    ap.add_argument("--rugosidad", type=float, default=0.8, help="0 brillante, 1 mate (def. 0.8)")
    ap.add_argument("--objeto", help="nombre del objeto; por defecto, el único mesh de la escena")
    ap.add_argument("--nombre-material", default=None)
    ap.add_argument("--salida", help="destino .blend; por defecto variantes/<fuente>_<color>.blend")
    args = ap.parse_args()

    src = Path(args.fuente).resolve()
    if not src.is_file():
        sys.exit(f"ERROR: no existe {src}")
    dst = Path(args.salida).resolve() if args.salida else REPO / "variantes" / f"{src.stem}_{args.color.lstrip('#')}.blend"
    if dst.exists():
        sys.exit(f"ERROR: el destino ya existe, no se sobrescribe: {dst}")
    if sha256_of(BLENDER) != BLENDER_SHA256:
        sys.exit("ERROR: el hash de Blender no coincide con ADR-0002; registrar la build distinta antes de seguir")

    color = parse_color(args.color)
    src_hash_before = sha256_of(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    nombre_mat = args.nombre_material or f"Mat_{args.color.lstrip('#')}"

    # Perfil temporal aislado (L-006: Blender escribe miniaturas en HOME).
    with tempfile.TemporaryDirectory(prefix="blender_variante_") as tmp:
        env = os.environ.copy()
        for k, d in (("HOME", "home"), ("BLENDER_USER_CONFIG", "config"), ("BLENDER_USER_SCRIPTS", "scripts"),
                     ("BLENDER_USER_DATAFILES", "data"), ("TMPDIR", "tmp")):
            (Path(tmp) / d).mkdir()
            env[k] = str(Path(tmp) / d)
        cmd = [str(BLENDER), "--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "1",
               "--python", str(BPY_SCRIPT), "--", str(src), str(dst), json.dumps(color),
               str(args.rugosidad), args.objeto or "", nombre_mat]
        t = time.monotonic()
        r = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        dur = round(time.monotonic() - t, 2)

    linea = next((l for l in r.stdout.splitlines() if l.startswith("VARIANTE ")), None)
    if r.returncode != 0 or linea is None:
        print(r.stdout)
        if dst.exists():
            dst.unlink()  # no dejar un candidato no verificado
        sys.exit(f"FAIL: Blender terminó con código {r.returncode}")
    resultado = json.loads(linea[len("VARIANTE "):])
    if sha256_of(src) != src_hash_before:
        sys.exit("FAIL: la fuente cambió durante la ejecución")

    registro = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "fuente": str(src.relative_to(REPO)) if src.is_relative_to(REPO) else str(src),
        "fuente_sha256": src_hash_before,
        "salida": str(dst.relative_to(REPO)) if dst.is_relative_to(REPO) else str(dst),
        "salida_sha256": sha256_of(dst),
        "color": args.color, "rugosidad": args.rugosidad, "duracion_s": dur,
        "geometria_sha256": resultado["geometria_sha256"], "objetos": resultado["objetos"],
        "geometria_sin_cambios": True,
    }
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"PASS en {dur} s -> {registro['salida']} (geometría idéntica, {len(resultado['objetos'])} objeto(s))")


if __name__ == "__main__":
    main()
