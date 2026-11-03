"""Exporta un mesh a STL en mm y verifica un STL por reimportación. Se ejecuta dentro de Blender
(vía lanzar_blender.py), en procesos distintos para exportar y para verificar.

Exportar:  export ARCHIVO.blend SALIDA.stl [--objeto NOMBRE]
Verificar: verify ARCHIVO.stl SALIDA.json --dims X,Y,Z [--tol 0.5] [--import-scale 0.001]

Escala: 1 unidad de Blender = 1 m, así que el STL se escribe con global_scale=1000 (coordenadas en mm)
y se reimporta con 0,001 (L-004, EXP-BPY-003). `verify` con una escala de importación equivocada
(por ejemplo --import-scale 0.01) debe salir con código 2: es el control negativo de escala.
"""
import argparse
import json
import os
import sys
from pathlib import Path

import bmesh
import bpy

EXPORT_SCALE = 1000.0


def exportar(a):
    out = os.path.abspath(a.stl)
    if os.path.lexists(out):
        raise SystemExit(f"ERROR: no se sobrescribe {out}")
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.archivo), load_ui=False)
    meshes = [o for o in bpy.data.objects if o.type == "MESH" and (not a.objeto or o.name == a.objeto)]
    if len(meshes) != 1:
        raise SystemExit(f"ERROR: se esperaba 1 mesh y hay {len(meshes)}: {[o.name for o in meshes]}; usar --objeto")
    obj = meshes[0]
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    r = bpy.ops.wm.stl_export(filepath=out, check_existing=False, ascii_format=False, export_selected_objects=True,
                              global_scale=EXPORT_SCALE, use_scene_unit=False, forward_axis="Y", up_axis="Z",
                              apply_modifiers=True, evaluation_mode="DAG_EVAL_VIEWPORT")
    if "FINISHED" not in r or not os.path.isfile(out) or os.path.getsize(out) == 0:
        raise SystemExit("ERROR: la exportación STL falló o dejó un archivo vacío")
    print("STL_EXPORT " + json.dumps({"stl": out, "objeto": obj.name, "global_scale": EXPORT_SCALE, "bytes": os.path.getsize(out)}))


def contar(bm):
    sin_ver, n = set(bm.verts), 0
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


def verificar(a):
    esperado = [float(x) for x in a.dims.split(",")]
    antes = set(bpy.context.scene.objects)
    r = bpy.ops.wm.stl_import(filepath=os.path.abspath(a.stl), global_scale=a.import_scale, use_scene_unit=False,
                              forward_axis="Y", up_axis="Z", use_mesh_validate=True)
    nuevos = [o for o in bpy.context.scene.objects if o not in antes and o.type == "MESH"]
    checks = [{"check": "un_mesh_importado", "observado": [o.name for o in nuevos], "pass": "FINISHED" in r and len(nuevos) == 1}]
    medidas = {}
    if len(nuevos) == 1:
        o = nuevos[0]
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.normal_update()
        pts = [o.matrix_world @ v.co for v in o.data.vertices]
        dims = [(max(p[i] for p in pts) - min(p[i] for p in pts)) * 1000 for i in range(3)]
        checks.append({"check": "envolvente_mm", "esperado": esperado, "observado": dims, "tolerancia_mm": a.tol,
                       "pass": all(abs(d - e) <= a.tol for d, e in zip(dims, esperado))})
        comps = contar(bm)
        checks.append({"check": "una_componente", "observado": comps, "pass": comps == 1})
        man = bool(bm.edges) and all(e.is_manifold for e in bm.edges)
        checks.append({"check": "manifold", "observado": man, "pass": man})
        vol = bm.calc_volume(signed=True) * abs(o.matrix_world.to_3x3().determinant()) * 1e9
        checks.append({"check": "volumen_positivo", "observado_mm3": vol, "pass": vol > 0})
        medidas = {"dimensiones_mm": dims, "volumen_mm3": vol, "triangulos": len(o.data.polygons)}
        bm.free()
    ok = all(c["pass"] for c in checks)
    res = {"status": "PASS" if ok else "FAIL", "stl": os.path.abspath(a.stl), "import_scale": a.import_scale, "medidas": medidas, "checks": checks}
    Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
    Path(a.salida).write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
    print("STL_VERIFICACION " + json.dumps({"status": res["status"], "fallos": [c["check"] for c in checks if not c["pass"]]}))
    if not ok:
        raise SystemExit(2)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="modo", required=True)
    e = sub.add_parser("export")
    e.add_argument("archivo")
    e.add_argument("stl")
    e.add_argument("--objeto")
    v = sub.add_parser("verify")
    v.add_argument("stl")
    v.add_argument("salida")
    v.add_argument("--dims", required=True)
    v.add_argument("--tol", type=float, default=0.5)
    v.add_argument("--import-scale", type=float, default=0.001)
    a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:])
    exportar(a) if a.modo == "export" else verificar(a)


main()
