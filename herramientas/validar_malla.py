"""Validador base de una malla en un .blend. Se ejecuta dentro de Blender (vía lanzar_blender.py).

Uso (tras el `--`):  ARCHIVO.blend SALIDA.json --dims X,Y,Z [--tol 0.01] [--volumen MM3 --tol-volumen 1]
                     [--cavidad X,Y,Z --tol-cavidad 0.01] [--componentes 1] [--objeto NOMBRE]

Comprueba sobre la malla evaluada, en mm: un solo mesh, envolvente, componentes, manifold, orientación
coherente, volumen positivo, volumen esperado (opcional) y ausencia de elementos degenerados.
Con --cavidad mide el hueco interior con rayos desde su centro: ancho en X e Y (12 rayos contra las
paredes), profundidad hasta el piso (9 rayos), planos interiores planos, piso cerrado y tapa abierta.
Escribe el JSON de evidencia y sale con código 2 si algo falla. No guarda el .blend.
"""
import argparse
import json
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def contar_componentes(bm):
    sin_ver = set(bm.verts)
    n = 0
    while sin_ver:
        n += 1
        pila = [sin_ver.pop()]
        while pila:
            v = pila.pop()
            for e in v.link_edges:
                o = e.other_vert(v)
                if o in sin_ver:
                    sin_ver.remove(o)
                    pila.append(o)
    return n


def medir_cavidad(obj, bm, pts, esperado, tol):
    """Mide el hueco interior lanzando rayos desde su centro. Coordenadas en metros; resultados en mm."""
    bm2 = bm.copy()
    bm2.transform(obj.matrix_world)
    tree = BVHTree.FromBMesh(bm2)
    xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    zmin, zmax = min(zs), max(zs)
    zmid = (zmin + zmax) / 2
    ex, ey, ez = (v / 1000 for v in esperado)

    def tiro(origen, dir_):
        hit = tree.ray_cast(Vector(origen), Vector(dir_), 10.0)
        return hit[0]

    def planos(eje, signo, desplazamientos, fijo_otro):
        valores = []
        for d in desplazamientos:
            if eje == 0:
                h = tiro((cx, cy + d, zmid), (signo, 0, 0))
                valores.append(None if h is None else h.x)
            else:
                h = tiro((cx + d, cy, zmid), (0, signo, 0))
                valores.append(None if h is None else h.y)
        return valores

    checks = []
    medidas = {}
    for eje, nombre, mitad, otro in ((0, "x", ex, ey), (1, "y", ey, ex)):
        desp = [-otro / 4, 0.0, otro / 4]
        plus, minus = planos(eje, 1, desp, None), planos(eje, -1, desp, None)
        if None in plus or None in minus:
            checks.append({"check": f"cavidad_{nombre}", "observado": "algun rayo no toco pared", "pass": False})
            continue
        spread = max(max(plus) - min(plus), max(minus) - min(minus)) * 1000
        ancho = (sum(plus) / 3 - sum(minus) / 3) * 1000
        medidas[f"cavidad_{nombre}_mm"] = ancho
        checks.append({"check": f"cavidad_{nombre}_mm", "esperado": mitad * 1000, "observado": ancho, "tolerancia_mm": tol,
                       "pass": abs(ancho - mitad * 1000) <= tol})
        checks.append({"check": f"plano_interior_plano_{nombre}", "dispersion_mm": spread, "tolerancia_mm": tol, "pass": spread <= tol})

    suelo = []
    for ox in (-ex / 4, 0.0, ex / 4):
        for oy in (-ey / 4, 0.0, ey / 4):
            h = tiro((cx + ox, cy + oy, zmid), (0, 0, -1))
            suelo.append(None if h is None else h.z)
    cerrado = None not in suelo
    checks.append({"check": "piso_cerrado", "rayos": len(suelo), "observado": cerrado, "pass": cerrado})
    if cerrado:
        piso = sum(suelo) / len(suelo)
        spread = (max(suelo) - min(suelo)) * 1000
        prof = (zmax - piso) * 1000
        medidas.update({"piso_z_mm": (piso - zmin) * 1000, "cavidad_z_mm": prof})
        checks.append({"check": "cavidad_z_mm", "esperado": ez * 1000, "observado": prof, "tolerancia_mm": tol, "pass": abs(prof - ez * 1000) <= tol})
        checks.append({"check": "piso_plano", "dispersion_mm": spread, "tolerancia_mm": tol, "pass": spread <= tol})
    arriba = tiro((cx, cy, zmid), (0, 0, 1)) is None
    checks.append({"check": "tapa_abierta", "observado": arriba, "pass": arriba})
    bm2.free()
    return checks, medidas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("blend")
    ap.add_argument("salida")
    ap.add_argument("--dims", required=True)
    ap.add_argument("--tol", type=float, default=0.01)
    ap.add_argument("--volumen", type=float)
    ap.add_argument("--tol-volumen", type=float, default=1.0)
    ap.add_argument("--cavidad", help="cavidad esperada X,Y,Z en mm (profundidad medida desde el borde superior)")
    ap.add_argument("--tol-cavidad", type=float, default=0.01)
    ap.add_argument("--componentes", type=int, default=1)
    ap.add_argument("--objeto")
    a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:])
    esperado = [float(x) for x in a.dims.split(",")]

    blend = str(Path(a.blend).resolve())
    bpy.ops.wm.open_mainfile(filepath=blend, load_ui=False)
    meshes = [o for o in bpy.data.objects if o.type == "MESH" and (not a.objeto or o.name == a.objeto)]
    checks = [{"check": "un_solo_mesh", "observado": [o.name for o in meshes], "pass": len(meshes) == 1}]
    if len(meshes) != 1:
        return finish(a.salida, blend, checks, {})
    obj = meshes[0]
    dg = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(obj.evaluated_get(dg), depsgraph=dg)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.normal_update()

    pts = [obj.matrix_world @ v.co for v in mesh.vertices]
    dims = [(max(p[i] for p in pts) - min(p[i] for p in pts)) * 1000 for i in range(3)]
    checks.append({"check": "envolvente_mm", "esperado": esperado, "observado": dims, "tolerancia_mm": a.tol,
                   "pass": all(abs(d - e) <= a.tol for d, e in zip(dims, esperado))})
    comps = contar_componentes(bm)
    checks.append({"check": "componentes", "esperado": a.componentes, "observado": comps, "pass": comps == a.componentes})
    manifold = bool(bm.edges) and all(e.is_manifold for e in bm.edges)
    checks.append({"check": "manifold", "observado": manifold, "pass": manifold})
    coherente = all(e.is_contiguous for e in bm.edges if e.is_manifold)
    checks.append({"check": "orientacion_coherente", "observado": coherente, "pass": coherente})
    vol = bm.calc_volume(signed=True) * abs(obj.matrix_world.to_3x3().determinant()) * 1e9
    checks.append({"check": "volumen_positivo", "observado_mm3": vol, "pass": vol > 0})
    if a.volumen is not None:
        checks.append({"check": "volumen_esperado", "esperado_mm3": a.volumen, "observado_mm3": vol,
                       "tolerancia_mm3": a.tol_volumen, "pass": abs(vol - a.volumen) <= a.tol_volumen})
    chicas = sum(e.calc_length() <= 1e-9 for e in bm.edges) + sum(f.calc_area() <= 1e-12 for f in bm.faces)
    checks.append({"check": "sin_degenerados", "observado": chicas, "pass": chicas == 0})
    if a.cavidad:
        c, m = medir_cavidad(obj, bm, pts, [float(x) for x in a.cavidad.split(",")], a.tol_cavidad)
        checks += c
    else:
        m = {}
    bm.free()
    finish(a.salida, blend, checks, {**m, "objeto": obj.name, "dimensiones_mm": dims, "volumen_mm3": vol, "componentes": comps})


def finish(salida, blend, checks, medidas):
    ok = all(c["pass"] for c in checks)
    res = {"status": "PASS" if ok else "FAIL", "archivo": blend, "blender": bpy.app.version_string, "medidas": medidas, "checks": checks}
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    Path(salida).write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
    print("VALIDACION " + json.dumps({"status": res["status"], "fallos": [c["check"] for c in checks if not c["pass"]]}))
    if not ok:
        raise SystemExit(2)


main()
